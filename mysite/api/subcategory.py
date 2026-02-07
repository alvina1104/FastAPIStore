from mysite.database.models import SubCategory
from mysite.database.shema import SubCategoryInputShema, SubCategoryOutShema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List

subcategory_router = APIRouter(prefix='/subcategory', tags=['SubCategory CRUD'])


# DB dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@subcategory_router.post('/', response_model=SubCategoryOutShema)
async def create_subcategory(subcategory_data: SubCategoryInputShema, db: Session = Depends(get_db)):
    # subcategory_data'ны колдонобуз
    subcategory_db = SubCategory(**subcategory_data.dict())
    db.add(subcategory_db)
    db.commit()
    db.refresh(subcategory_db)
    return subcategory_db


@subcategory_router.get('/', response_model=List[SubCategoryOutShema])
async def list_subcategory(db: Session = Depends(get_db)):
    return db.query(SubCategory).all()


@subcategory_router.get('/{subcategory_id}', response_model=SubCategoryOutShema)
async def detail_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    subcategory = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=404, detail='Мындай подкатегория жок')
    return subcategory


@subcategory_router.put('/{subcategory_id}', response_model=dict)
async def update_subcategory(subcategory_id: int, subcategory_data: SubCategoryInputShema,
                             db: Session = Depends(get_db)):
    # Биринчи базадан табабыз
    subcategory_db = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()

    if not subcategory_db:
        raise HTTPException(status_code=404, detail='Мындай подкатегория жок')

    # Маалыматтарды жаңыртуу
    for key, value in subcategory_data.dict().items():
        setattr(subcategory_db, key, value)

    db.commit()
    db.refresh(subcategory_db)
    return {'message': 'Подкатегория ийгиликтүү өзгөртүлдү'}



@subcategory_router.delete('/{subcategory_id}', response_model=dict)
async def delete_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    subcategory_db = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()

    if not subcategory_db:
        raise HTTPException(status_code=404, detail='Мындай подкатегория жок')

    db.delete(subcategory_db)
    db.commit()
    return {'message': 'Подкатегория өчүрүлдү'}