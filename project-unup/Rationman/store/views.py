from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import *
import json

def home(request):
    return render(request, 'store/home.html')

#REGISTRATION

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created successfully!. Please login to continue')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'store/register.html',{'form':form})

@login_required
def profile(request):
    return render(request, 'store/profile.html', {'title': 'My Account'})

#CATEGORIES
@login_required
def category(request):
    return render(request,'store/category.html',{'title': 'Categories'})

#PRODUCTS
def drinks(request):
    products = Product.objects.filter(product_category = 'Drinks')
    params = {'product':products, 'range': range(len(products))}
    return render(request, 'store/drinks.html', params)

#CEREALS PAGE
def cereals(request):
    products = Product.objects.filter(product_category = 'Cereals')
    params = {'product':products, 'range': range(len(products))}
    return render(request, 'store/cereals.html', params)

#SNACKS PAGE
def snacks(request):
    products = Product.objects.filter(product_category = 'Snacks')
    params = {'product':products, 'range': range(len(products))}
    return render(request, 'store/snacks.html', params)

#DIARY PAGE
def diaryprod(request):
    products = Product.objects.filter(product_category = 'Diary Products')
    params = {'product':products, 'range': range(len(products))}
    return render(request, 'store/diaryprod.html', params)

#spices
def spices(request):
    products = Product.objects.filter(product_category = 'Spices')
    params = {'product':products, 'range': range(len(products))}
    return render(request, 'store/spices.html', params)


#search
def search(request):
    query = request.GET['query']
    if len(query)>100 or len(query) == 0:
        products = Product.objects.none()
    else:
        product_name = Product.objects.filter(product_name__icontains = query)
        product_category = Product.objects.filter(product_category__icontains = query)
        products = product_name.union(product_category)

    if products.count() == 0:
        messages.warning(request, f'No search results found. Please refine your Queryset')
    params = {"product": products, "query": query}
    return render(request, 'store/search.html',params)


def trolley(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
    context = {'items':items, 'order':order}
    return render(request, 'store/trolley.html',context)

#UPDATEITEMS

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("productId: ", productId)
    print("Action: ", action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    print(orderItem.product)
    print(orderItem.order)
    print(orderItem.quantity)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    print(orderItem.quantity)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)