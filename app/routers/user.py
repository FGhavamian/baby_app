from fastapi import APIRouter, status, HTTPException, Depends

from .. import schemas, utils, oauth2
from ..database import cur, conn


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate):
    user.password = utils.hash(user.password)

    cur.execute(
        f"insert into users (email, password) values ('{user.email}', '{user.password}') returning *;"
    )

    conn.commit()
    added_user = cur.fetchone()

    return added_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, current_user: int = Depends(oauth2.get_current_user)):
    cur.execute(f"select * from users where id = {id};")

    user = cur.fetchone()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id={id} not found"
        )

    return user
