from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Union

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
