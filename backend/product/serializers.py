from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','product_from', 'name', 'description', 'price', 'stock', 'image','image2','image3']
