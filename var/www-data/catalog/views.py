from django.shortcuts import get_object_or_404, render

from catalog.models import Product


def catalog(request):
    products = Product.objects.all()
    return render(request, "catalog.html", {
        'products': products,
    })


def show_product(request, product_pk):
    product = get_object_or_404(Product,pk=product_pk)
    return render(request, "product.html", {'product': product})


def show_category(request):
    return render(request, "category.html", {})