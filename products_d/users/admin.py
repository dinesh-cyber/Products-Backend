from django.contrib import admin

# Register your models here.
from products_d.users.models import User, Product

admin.site.register([User, Product])