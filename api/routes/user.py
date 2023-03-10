from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from api import templates, _l, flash
from api.config.database import get_db

from api.models.user import User
from api.models.account import Bank
from api.models.provider import Provider

from api.schemas.base import MessageResponse
from api.schemas.user import UserCreate

from api.utils import auth

user = APIRouter()


@user.get("/", response_class=HTMLResponse, tags=["users"])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, **_l})


@user.get(
    "/dashboard",
    response_class=HTMLResponse,
    tags=["dashboard"],
    description="Retrieve all information needed for a dashboard information",
)
@auth.check_jwt_auth
async def dashboard(request: Request, db: Session = Depends(get_db)):
    # Get information for dashboard main view
    banks = Bank.get_total(db)
    providers = Provider.get_total(db)
    return templates.TemplateResponse(
        "main.html", {"request": request, "banks": banks, "providers": providers, **_l}
    )


@user.post(
    "/register",
    response_model=MessageResponse,
    status_code=200,
    tags=["users"],
    description="Endpoint to register new users to system",
)
async def register(user: UserCreate, request: Request, db: Session = Depends(get_db)):
    redirect_url = request.url_for("index")
    response = dict(redirect_to=redirect_url, message=_l.get("registration_success"))

    # Check if user is already registed
    user_exists = User.get_by_email(db=db, email=user.email)
    if user_exists:
        response.update(message=_l.get("user_registered"))
        flash(request, response.get("message"), "danger")
        return response

    # Register user
    User.create(db=db, user=user)
    flash(request, response["message"], "success")
    return response


@user.post(
    "/login",
    response_model=MessageResponse,
    status_code=200,
    tags=["users"],
    description="Log In an user in the system",
)
async def login(
    user: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    redirect_url = request.url_for("index")
    response = dict(redirect_to=redirect_url)

    # Verify the user credentials and generate a JWT token for session validation
    user_registered = User.get_by_email(db=db, email=user.email)
    if not user_registered:
        # User not registered
        response.update(message=_l.get("user_not_registered"))
        flash(request, response.get("message"), "danger")
    elif not user_registered.check_password(user.password):
        response.update(message=_l.get("invalid_password"))
        flash(request, response.get("message"), "danger")
    else:
        response["redirect_to"] = request.url_for("dashboard")
        token = auth.create_jwt_token(
            email=user_registered.email, id=user_registered.id
        )
        # Store the JWT token in the session
        request.session["token"] = token
        request.session["username"] = user.email
        response.update(message=_l.get("welcome"))
    return response


@user.get(
    "/logout",
    response_class=RedirectResponse,
    tags=["users"],
    description="Logout from system access",
)
async def logout(request: Request):
    redirect_url = request.url_for("index")
    request.session.pop("token", None)
    return RedirectResponse(redirect_url)
