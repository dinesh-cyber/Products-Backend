from django.urls import path

# import views here
from products_d.users.views import LoginAPI, RegisterAPI, ProductsAPI, ProductsUpdateAPI


# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Socialight API",
#         default_version="v1",
#         description="This is the api for socialight",
#         contact=openapi.Contact(email="vishnu.prasad@socialight.co.in"),
#         url=default_url
#     ),
#     url = default_url,
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
  path('login/', LoginAPI.as_view()),
  path('register/', RegisterAPI.as_view()),
  path('products/', ProductsAPI.as_view()),
  path('product/<product_id>', ProductsUpdateAPI.as_view())
]