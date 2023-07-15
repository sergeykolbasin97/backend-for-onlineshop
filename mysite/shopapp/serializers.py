from .models import Order
from .models import Product
from rest_framework import serializers


class ProductSerialize(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'pk', 'name', 'price', 'description', 'discount', 'created_at', 'archived', 'preview'


class OrderSerialize(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = 'pk', 'delivery_address', 'promocode', 'created_at', 'user', 'products'

