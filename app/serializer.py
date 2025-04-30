from rest_framework import serializers
from app.models import *
from django.contrib.auth.models import User

## custom_serializer by post


class SubcategoryByCategoryIDserializer(serializers.ModelSerializer):
    class Meta:
        model = Sub_category
        fields = '__all__'
        read_only_fields = ('user','ub_category_name','image')


class ProductBySubcategoryIDserializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('user','product_name','product_price','product_description','color','size','brand')


# class searchProductserializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'
#         read_only_fields = ('use','product_name','product_price','product_description','color','size','brand')


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'product_name', 'product_price', 'product_description']


### api by ajax



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sub_category
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ('id','product_name', 'product_price')
        # fields = ('product_name','product_price')


class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    # product = ProductSerializer(read_only=True)
    class Meta:
        model = Product_Image
        fields = ('id','product','image')

class AddToCart(serializers.HyperlinkedModelSerializer):
    class Meta:
        models = Add_To_Cart
        fields = ('id', 'user', 'product', 'price', 'quantity', 'booking_date', 'delivery_date', 'status', 'shipping_address', 'payment_method')



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '_all_'
        read_only_fields =('id','booking_date','delivery_date','status','user','price')