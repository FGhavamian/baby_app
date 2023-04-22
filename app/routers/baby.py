from fastapi import APIRouter, status, HTTPException, Depends

from .. import schemas, oauth2
from app.database import cur, conn


router = APIRouter(prefix="/babies", tags=["babies"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BabyOut)
def create_baby(
    baby: schemas.BabyBase,
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    cur.execute(
        f"insert into babies (name, user_id) values ('{baby.name}', {current_user.id}) returning *;"
    )

    conn.commit()
    added_baby = cur.fetchone()

    return added_baby


@router.get("/{id}", response_model=schemas.BabyOut)
def get_baby(id: int, current_user: int = Depends(oauth2.get_current_user)):
    cur.execute(f"select * from babies where id = {id};")
    baby = cur.fetchone()
    baby = schemas.BabyOut(**baby)

    if not baby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"baby with id={id} not found"
        )

    if baby.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not authorized to see baby with id={id}",
        )

    return baby
