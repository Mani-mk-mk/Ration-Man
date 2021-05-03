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
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from webdriver_manager.chrome import ChromeDriverManager
import json

items = {}
monthly_items = {}
party_items = {}
def home(request):
    products = Product.objects.filter(product_category = 'Drinks')
    context = {'product': products, 'range': range(0,3)}
    return render(request, 'store/home.html',context)

def yourorder(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

        prev, created = PreviousOrder.objects.get_or_create(customer=customer, used=False)
        previtem = prev.previousorderitem_set.all()
    else:
        items = []
        previtem = []
    context = {'items':items, 'order':order, 'previtem':previtem}

    return render(request, 'store/yourorder.html',context)

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

        lists, created = List.objects.get_or_create(customer=customer, used=False)
        listitems = lists.listitem_set.all()

    else:
        items = []
        listitems = []
        order = {'get_cart_items':0, 'get_cart_total':0}
    context = {'items':items, 'order':order, 'listitems':listitems}
    return render(request, 'store/trolley.html',context)

#REMINDER
def reminder(request):
    waiting_time = int(request.POST.get("time",False))
    print(waiting_time)
    if waiting_time != 0:
        template = render_to_string('store/template.html', {'name': request.user.username})
        time.sleep(waiting_time)
        email = EmailMessage(
            "Knock knock! Ration-Man here!!",
            template,
            settings.EMAIL_HOST_USER,
            [request.user.email],
        )
        email.fail_silently=False
        email.send()

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
        product = Product.objects.all()
        lists, created = List.objects.get_or_create(customer=customer, used=False)
        items = lists.listitem_set.all()

    else:
        items = []
    context = {'items':items, 'product':product}
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
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)


    listItem, created = ListItem.objects.get_or_create(list=list, product=product)
    print(listItem.product)
    print(listItem.list)
    print(listItem.quantity)

    if action == 'add':
        listItem.quantity = (listItem.quantity + 1)
        
    elif action == 'remove':
        listItem.quantity = (listItem.quantity - 1)
    print(listItem.quantity)
    listItem.save()
    orderItem.delete()
    # if listItem.quantity >= 1:
    items[productId] = listItem.quantity
    if items[productId] <= 0:
        del items[productId]
    print(items)

    if listItem.quantity <= 0:
        listItem.delete()

    return JsonResponse('Item was added', safe=False)

def monthly(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.all()
        monthly, created = Monthly.objects.get_or_create(customer=customer, used=False)
        items = monthly.monthlyitem_set.all()

    else:
        items = []
    context = {'items':items, 'product':product}
    return render(request, 'store/monthly.html',context)

def updateMonthly(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("productId: ", productId)
    print("Action: ", action)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    monthly, created = Monthly.objects.get_or_create(customer=customer, used=False)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)


    monthlyItem, created = MonthlyItem.objects.get_or_create(monthly=monthly, product=product)
    print(monthlyItem.product)
    print(monthlyItem.monthly)
    print(monthlyItem.quantity)

    if action == 'plus':
        monthlyItem.quantity = (monthlyItem.quantity + 1)
        
    elif action == 'minus':
        monthlyItem.quantity = (monthlyItem.quantity - 1)
        if monthlyItem.quantity <= 0:
            monthlyItem.delete()    

    print(monthlyItem.quantity)
    monthlyItem.save()
    orderItem.delete()
    # if listItem.quantity >= 1:
    monthly_items[productId] = monthlyItem.quantity
    if monthly_items[productId] <= 0:
        del monthly_items[productId]
    print(monthly_items)

    if monthlyItem.quantity <= 0:
        monthlyItem.delete()

    return JsonResponse('Item was added', safe=False)

def party(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.all()
        party, created = Party.objects.get_or_create(customer=customer, used=False)
        items = party.partyitem_set.all()

    else:
        items = []
    context = {'items':items, 'product':product}
    return render(request, 'store/party.html',context)

def updateParty(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("productId: ", productId)
    print("Action: ", action)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    party, created = Party.objects.get_or_create(customer=customer, used=False)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)


    partyItem, created = PartyItem.objects.get_or_create(party=party, product=product)
    print(partyItem.product)
    print(partyItem.party)
    print(partyItem.quantity)

    if action == 'plus':
        partyItem.quantity = (partyItem.quantity + 1)
        
    elif action == 'minus':
        partyItem.quantity = (partyItem.quantity - 2)
    print(partyItem.quantity)
    partyItem.save()
    orderItem.delete()
    # if listItem.quantity >= 1:
    party_items[productId] = partyItem.quantity
    if party_items[productId] <= 0:
        del party_items[productId]
    print(party_items)

    if partyItem.quantity <= 0:
        partyItem.delete()

    return JsonResponse('Item was added', safe=False)
#ADDING ITEMS INTO CART

def checkout_amazon(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

        lists, created = List.objects.get_or_create(customer=customer, used=False)
        listitems = lists.listitem_set.all()

        previousitem = OrderItem.objects.all()
    previous = {}
    # for i in previousitem:
    #     previousorder, created = PreviousOrder.objects.get_or_create(customer=customer, used=False)
    #     previousOrderItem, created = PreviousOrderItem.objects.get_or_create(previousorder=previousorder, product=i.product)
    #     previousOrderItem.delete()

    for i in previousitem:
        previous[i.product.id] = i.quantity
    for i in previous:
        product = Product.objects.get(id=i)
        previousorder, created = PreviousOrder.objects.get_or_create(customer=customer, used=False)
        previousOrderItem, created = PreviousOrderItem.objects.get_or_create(previousorder=previousorder, product=product)
        previousOrderItem.quantity = (previousOrderItem.quantity + 1)
        previousOrderItem.Ordered_from = 2
        # if previousOrderItem.quantity == 2:
        #     previousOrderItem.quantity -= 1
        previousOrderItem.save()

    items = []
    order = {'get_cart_items':0, 'get_cart_total':0}
    context = {'items':items, 'order':order, 'company': 'Amazon'}
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.amazon.in/')
    btn = driver.find_element_by_id("nav-link-accountList-nav-line-1")
    btn.click()
    user = driver.find_element_by_class_name('a-input-text')
    user.clear()
    user.send_keys("9284160249")
    btn = driver.find_element_by_id('continue')
    btn.click()

    passd =  driver.find_element_by_xpath("//input[@type='password']")
    passd.clear()
    passd.send_keys("Mani@1234")


    button = driver.find_element_by_xpath("//input[@type='submit']")
    button.click()

    print('User Successfully Logined In')

    products = OrderItem.objects.all()
    for product in products:
        url = product.product.product_amazon_url
        if url != "empty":
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
                    try:
                        button = driver.find_element_by_class_name('priceBlockBuyingPriceString')
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

        lists, created = List.objects.get_or_create(customer=customer, used=False)
        listitems = lists.listitem_set.all()

        previousitem = OrderItem.objects.all()
    previous = {}
    # for i in previousitem:
    #     previousorder, created = PreviousOrder.objects.get_or_create(customer=customer, used=False)
    #     previousOrderItem, created = PreviousOrderItem.objects.get_or_create(previousorder=previousorder, product=i.product)
    #     previousOrderItem.delete()

    for i in previousitem:
        previous[i.product.id] = i.quantity
    for i in previous:
        product = Product.objects.get(id=i)
        previousorder, created = PreviousOrder.objects.get_or_create(customer=customer, used=False)
        previousOrderItem, created = PreviousOrderItem.objects.get_or_create(previousorder=previousorder, product=product)
        previousOrderItem.quantity = (previousOrderItem.quantity + 1)
        previousOrderItem.Ordered_from = 1
        # if previousOrderItem.quantity == 2:
        #     previousOrderItem.quantity -= 1
        previousOrderItem.save()

    items = []
    order = {'get_cart_items':0, 'get_cart_total':0}
    context = {'items':items, 'order':order, 'company': 'Flipkart'}
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

        lists, created = List.objects.get_or_create(customer=customer, used=False)
        listitems = lists.listitem_set.all()

        previousitem = OrderItem.objects.all()
    previous = {}
    # for i in previousitem:
    #     previousorder, created = PreviousOrder.objects.get_or_create(customer=customer, used=False)
    #     previousOrderItem, created = PreviousOrderItem.objects.get_or_create(previousorder=previousorder, product=i.product)
    #     previousOrderItem.delete()

    for i in previousitem:
        previous[i.product.id] = i.quantity
    for i in previous:
        product = Product.objects.get(id=i)
        previousorder, created = PreviousOrder.objects.get_or_create(customer=customer, used=False)
        previousOrderItem, created = PreviousOrderItem.objects.get_or_create(previousorder=previousorder, product=product)
        previousOrderItem.quantity = (previousOrderItem.quantity + 1)
        previousOrderItem.Ordered_from = 3
        # if previousOrderItem.quantity == 2:
        #     previousOrderItem.quantity -= 1
        previousOrderItem.save()
        previousOrderItem.Ordered_from = 3
  
    items = []
    order = {'get_cart_items':0, 'get_cart_total':0}
    context = {'items':items, 'order':order, 'company': "Big Basket"}
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
    return render(request, 'store/trolley.html',{'items':items, 'order':order, 'company': "Big Basket"})

#ITEMS ADDED INTO CART

def add_to_cart(request):
    customer = request.user.customer
    list, created = List.objects.get_or_create(customer=customer, used=False)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    listitems = ListItem.objects.all()

    if len(items) == 0:
        print("EMPTY")
        for item in listitems:
            items[item.product.id] = item.quantity 
            if item.quantity == 0:
                del items[item.product.id]

    for i in items:
        product = Product.objects.get(id=i)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderItem.quantity += 1
        if orderItem.quantity == 2:
            orderItem.quantity -= 1
        orderItem.save()
    return render(request, "store/list.html")

def monthly_cart(request):
    customer = request.user.customer
    monthly, created = Monthly.objects.get_or_create(customer=customer, used=False)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    monthlyitems = MonthlyItem.objects.all()

    if len(monthly_items) == 0:
        print("EMPTY")
        for item in monthlyitems:
            monthly_items[item.product.id] = item.quantity 
            if item.quantity == 0:
                del monthly_items[item.product.id]

    for i in monthly_items:
        product = Product.objects.get(id=i)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderItem.quantity += 1
        if orderItem.quantity == 2:
            orderItem.quantity -= 1
        orderItem.save()
    return render(request, "store/monthly.html")

def party_cart(request):
    customer = request.user.customer
    party, created = Party.objects.get_or_create(customer=customer, used=False)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    partyitems = PartyItem.objects.all()

    if len(party_items) == 0:
        print("EMPTY")
        for item in partyitems:
            party_items[item.product.id] = item.quantity 
            if item.quantity == 0:
                del party_items[item.product.id]
    print(len(party_items))
    if len(party_items) == 0:
        print("Still empty")

    for i in party_items:
        product = Product.objects.get(id=i)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderItem.quantity += 1
        if orderItem.quantity == 2:
            orderItem.quantity -= 1
        orderItem.save()
        orderItem.save()
    return render(request, "store/party.html")
