from rest_framework import serializers

# import models here
from products_d.users.models import User, Product

class UserSeriaizer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = "__all__"

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "password"]


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"