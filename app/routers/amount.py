from typing import List, Dict

from fastapi import APIRouter, status, HTTPException, Depends

from .. import schemas, oauth2
from ..database import cur, conn
from ..core.amount_stats import compute_rolling_sum


router = APIRouter(prefix="/amounts", tags=["amounts"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AmountOut)
def add_amount(
    amount: int,
    baby_id: int,
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    cur.execute(f"select * from babies where id = {baby_id}")
    baby = cur.fetchone()

    if not baby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"baby with id={baby_id} not found.",
        )

    baby = schemas.BabyOut(**baby)

    if baby.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not authorized to add amounts for baby with id={baby_id}",
        )

    cur.execute(
        f"""
        insert into amounts (value, baby_id)
        values ({amount}, {baby_id})
        returning *;
    """
    )
    conn.commit()
    added_amount = cur.fetchone()

    return added_amount


@router.get("/stats", response_model=Dict)
def compute_sum_over_past_hours(
    num_hours: int,
    baby_id: int,
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    if not baby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"baby with id={baby_id} not found.",
        )

    baby = schemas.BabyOut(**baby)

    if baby.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not authorized to measure statistics for baby with id={baby_id}",
        )

    cur.execute(
        f"""
        select * 
        from amounts
        where baby_id = {baby_id};"""
    )
    amounts = cur.fetchall()

    hours_sum = compute_rolling_sum(amounts, num_hours)

    return hours_sum.to_dict()


@router.get("/{n}", response_model=List[schemas.AmountOut])
def read_amounts(
    n: int,
    baby_id: int,
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    cur.execute(f"select * from babies where id = {baby_id}")
    baby = cur.fetchone()

    if not baby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"baby with id={baby_id} not found.",
        )

    baby = schemas.BabyOut(**baby)

    if baby.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not authorized to add amounts for baby with id={baby_id}",
        )

    cur.execute(
        f"""
        select * 
        from amounts 
        where baby_id = {baby_id} 
        order by created_at desc 
        limit {n};"""
    )
    amounts = cur.fetchall()

    return amounts
