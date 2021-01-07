from rest_framework.serializers import ModelSerializer
from billing.models import Products

class ProductSerializer(ModelSerializer):
    class Meta:
        model=Products
        fields=["product_name"]