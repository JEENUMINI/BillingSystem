from django import forms
from django.forms import ModelForm
from billing.models import Products,Purchase,Order,OrderLines

class ProductsForm(ModelForm):
    class Meta:
        model=Products
        fields="__all__"

class PurchaseForm(ModelForm):
    class Meta:
        model=Purchase
        fields=["product","qty","purchase_price","selling_price"]

class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields=["billnumber","customer_name","phone_number"]

class OrderLinesForm(ModelForm):
    # bill_number=forms.CharField(max_length=12)
    class Meta:
        model=OrderLines
        fields=["bill_number","product_name","product_qty"]
