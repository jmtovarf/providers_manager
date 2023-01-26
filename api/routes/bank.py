from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from api import templates, _l, flash
from api.config.database import get_db
from api.models.account import Bank
from api.schemas.account import BankCreate, Bank as BankSchema
from api.schemas.base import MessageResponse

from api.utils import auth

bank = APIRouter()


@bank.get("/bank")
@auth.check_jwt_auth
async def list_banks(
    request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    banks = Bank.get_all(db, skip=skip, limit=limit)
    bank_entities = [BankSchema.from_orm(bank) for bank in banks]
    return templates.TemplateResponse(
        "bank/index.html",
        {"request": request, **_l, "banks": bank_entities},
    )


@bank.get("/bank/details/{bank_id}")
@auth.check_jwt_auth
async def get_bank(request: Request, bank_id: int):
    return templates.TemplateResponse(
        "bank/details.html",
        {"request": request, **_l},
    )


@bank.get("/bank/create")
@auth.check_jwt_auth
async def create_view(request: Request):
    return templates.TemplateResponse(
        "bank/create.html",
        {"request": request, **_l},
    )


@bank.get("/bank/update/{bank_id}")
@auth.check_jwt_auth
async def update_view(request: Request, bank_id: int, db: Session = Depends(get_db)):
    bank = Bank.get_by_id(db, id=bank_id)
    if not bank:
        flash(request, _l.get("not_found"), "success")
        redirect_url = request.url_for("list_banks")
        return RedirectResponse(redirect_url)

    bank_entity = BankSchema.from_orm(bank)
    return templates.TemplateResponse(
        "bank/update.html",
        {"request": request, "bank": bank_entity, **_l},
    )


@bank.post(
    "/bank",
    response_model=MessageResponse,
    status_code=200,
    tags=["bank"],
    description="Create a new bank",
)
@auth.check_jwt_auth
async def create_bank(
    request: Request, bank: BankCreate, db: Session = Depends(get_db)
):
    redirect_url = request.url_for("list_banks")
    response = dict(redirect_to=redirect_url, message=_l.get("creation_success"))
    Bank.create(db, bank)
    flash(request, response["message"], "success")
    return response


@bank.patch(
    "/bank/{bank_id}",
    response_model=MessageResponse,
    status_code=200,
    tags=["bank"],
    description="Update an existing bank",
)
@auth.check_jwt_auth
async def update_bank(
    request: Request, bank: BankCreate, bank_id: int, db: Session = Depends(get_db)
):
    redirect_url = request.url_for("list_banks")
    response = dict(redirect_to=redirect_url, message=_l.get("update_success"))
    bank_model = Bank.get_by_id(db, bank_id)
    bank_model.update(db, bank.dict())
    flash(request, response["message"], "success")
    return response
