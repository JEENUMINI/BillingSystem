"""BillingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from billing.views import AddProduct,ListProduct,EditProduct,DeleteProduct,AddPurchase,ListPurchases,EditPurchase,DeletePurchase

urlpatterns = [

path('addproduct',AddProduct.as_view(),name="addproduct"),
path('listproduct',ListProduct.as_view(),name="listproduct"),
path('editproduct/<int:pk>',EditProduct.as_view(),name="editproduct"),
path('delete/<int:pk>',DeleteProduct.as_view(),name="delete"),
path('addpurchase',AddPurchase.as_view(),name="addpurchase"),
path('listpurchases',ListPurchases.as_view(),name="listpurchases"),
path('editpurchase/<int:pk>',EditPurchase.as_view(),name="editpurchase"),
path('deletepurchase/<int:pk>',DeletePurchase.as_view(),name="deletepurchase"),
]
