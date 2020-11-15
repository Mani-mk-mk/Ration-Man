from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home-page'),
    path('about/', views.about, name = 'About'),
    path('contact/', views.contact, name = 'Contact'),
    path('tracker/', views.tracker, name = 'Tracker'),
    path('search/', views.search, name = 'Search'),
    path('productview/', views.productview, name = 'Products'),

]
