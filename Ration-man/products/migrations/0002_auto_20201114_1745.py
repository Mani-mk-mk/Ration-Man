# Generated by Django 3.1.3 on 2020-11-14 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_category', models.CharField(max_length=50)),
                ('product_quantity', models.CharField(max_length=50)),
                ('product_image', models.ImageField(upload_to='images')),
                ('product_flipkart_url', models.TextField(max_length=200)),
                ('product_amazon_url', models.TextField(max_length=200)),
                ('product_bigb_url', models.TextField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Products',
        ),
    ]