from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from api import templates, _l, flash
from api.config.database import get_db
from api.models.account import Bank
from api.models.provider import Provider
from api.schemas.account import Bank as BankSchema
from api.schemas.provider import ProviderCreate, Provider as ProviderSchema
from api.schemas.base import MessageResponse

from api.utils import auth

provider = APIRouter()


@provider.get(
    "/provider", tags=["provider"], description="Get the list of providers created"
)
@auth.check_jwt_auth
async def list_providers(
    request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    providers = Provider.get_all(db, skip=skip, limit=limit)
    provider_entities = [ProviderSchema.from_orm(provider) for provider in providers]
    return templates.TemplateResponse(
        "provider/index.html",
        {"request": request, **_l, "providers": provider_entities},
    )


@provider.get("/provider/create")
@auth.check_jwt_auth
async def create_view(request: Request, db: Session = Depends(get_db)):
    banks = Bank.get_all(db)
    bank_entities = [BankSchema.from_orm(bank) for bank in banks]
    return templates.TemplateResponse(
        "provider/create.html",
        {"request": request, "banks": bank_entities, **_l},
    )


@provider.post(
    "/provider",
    response_model=MessageResponse,
    status_code=200,
    tags=["provider"],
    description="Create a new provider",
)
@auth.check_jwt_auth
async def create_provider(
    request: Request,
    provider: ProviderCreate,
    db: Session = Depends(get_db),
):
    redirect_url = request.url_for("list_providers")
    response = dict(redirect_to=redirect_url, message=_l.get("creation_success"))
    Provider.create(db, data=provider.dict())
    flash(request, response["message"], "success")
    return response


@provider.get("/provider/update/{provider_id}")
@auth.check_jwt_auth
async def update_view(
    request: Request, provider_id: str, db: Session = Depends(get_db)
):
    provider = Provider.get_by_id(db, id=provider_id)
    if not provider:
        flash(request, _l.get("not_found"), "success")
        redirect_url = request.url_for("list_providers")
        return RedirectResponse(redirect_url)

    # Get banks to be assigned
    banks = Bank.get_all(db)
    bank_entities = [BankSchema.from_orm(bank) for bank in banks]
    provider_entity = ProviderSchema.from_orm(provider)
    return templates.TemplateResponse(
        "provider/update.html",
        {"request": request, "provider": provider_entity, "banks": bank_entities, **_l},
    )


@provider.patch(
    "/provider/{provider_id}",
    response_model=MessageResponse,
    status_code=200,
    tags=["provider"],
    description="Update an existing provider",
)
@auth.check_jwt_auth
async def update_provider(
    request: Request,
    provider: ProviderCreate,
    provider_id: str,
    db: Session = Depends(get_db),
):
    redirect_url = request.url_for("list_providers")
    response = dict(redirect_to=redirect_url, message=_l.get("update_success"))

    # Get provider model to be updated
    bank_model = Provider.get_by_id(db, provider_id)
    bank_model.update(db, data=provider.dict())
    flash(request, response["message"], "success")

    return response
