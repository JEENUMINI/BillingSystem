from django import forms
from django.forms import ModelForm
from billing.models import Products,Purchase

class ProductsForm(ModelForm):
    class Meta:
        model=Products
        fields="__all__"

class PurchaseForm(ModelForm):
    class Meta:
        model=Purchase
        fields=["product","qty","purchase_price","selling_price"]
