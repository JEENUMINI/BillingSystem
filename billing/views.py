from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from billing.forms import ProductsForm,PurchaseForm
from billing.models import Products,Purchase

# Create your views here.

class AddProduct(TemplateView):
    form_class=ProductsForm()
    template_name = "billing/add_product.html"
    context={}

    def get(self, request, *args, **kwargs):
        form=ProductsForm()
        self.context["form"]=form
        return render(request,self.template_name,self.context)

    def post(self, request, *args, **kwargs):
        form=ProductsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listproduct")

class ListProduct(TemplateView):
    model=Products
    template_name = "billing/list_product.html"
    context={}

    def get_query_set(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        self.context["products"]=self.get_query_set()
        return render(request,self.template_name,self.context)

class EditProduct(TemplateView):
    model=Products
    template_name = "billing/edit_product.html"
    context = {}

    def get_query_set(self,id):
        return self.model.objects.get(id=id)

    def get(self, request, *args, **kwargs):
        products=self.get_query_set(kwargs.get("pk"))
        form=ProductsForm(instance=products)
        self.context["form"]=form
        return render(request,self.template_name,self.context)

    def post(self, request, *args, **kwargs):
        products = self.get_query_set(kwargs.get("pk"))
        form=ProductsForm(instance=products,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("listproduct")

class DeleteProduct(TemplateView):
    model=Products

    def get_query_set(self,id):
        return self.model.objects.get(id=id)

    def get(self, request, *args, **kwargs):
        products=self.get_query_set(kwargs.get("pk"))
        products.delete()
        return redirect("listproduct")

class AddPurchase(TemplateView):
    form_class=PurchaseForm()
    template_name = "billing/add_purchase.html"
    context={}

    def get(self, request, *args, **kwargs):
        form = PurchaseForm()
        self.context["form"]=form
        return render(request,self.template_name,self.context)

    def post(self, request, *args, **kwargs):
        form=PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listpurchases")

class ListPurchases(TemplateView):
    model=Purchase
    template_name = "billing/list_purchases.html"
    context={}

    def get_query_set(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        self.context["purchases"]=self.get_query_set()
        return render(request,self.template_name,self.context)

class EditPurchase(TemplateView):
    model=Purchase
    template_name = "billing/edit_purchase.html"
    context = {}

    def get_query_set(self,id):
        return self.model.objects.get(id=id)

    def get(self, request, *args, **kwargs):
        purchases=self.get_query_set(kwargs.get("pk"))
        form=PurchaseForm(instance=purchases)
        self.context["form"]=form
        return render(request,self.template_name,self.context)

    def post(self, request, *args, **kwargs):
        purchases = self.get_query_set(kwargs.get("pk"))
        form=PurchaseForm(instance=purchases,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("listpurchases")
        else:
            self.context["form"] = form
            return render(request, self.template_name, self.context)

class DeletePurchase(TemplateView):
    model=Purchase

    def get_query_set(self,id):
        return self.model.objects.get(id=id)

    def get(self, request, *args, **kwargs):
        purchases=self.get_query_set(kwargs.get("pk"))
        purchases.delete()
        return redirect("listpurchases")



