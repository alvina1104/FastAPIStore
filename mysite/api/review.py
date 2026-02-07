from mysite.database.models import Review, Product, UserProfile
from mysite.database.schema import ReviewInputShema, ReviewOutShema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List

review_router = APIRouter(prefix='/review', tags=['Review CRUD'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@review_router.post('/', response_model=ReviewOutShema)
async def create_review(review_in: ReviewInputShema, db: Session = Depends(get_db)):

    user = db.query(UserProfile).filter(UserProfile.id == review_in.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Мындай колдонуучу табылган жок!")


    product = db.query(Product).filter(Product.id == review_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Мындай продукт табылган жок!")

    # 3. Сактоо
    review_db = Review(**review_in.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.get('/', response_model=List[ReviewOutShema])
async def list_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@review_router.get('/{review_id}', response_model=ReviewOutShema)
async def detail_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail='Сын-пикир табылган жок')
    return review


@review_router.put('/{review_id}', response_model=dict)
async def update_review(review_id: int, review_in: ReviewInputShema, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail='Сын-пикир табылган жок')

    for key, value in review_in.dict().items():
        setattr(review_db, key, value)

    db.commit()
    db.refresh(review_db)
    return {'message': 'Сын-пикир ийгиликтүү жаңыртылды'}


@review_router.delete('/{review_id}', response_model=dict)
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail='Сын-пикир табылган жок')

    db.delete(review_db)
    db.commit()
    return {'message': 'Сын-пикир өчүрүлдү'}