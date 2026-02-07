from .db import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer, String, Enum, Date, ForeignKey,Text,Boolean, DateTime
from typing import Optional,List
from enum import Enum as PyEnum
from datetime import date, datetime

class StatusChoices(str, PyEnum):
    gold = 'gold'
    silver = 'silver'
    bronze = 'bronze'
    simple = 'simple'

class UserProfile(Base):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String,unique=True)
    email: Mapped[str] = mapped_column(String,unique=True)
    password: Mapped[str] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String,nullable=True)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices),default=StatusChoices.simple)
    data_registered: Mapped[date] = mapped_column(Date,default=date.today)

    user_review: Mapped[List['Review']] = relationship(back_populates='user',
                                                       cascade='all, delete-orphan')


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    category_image: Mapped[str] =mapped_column(String)
    category_name: Mapped[str] = mapped_column(String(50))

    subcategories: Mapped[List['SubCategory']] = relationship(back_populates='category',
                                                              cascade='all, delete-orphan')


class SubCategory(Base):
    __tablename__ = 'sub_category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    sub_category_name: Mapped[str] = mapped_column(String(50))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    sub_products: Mapped[List['Product']] = relationship(back_populates='subcategory',
                                                         cascade='all, delete-orphan')

    category: Mapped[Category] = relationship(Category, back_populates='subcategories')

class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    subcategory_id: Mapped[int] = mapped_column(ForeignKey('sub_category.id'))
    product_name: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column(Integer)
    article_number: Mapped[int] = mapped_column(Integer,unique=True)
    description: Mapped[str] = mapped_column(Text)
    video: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    product_type: Mapped[bool] = mapped_column(Boolean)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    images: Mapped[List['ProductImage']] = relationship(back_populates='product',
                                                        cascade='all, delete-orphan')

    product_review:Mapped[List['Review']] = relationship(back_populates='products',
                                                         cascade='all, delete-orphan')

    subcategory: Mapped[SubCategory] = relationship(back_populates='sub_products')


class ProductImage(Base):
    __tablename__ = 'product_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    image: Mapped[str] = mapped_column(String)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))

    product:Mapped[Product] = relationship(back_populates='images')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    text: Mapped[str] = mapped_column(Text)
    stars: Mapped[int] = mapped_column(Integer)
    created_date: Mapped[date] = mapped_column(Date, default=date.today)

    user: Mapped[UserProfile] = relationship(back_populates='user_review')
    products: Mapped[Product] = relationship(back_populates='product_review')






