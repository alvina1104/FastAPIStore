from fastapi import APIRouter, HTTPException,Depends
from pyexpat.errors import messages

from mysite.database.db import SessionLocal
from mysite.database.models import UserProfile
from mysite.database.schema import UserProfileInputSchema,UserProfileOutSchema,UserLoginSchema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



auth_router = APIRouter(prefix='/auth',tags=['Auth'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@auth_router.post('/register/', response_model=dict)
async def register(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if user_db or email_db:
        raise HTTPException(detail='Мындай username же почта  бар экен',status_code=400)

    hash_password = get_password_hash(user.password)
    user_data = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        age=user.age,
        phone_number=user.phone_number,
        password=hash_password,

    )

    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {'massage':'Сиз регистрация болдунуз'}

@auth_router.post('/login/', response_model=dict)
async def login(user: UserLoginSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if not user_db or verify_password(user.password,user_db.password):
        raise HTTPException(detail='Сиз жазган маалымыт туура эмес',status_code=401)

    return {'messages':'Доступ бар'}







