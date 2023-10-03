# Importing Python packages
from datetime import datetime, timedelta
from databases import Database


from jose import jwt, JWTError
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from api_parameters import ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
# Importing from project files
from core.models import User
from core.database import get_database

# ---------------------------------------------------------------------------------------------------


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, token_type: str) -> str:
    to_encode = data.copy()
    if token_type == "access":
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(token: str = Depends(oauth2_scheme), database:Database=Depends(get_database)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        userid: str = payload.get("id")
        email: str = payload.get("email")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    query = User.select().where(User.c.id == userid, User.c.email == email)
    result = await database.fetch_one(query)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {**result, "disabled": False}

