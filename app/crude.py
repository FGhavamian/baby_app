from sqlalchemy.orm import Session
import pandas as pd

from . import models, schemas, utils


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    user.password = utils.hash(user.password)
    db_user = models.Users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_baby(db: Session, baby_id: int):
    return db.query(models.Babies).filter(models.Babies.id == baby_id).first()


def get_baby_by_name(db: Session, user_id: int, baby_name: str):
    return (
        db.query(models.Babies)
        .filter(models.Babies.user_id == user_id)
        .filter(models.Babies.name == baby_name)
        .first()
    )


def create_baby(db: Session, baby: schemas.BabyCreate, user_id: int):
    db_baby = models.Babies(**baby.dict(), user_id=user_id)
    db.add(db_baby)
    db.commit()
    db.refresh(db_baby)
    return db_baby


def add_amount(db: Session, amount: int, baby_id: int):
    db_amount = models.Amounts(value=amount, baby_id=baby_id)
    db.add(db_amount)
    db.commit()
    db.refresh(db_amount)
    return db_amount


def get_amounts(db: Session, n: int, baby_id: int):
    return (
        db.query(models.Amounts)
        .filter(models.Amounts.baby_id == baby_id)
        .order_by(models.Amounts.created_at.desc())
        .limit(n)
        .all()
    )
