from django.db.models import Sum
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from billing.forms import ProductsForm,PurchaseForm,OrderForm,OrderLinesForm
from billing.models import Products,Purchase,Order,OrderLines

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

class OrderView(TemplateView):
    model=Order
    template_name = "billing/order.html"
    context={}

    def get(self, request, *args, **kwargs):
        orders=Order.objects.all().last()
        billnumber=int(orders.billnumber)
        billnumber+=1
        billnumber=str(billnumber)
        form=OrderForm(initial={"billnumber":billnumber})
        self.context["form"]=form
        return render(request,self.template_name,self.context)

    def post(self, request, *args, **kwargs):
        form=OrderForm(request.POST)
        if form.is_valid():
            billnum=form.cleaned_data.get("billnumber")
            form.save()
            return redirect("orderlines",billno=billnum)
        else:
            self.context["form"]=form
            return render(request,self.template_name,self.context)

class OrderLinesView(TemplateView):
    model=OrderLines
    template_name = "billing/orderlines.html"
    context={}
    def get(self, request, *args, **kwargs):
        billnum=kwargs.get("billno")
        self.context["billnumber"] = billnum
        print(billnum)
        bill=Order.objects.get(billnumber=billnum)
        form=OrderLinesForm(initial={"bill_number":bill})
        self.context["form"]=form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form=OrderLinesForm(request.POST)
        if form.is_valid():
            billnum = kwargs.get("billno")
            product_name = form.cleaned_data.get("product_name")
            billnum=form.cleaned_data.get("bill_number")
            product_qty=form.cleaned_data.get("product_qty")
            getpdtname=Products.objects.get(product_name=product_name)
            products = Purchase.objects.get(product__product_name=product_name)
            qty=products.qty
            sellingprice=products.selling_price
            amount=product_qty*sellingprice
            balanceqty=qty-product_qty
            products.qty=balanceqty
            products.save()
            self.context["products"] = products
            bill = Order.objects.get(billnumber=billnum)
            form = OrderLinesForm(initial={"bill_number": bill})
            self.context["form"] = form
            orderlines=OrderLines(bill_number=bill,product_name=getpdtname,product_qty=product_qty,amount=amount)
            orderlines.save()
            total=OrderLines.objects.filter(bill_number=bill).aggregate(Sum('amount'))
            self.context["total"] = total
            bill.bill_total=total
            # print(bill.bill_total["amount__sum"])
            Order.objects.filter(billnumber=billnum).update(bill_total= bill.bill_total["amount__sum"])
            orderlinesdata=OrderLines.objects.filter(bill_number=bill)
            self.context["orderlinesdata"]=orderlinesdata
            return render(request, self.template_name, self.context)
        else:
            self.context["form"] = form
            return render(request, self.template_name, self.context)

class BillGenerate(TemplateView):
    model=OrderLines
    template_name = "billing/bill_generate.html"
    context={}
    def get_object(self,id):
        return self.model.objects.get(bill_number=id)

    def get(self, request, *args, **kwargs):
        billnum=kwargs.get("billno")
        print(billnum)
        bill=Order.objects.get(billnumber=billnum)
        self.context["orderdata"]=bill
        billitems=self.model.objects.values_list("bill_number").last()
        getallitems=self.model.objects.filter(bill_number=billitems)
        self.context["getallitems"] = getallitems
        return render(request,self.template_name,self.context)

class View_ToatlBill(TemplateView):
    model=Order
    template_name = "billing/bill_total_views.html"
    context={}
    def get_object(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        allval=self.get_object()
        self.context["forms"]=allval
        return render(request,self.template_name,self.context)
    #
    # def post(self, request, *args, **kwargs):
    #     form = OrderForm(request.POST)
    #     if form.is_valid():
    #         billnum = form.cleaned_data.get("billnumber")
    #         return redirect("viewbilldetails", billno=billnum)
    #     else:
    #         self.context["form"] = form
    #         return render(request, self.template_name, self.context)





