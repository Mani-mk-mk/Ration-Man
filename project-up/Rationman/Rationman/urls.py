"""Rationman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from store import views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.home, name = "home-page"),
    path('register/', home_views.register, name ='register'),
    path('profile/', home_views.profile, name ='profile'),
    path('categories/', home_views.category, name ='category'),
    path('login/', auth_views.LoginView.as_view(template_name = 'store/login.html'), name ='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'store/logout.html'), name ='logout'),
    path('drinks/', home_views.drinks, name = 'drinks'),
    path('search/', home_views.search, name = 'search'),
    path('cereals/', home_views.cereals, name = 'cereals'),
    path('spices/', home_views.spices, name = 'spices'),
    path('diaryprod/', home_views.diaryprod, name = 'diaryprod'),
    path('reminder/', home_views.reminder, name = 'reminder'),
    path('snacks/', home_views.snacks, name = 'snacks'),
    path('list/', home_views.lists, name = 'list'),
    path('trolley/', home_views.trolley, name = 'trolley'),
    path('update_item/', home_views.updateItem, name = 'update_item'),
    path('update_list/', home_views.updateList, name = 'update_list'),
    path('amazon/', home_views.checkout_amazon, name = 'checkout_amazon'),
    path('flipkart/', home_views.checkout_flipkart, name = 'checkout_flipkart'),
    path('bigb/', home_views.checkout_bigb, name = 'checkout_bigb'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)