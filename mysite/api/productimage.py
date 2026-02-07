from mysite.database.models import ProductImage, Product
from mysite.database.schema import ProductImageInputShema, ProductImageOutShema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List

product_image_router = APIRouter(prefix='/product-image', tags=['Product Image CRUD'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@product_image_router.post('/', response_model=ProductImageOutShema)
async def create_product_image(image_in: ProductImageInputShema, db: Session = Depends(get_db)):
    # 1. Продукт базада барбы текшеребиз
    product = db.query(Product).filter(Product.id == image_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Мындай продукт жок, алгач продукт түзүңүз!")


    image_db = ProductImage(**image_in.dict())
    db.add(image_db)
    db.commit()
    db.refresh(image_db)
    return image_db


@product_image_router.get('/', response_model=List[ProductImageOutShema])
async def list_product_images(db: Session = Depends(get_db)):
    return db.query(ProductImage).all()


@product_image_router.get('/{image_id}', response_model=ProductImageOutShema)
async def detail_product_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail='Сүрөт табылган жок')
    return image


@product_image_router.put('/{image_id}', response_model=dict)
async def update_product_image(image_id: int, image_in: ProductImageInputShema, db: Session = Depends(get_db)):
    image_db = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not image_db:
        raise HTTPException(status_code=404, detail='Сүрөт табылган жок')

    for key, value in image_in.dict().items():
        setattr(image_db, key, value)

    db.commit()
    db.refresh(image_db)
    return {'message': 'Сүрөт ийгиликтүү жаңыртылды'}


@product_image_router.delete('/{image_id}', response_model=dict)
async def delete_product_image(image_id: int, db: Session = Depends(get_db)):
    image_db = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not image_db:
        raise HTTPException(status_code=404, detail='Сүрөт табылган жок')

    db.delete(image_db)
    db.commit()
    return {'message': 'Сүрөт өчүрүлдү'}