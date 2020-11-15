from django.db import models

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    product_category = models.CharField(max_length=50)
    product_quantity = models.CharField(max_length=50)
    product_image = models.ImageField(upload_to="images")
    product_flipkart_url = models.TextField(max_length=200)
    product_amazon_url = models.TextField(max_length=200)
    product_bigb_url = models.TextField(max_length=200)

    def __str__(self):
        return self.product_name
