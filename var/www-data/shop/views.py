from django.shortcuts import render

from catalog.models import Product

def home(request):
    products = Product.objects.all()
    return render(request, "base.html", {'products': products})

def contact(request):
    return render(request, "contact.html")


def blog(request):
    return render(request, "blog.html")


def about(request):
    return render(request, "about.html")
