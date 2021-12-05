from django.urls import path

# import views here
from products_d.users.views import LoginAPI, RegisterAPI, ProductsAPI, ProductsUpdateAPI

urlpatterns = [
  path('login/', LoginAPI.as_view()),
  path('register/', RegisterAPI.as_view()),
  path('products/', ProductsAPI.as_view()),
  path('product/<product_id>', ProductsUpdateAPI.as_view())
]