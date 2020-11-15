from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def category(request):
    return render(request,'Categories/category.html',{'title': 'Categories'})
