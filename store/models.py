from django.db import models
from django.contrib.auth.models import User
from scrape import scrape as wb

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_category = models.CharField(max_length=50)
    product_quantity = models.CharField(max_length=50)
    product_image = models.ImageField(upload_to="images")

    product_flipkart_url = models.TextField(max_length=200)
    product_amazon_url = models.TextField(max_length=200)
    product_bigb_url = models.TextField(max_length=200)

    price_flipkart = models.DecimalField(max_digits=5, decimal_places=2,default=0, null=True, blank=True)
    price_amazon = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, blank=True)
    price_bigb = models.DecimalField(max_digits=5, decimal_places=2, null=True,default=0 , blank=True)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    total_a = 0
    total_f = 0
    total_b = 0

    def __str__(self):
        return str(self.id)

    @property
    def flipkart_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.total_flipkart for item in orderitem])
        Order.total_f += total
        return total

    @property
    def amazon_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.total_amazon for item in orderitem])
        Order.total_a += total
        return total

    @property
    def bigb_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.total_bigb for item in orderitem])
        Order.total_b += total
        return total

    @property
    def get_cart_items(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total

    @property
    def best_buy(self):
        if Order.total_a <= Order.total_f and Order.total_a <= Order.total_b:
            return Order.total_a
        elif Order.total_f <= Order.total_b:
            return Order.total_f
        else:
            return Order.total_b

    @property
    def offer(self):
        if Order.total_a <= Order.total_f and Order.total_a <= Order.total_b:
            return "Amazon"
        elif Order.total_f <= Order.total_b:
            return "Flipkart"
        else:
            return "BigBasket"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    @property
    def total_flipkart(self):
        try:
            price = wb.flipkart(self.product.product_flipkart_url)
        except:
            price = 0
        self.product.price_flipkart = price
        total = price * self.quantity
        return total
    
    @property
    def total_amazon(self):
        try:
            price = wb.amazon(self.product.product_amazon_url)
        except:
            price = 0
        self.product.price_amazon = price
        total = price * self.quantity
        return total

    @property
    def total_bigb(self):
        try:
            price = wb.bigb(self.product.product_bigb_url)
        except:
            price = 0
        self.product.price_bigb = price
        total = price * self.quantity
        return total


class List(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)

class ListItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    list = models.ForeignKey(List, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

class PreviousOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)

class PreviousOrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    previousorder = models.ForeignKey(PreviousOrder, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    Ordered_from = models.IntegerField(default=1, null=True, blank=True)

class Monthly(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)

class MonthlyItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    monthly = models.ForeignKey(Monthly, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

class Party(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)

class PartyItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
