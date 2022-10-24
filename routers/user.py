from http.client import HTTPException
from fastapi import APIRouter, Request, Depends, status
from fastapi.templating import Jinja2Templates
from libs.models import User
from libs.hashing import Hasher
from sqlalchemy.orm import Session
from libs.database import get_db
from sqlalchemy.exc import IntegrityError
from routers.login import oauth2_scheme
from configparser import ConfigParser
from jose import jwt

config = ConfigParser()
config.read("config/config.ini")


router = APIRouter()
templates = Jinja2Templates(directory="templates")
hasher = Hasher()


@router.get('/userinfo', tags=['user'])
def user_info(request: Request, token:str=Depends(oauth2_scheme)):
    """
    test page with OAuth2 authentication
    """
    return templates.TemplateResponse("userinfo.html",{"request":request})

# @router.get("/login", tags=['user'])
# def login_page(request: Request):
#     """
#     login page
#     """
#     return templates.TemplateResponse("login.html", {"request": request})


# @router.post("/login", tags=['user'])
# async def login_user(request:Request, db:Session=Depends(get_db), token:str=Depends(oauth2_scheme)):
#     """
#     login user
#     """
#     errors = []
#     try:
#         payload = jwt.decode(token, config.get("security", "jwt_secret_key"), algorithm=config.get("security", "algorithm"))
#         username = payload.get("sub")
#         if username is None:
#             errors.append("Unable to verify credentials")
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details="Unable to verify credentials")

#         user = db.query(User).filter(User.name==username).first()
#         if user is None:
#             errors.append("User not found")
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details="User not found")

#     except Exception as e:
#         errors.append("Unable to verify credentials")
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details="Unable to verify credentials")
    
#     if errors:
#         for error in errors:
#             print(error)
#         return templates.TemplateResponse("home.html", {"request": request, "errors": errors})

#     user = await request.form()
#     username = user.get('username')
#     password = hasher.hash_password(user.get('password'))
#     authenticator = db.query(User).filter(User.name==username and User.password==password).first()
#     if authenticator:
#         return templates.TemplateResponse("userinfo.html", {"request": request})
#     return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})

@router.get("/register", tags=["user"])
def registration(request: Request):
    """
    registration page
    """
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", tags=['user'])
async def register_user(request: Request, db: Session=Depends(get_db)):
    """
    new user register function.
    """
    form = await request.form()
    username = form.get("username")
    email = form.get("email")
    password = form.get("password")
    confirm_password = form.get("confirmpassword")
    
    errors = []

    if len(password) < 4:
        errors.append("Password must be less than 4 characters")
        print(errors)
    if password != confirm_password:
        errors.append("Retyped password is not the same as password")
    if errors:
        for error in errors:
            print(error)
        return templates.TemplateResponse("register.html", {"request": request, "errors": errors})
    user = User(name=username, email=email, password=hasher.hash_password(password))
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return templates.TemplateResponse("home.html", {"request": request})
    except IntegrityError:
        errors.append("Username or email already exists")
        print(errors)
        return templates.TemplateResponse("register.html", {"request": request, "errors": errors})



