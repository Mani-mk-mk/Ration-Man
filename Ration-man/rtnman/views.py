from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'rtnman/home.html')

def about(request):
    return HttpResponse("WE ARE AT ABOUT PAGE")

def contact(request):
    return HttpResponse("WE ARE AT Contact PAGE")

def tracker(request):
    return HttpResponse("WE ARE AT Tracker PAGE")

def search(request):
    return HttpResponse("WE ARE AT Search PAGE")

def productview(request):
    return HttpResponse("WE ARE AT PD PAGE")
