# Generated by Django 3.1.3 on 2020-11-14 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_price', models.IntegerField()),
                ('product_category', models.CharField(max_length=50)),
                ('product_image', models.ImageField(upload_to='images')),
                ('product_flipkart_url', models.TextField(max_length=200)),
                ('product_amazon_url', models.TextField(max_length=200)),
                ('product_bigb_url', models.TextField(max_length=200)),
            ],
        ),
    ]
