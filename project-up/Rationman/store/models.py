from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return str(self.id)

    @property
    def flipkart_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.total_flipkart for item in orderitem])
        return total

    @property
    def amazon_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.total_amazon for item in orderitem])
        return total

    @property
    def bigb_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.total_bigb for item in orderitem])
        return total

    @property
    def get_cart_items(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    @property
    def total_flipkart(self):
        total = self.product.price_flipkart * self.quantity
        return total
    
    @property
    def total_amazon(self):
        total = self.product.price_amazon * self.quantity
        return total

    @property
    def total_bigb(self):
        total = self.product.price_bigb * self.quantity
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
