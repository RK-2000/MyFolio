from django.shortcuts import render

# Create your views here.



def join(request):
    if request.user.is_authenticated:
