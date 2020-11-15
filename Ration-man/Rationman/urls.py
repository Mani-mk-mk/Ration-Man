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
from user import views as user_views
from Categories import views as category_views
from products import views as products_view
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name ='register'),
    path('profile/', user_views.profile, name ='profile'),
    path('login/', auth_views.LoginView.as_view(template_name = 'user/login.html'), name ='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'user/logout.html'), name ='logout'),
    path('drinks/', products_view.drinks, name = 'drinks'),
    path('cereals/', products_view.cereals, name = 'cereals'),
    path('diaryprod/', products_view.diaryprod, name = 'diaryprod'),
    path('spices/', products_view.spices, name = 'spices'),
    path('snacks/', products_view.snacks, name = 'snacks'),
    path('about/', include("rtnman.urls")),
    path('contact/', include("rtnman.urls")),
    path('tracker/', include("rtnman.urls")),
    path('search/', include("rtnman.urls")),
    path('productview/', include("rtnman.urls")),
    path('', include("rtnman.urls")),
    path('categories/', category_views.category, name='Category'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
