from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    types_of_users = [
        ("admin", "admin"),
        ("manager", "manager"),
        ("staff", "staff"),
    ]
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=30)
    password = models.CharField(blank=False, null=False, max_length=255)
    phone = models.BigIntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    user_type = models.CharField(
        max_length=30, choices=types_of_users, default="staff"
    )

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user"


class Product(models.Model):
    title = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.IntegerField()
    publish = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    image = models.FileField(upload_to="products/")
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
