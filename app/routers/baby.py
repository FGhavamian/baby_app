from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from .. import schemas, oauth2, crude
from app.database import get_db


router = APIRouter(prefix="/babies", tags=["babies"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Baby)
def create_baby(
    baby: schemas.BabyCreate,
    current_user: schemas.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    db_baby = crude.get_baby_by_name(db, current_user.id, baby.name)

    if db_baby:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You already have a baby named {baby.name}.",
        )

    return crude.create_baby(db, baby, current_user.id)


@router.get("/{id}", response_model=schemas.Baby)
def get_baby(
    id: int,
    current_user: schemas.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    db_baby = crude.get_baby(db, id)

    if not db_baby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"baby with id={id} not found"
        )

    if db_baby.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not authorized to see baby with id={id}",
        )

    return db_baby
