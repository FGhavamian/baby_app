from typing import List, Dict

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from .. import schemas, oauth2, crude
from ..database import get_db
from ..core.amount_stats import compute_rolling_sum


router = APIRouter(prefix="/amounts", tags=["amounts"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Amount)
def add_amount(
    amount: int,
    baby_id: int,
    current_user: schemas.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    db_baby = crude.get_baby(db, baby_id)

    if not db_baby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"baby with id={baby_id} not found.",
        )

    if db_baby.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not authorized to add amounts for baby with id={baby_id}",
        )

    return crude.add_amount(db, amount, baby_id)


# TODO: CHECKOUT pandera library
# @router.get("/stats", response_model=List[schemas.AmountSum])
# def compute_sum_over_past_hours(
#     num_hours: int,
#     baby_id: int,
#     current_user: schemas.User = Depends(oauth2.get_current_user),
#     db: Session = Depends(get_db),
# ):
#     db_baby = crude.get_baby(db, baby_id)

#     if not db_baby:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"baby with id={baby_id} not found.",
#         )

#     if db_baby.user_id != current_user.id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail=f"You are not authorized to add amounts for baby with id={baby_id}",
#         )

#     amounts = crude.get_amounts(db, 1000, baby_id)

#     hours_sum = compute_rolling_sum(amounts, num_hours)

#     print(hours_sum)

#     return hours_sum


@router.get("/{n}", response_model=List[schemas.Amount])
def read_amounts(
    n: int,
    baby_id: int,
    current_user: schemas.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    db_baby = crude.get_baby(db, baby_id)

    if not db_baby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"baby with id={baby_id} not found.",
        )

    if db_baby.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not authorized to add amounts for baby with id={baby_id}",
        )

    return crude.get_amounts(db, n, baby_id)
