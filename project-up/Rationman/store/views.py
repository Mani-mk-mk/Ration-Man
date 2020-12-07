from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import *
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
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

#TROLLEY PAGE
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

#REMINDER
def reminder(request):
#    if request.method == 'POST':
#        form = UserRegisterForm(request.POST)
#        if form.is_valid():
#            form.save()
#            username = form.cleaned_data.get('username')
#            messages.success(request, f'Your account has been created successfully!. Please login to continue')
#            return redirect('login')

    return render(request, 'store/reminder.html')

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


def lists(request):
    if request.user.is_authenticated:
        customer = request.user.customer

        lists, created = List.objects.get_or_create(customer=customer, used=False)
        items = lists.listitem_set.all()
    else:
        items = []
    context = {'items':items}
    return render(request, 'store/list.html',context)


def updateList(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("productId: ", productId)
    print("Action: ", action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    list, created = List.objects.get_or_create(customer=customer, used=False)

    listItem, created = ListItem.objects.get_or_create(list=list, product=product)
    print(listItem.product)
    print(listItem.list)
    print(listItem.quantity)

    if action == 'plus':
        listItem.quantity = (listItem.quantity + 1)

    elif action == 'minus':
        listItem.quantity = (listItem.quantity - 1)
    print(listItem.quantity)
    listItem.save()
    if listItem.quantity <= 0:
        listItem.delete()
    return JsonResponse('Item was added', safe=False)


#ADDING ITEMS INTO CART

def checkout_amazon(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
    context = {'items':items, 'order':order}
    driver = webdriver.Chrome(ChromeDriverManager().install())
    products = OrderItem.objects.all()
    for product in products:
        url = product.product.product_amazon_url
        if url == "empty":
            continue
        driver.get(url)
        try:
            button = driver.find_element_by_id('add-to-cart-button')
            button.click()
            time.sleep(2)
        except:
            try:
                button = driver.find_element_by_id('buybox-see-all-buying-choices-announce')
                button.click()
                button = driver.find_element_by_class_name('a-button-input')
                button.click()
                time.sleep(2)
            except:
                print("NO BUTTON FOUND MAYBE CURRENTLY UNAVAILABLE")
        
    time.sleep(120)
    driver.close()
    return render(request, 'store/trolley.html',context)


def checkout_flipkart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
    context = {'items':items, 'order':order}
    driver = webdriver.Chrome(ChromeDriverManager().install())

    products = OrderItem.objects.all()
    #SPECIALLY DESIGNED LOGIC FOR FLIPKART
    driver.get('https://flipkart.com/')

    user = driver.find_element_by_class_name('VJZDxU')
    user.clear()
    user.send_keys("9284160249")

    passd =  driver.find_element_by_xpath("//input[@type='password']")
    passd.clear()
    passd.send_keys("mani1234")


    button = driver.find_element_by_xpath("//button[@class='_2KpZ6l _2HKlqd _3AWRsL']")
    button.click()

    print('User Successfully Logined In')

    time.sleep(3)
    for product in products:
        url = product.product.product_flipkart_url
        if url == "empty":
            continue
        driver.get(url)
        try:
            button = driver.find_element_by_class_name('_2KpZ6l')
            button.click()
            time.sleep(2)
            #for i in range(0, len(product.quantity)):
               # button = driver.find_element_by_class_name('_1vDsnQ')
               # button.click()
        except:
            print()
            print("NO BUTTON FOUND MAYBE THE PRODUCT IS CURRENTLY UNAVAILABLE")
    time.sleep(120)
    driver.close()
    return render(request, 'store/trolley.html',context)


def checkout_bigb(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
    context = {'items':items, 'order':order}
    driver = webdriver.Chrome(ChromeDriverManager().install())
    #chrome_options = webdriver.ChromeOptions(); 
    #chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
    #driver = webdriver.Chrome(options=chrome_options);
    products = OrderItem.objects.all()
    for product in products:
        url = product.product.product_bigb_url
        if url == "empty":
            continue
        driver.get(url)
        try:
            button = driver.find_element_by_class_name('Cs6YO')
            button.click()
            time.sleep(5)
            #try:
                #for i in range(0, len(product.orderitem.quantity)):
                    #button = driver.find_element_by_class_name('_1aJzw')
                    #button.click()
            #except:
                #print("CANT INCREASE")
        except:
            print()
            print("NO BUTTON FOUND MAYBE THE PRODUCT IS CURRENTLY UNAVAILABLE")
    time.sleep(120)
    driver.close()
    return render(request, 'store/trolley.html',context)

#ITEMS ADDED INTO CART