from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from .. import schemas, oauth2, crude
from ..database import get_db


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crude.get_user_by_email(db, user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

    return crude.create_user(db, user)


@router.get("/{id}", response_model=schemas.User)
def get_user(
    id: int,
    current_user: schemas.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not allowed to access other users data",
        )

    db_user = crude.get_user(db, id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id={id} not found"
        )

    return db_user
