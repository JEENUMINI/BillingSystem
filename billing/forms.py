from random import choices

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

class OrderLinesForm(forms.Form):
    bill_number=forms.CharField()
    queryset=Purchase.objects.all().values_list('product__product_name',flat=True)
    choices=[(name, name) for name in queryset]
    product_name=forms.ChoiceField(choices=choices,required=False,widget=forms.Select())
    product_qty=forms.IntegerField()

    # class Meta:
    #     model = OrderLines
    #     fields = ["bill_number","product_name","product_qty"]
