from django.shortcuts import render
from .models import Product

#DRINKS PAGE
def drinks(request):
    products = Product.objects.filter(product_category = 'Drinks')
    print(products)
    params = {'product':products, 'range': range(len(products))}
    print(params)
    return render(request, 'products/drinks.html', params)

#CEREALS PAGE
def cereals(request):
    products = Product.objects.filter(product_category = 'Cereals')
    print(products)
    params = {'product':products, 'range': range(len(products))}
    print(params)
    return render(request, 'products/cereals.html', params)

#SNACKS PAGE
def snacks(request):
    products = Product.objects.filter(product_category = 'Snacks')
    print(products)
    params = {'product':products, 'range': range(len(products))}
    print(params)
    return render(request, 'products/snacks.html', params)

#DIARY PAGE
def diaryprod(request):
    products = Product.objects.filter(product_category = 'Diary')
    print(products)
    params = {'product':products, 'range': range(len(products))}
    print(params)
    return render(request, 'products/diaryprod.html', params)

#spices
def spices(request):
    products = Product.objects.filter(product_category = 'Spices')
    print(products)
    params = {'product':products, 'range': range(len(products))}
    print(params)
    return render(request, 'products/spices.html', params)
