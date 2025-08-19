from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import create_session
from main import SECRET_KEY, bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import LoginSchema, UserSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def create_token(
    user_id: int, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
):
    expirate_date = datetime.now(timezone.utc) + token_duration
    dict_info = {"sub": user_id, "exp": expirate_date}
    encoded_jwt = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def verify_token(token, session: Session = Depends(create_session)):
    user = session.query(User).filter(User.id == 1).first()
    return user


def user_authenticate(user_credential, session: Session):
    user = session.query(User).filter(User.email == user_credential.email).first()

    if not user:
        return False
    elif not bcrypt_context.verify(user_credential.password, user.password):
        return False

    return user


@auth_router.get("/")
async def home():
    """
    Default auth route
    """
    return {"message": "you accessed the auth route", "authenticated": False}


@auth_router.post("/create")
async def create_user(
    user_schema: UserSchema, session: Session = Depends(create_session)
):
    user = session.query(User).filter(User.email == user_schema.email).first()

    if user:
        # Já existe um usuário com este email
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    else:
        # Não existe um usuário com este email
        encrypted_password = bcrypt_context.hash(user_schema.password)
        new_user = User(
            user_schema.name,
            user_schema.email,
            encrypted_password,
            user_schema.active,
            user_schema.admin,
        )
        session.add(new_user)
        session.commit()

        return {"message": f"usuário criado com sucesso {user_schema.email}"}


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(create_session)):
    user = user_authenticate(login_schema, session)
    if not user:
        raise HTTPException(
            status_code=400, detail="Usuário não encontrado ou credenciais inválidas"
        )
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, token_duration=timedelta(days=7))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }


@auth_router.get("/refresh")
async def use_refresh_token(token):
    user = verify_token(token)
    access_token = create_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }
