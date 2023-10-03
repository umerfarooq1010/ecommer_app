# Importing Python packages
import traceback
from passlib.hash import pbkdf2_sha256

# Importing FastAPI packages
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text


# Importing from project files
from core.database import database
from core.models import User
from auth.Token import create_access_token



# Router Object to Create Routes
router = APIRouter(
    tags=["Log In"]
)


# ---------------------------------------------------------------------------------------------------


@router.post('/login/', summary="Performs authentication")
async def log_in(request: OAuth2PasswordRequestForm = Depends()):
    """
        Performs authentication and returns the authentication token to keep the user
        logged in for longer time.

        Provide **Username** and **Password** to log in.

    """
    print("Calling log_in method")
    user_name=request.username.lower()
    select_query = User.select().where(User.c.username == user_name)
    select_result = await database.fetch_one(select_query)
    # if select_result:
    #     if not select_result.active:
    #         raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User is already registered but not activated")
    #

    if not select_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    if not pbkdf2_sha256.verify(request.password, select_result["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Password is incorrect")
    access_token = create_access_token(data={"sub": select_result["username"],
                                             "email": select_result["email"],
                                             "scopes": request.scopes,
                                             "id": select_result["id"]},
                                       token_type="access")

    return {"access_token": access_token, "token_type": "bearer"}

