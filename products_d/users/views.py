from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Q

# import serializers here
from products_d.users.serializers import UserSeriaizer, ProductsSerializer, LoginSerializer

# import models here
from products_d.users.models import Product, User

# Create your views here
class RegisterAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = UserSeriaizer(data=data)
        if serializer.is_valid():
            obj = serializer.save()
            obj.set_password(data.get("password"))
            obj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(**request.data)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                user = User.objects.get(id=user.id)
                data = UserSeriaizer(user).data
                return Response(
                    {
                        "token": token.key,
                        "user": data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": "Invalid authentication credentials",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductsAPI(APIView):

    def get(self, request):
        if request.user.user_type != "staff":
            products = Product.objects.filter(Q(publish=True) & Q(is_active=True))
            serializer = ProductsSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "You don't have permission to this api"},
                status=status.HTTP_400_BAD_REQUEST
            ) 

    def post(self, request):
        if request.user.user_type == "admin":
            data = request.data
            data['created_by'] = request.user.id
            serializer = ProductsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"message": "You don't have permission to this api"},
                status=status.HTTP_400_BAD_REQUEST
            ) 

class ProductsUpdateAPI(APIView):
    def put(self, request, product_id):
        if request.user.user_type != "staff":
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"message": "Invalid product Id"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = request.data
            serializer = ProductsSerializer(instance=product, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "You don't have permission to this api"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, product_id):
        if request.user.user_type != "staff":
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"message": "Invalid product Id"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # make product active false when admin or manager deletes products
            product.is_active = False
            product.save()
            serializer = ProductsSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"message": "You don't have permission to this api"},
            status=status.HTTP_400_BAD_REQUEST
        )