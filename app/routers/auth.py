from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import schemas, oauth2, utils
from ..database import cur


router = APIRouter(tags=["authentication"])


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    cur.execute(f"select * from users where email = '{user_credentials.username}'")
    user = cur.fetchone()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not utils.verify(user_credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": user["id"]})

    return {"access_token": access_token, "token_type": "bearer"}
