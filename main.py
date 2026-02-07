from itertools import product

from fastapi import FastAPI
from mysite.api import user, category, subcategory,product,productimage,review,auth
import uvicorn

shop_app = FastAPI(title="Shop API")
shop_app.include_router(user.user_router)
shop_app.include_router(category.category_router)
shop_app.include_router(subcategory.subcategory_router)
shop_app.include_router(product.product_router)
shop_app.include_router(productimage.product_image_router)
shop_app.include_router(review.review_router)
shop_app.include_router(auth.auth_router)

if __name__ == "__main__":
    uvicorn.run(shop_app, host="127.0.0.1", port=8001)
