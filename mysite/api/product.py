from mysite.database.models import Product, SubCategory
from mysite.database.shema import ProductInputShema, ProductOutShema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List

product_router = APIRouter(prefix='/product', tags=['Product CRUD'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_router.post('/', response_model=ProductOutShema)
async def create_product(product_in: ProductInputShema, db: Session = Depends(get_db)):
    # 1. Подкатегория бар экенин текшерүү (ForeignKey катасын алдын алуу)
    subcategory = db.query(SubCategory).filter(SubCategory.id == product_in.subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=404, detail="Мындай подкатегория жок, алгач аны түзүңүз!")

    product_db = Product(**product_in.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.get('/', response_model=List[ProductOutShema])
async def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@product_router.get('/{product_id}', response_model=ProductOutShema)
async def detail_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Продукт табылган жок')
    return product


@product_router.put('/{product_id}', response_model=dict)
async def update_product(product_id: int, product_in: ProductInputShema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Продукт табылган жок')


    for key, value in product_in.dict().items():
        setattr(product_db, key, value)

    db.commit()
    db.refresh(product_db)
    return {'message': 'Продукт ийгиликтүү өзгөртүлдү'}


@product_router.delete('/{product_id}', response_model=dict)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Продукт табылган жок')

    db.delete(product_db)
    db.commit()
    return {'message': 'Продукт өчүрүлдү'}