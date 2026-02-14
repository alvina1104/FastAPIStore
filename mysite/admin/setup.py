from fastapi import FastAPI
from .views import (UserProfileAdmin,RefreshTokenAdmin, CategoryAdmin, SubCategoryAdmin,
                    ProductAdmin,ProductImageAdmin, ReviewAdmin)
from sqladmin import Admin
from mysite.database.db import engine



def setup_admin(mysite: FastAPI):
    admin = Admin(mysite, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(RefreshTokenAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(SubCategoryAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(ProductImageAdmin)
    admin.add_view(ReviewAdmin)





