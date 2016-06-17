from django.shortcuts import get_object_or_404, render

from catalog.models import Product
from basket.basket_utils import get_current_basket

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def catalog(request):
    try:
        products = Product.objects.all()
        basket = get_current_basket(request)
    except Exception as e:
        logger.error('%s (%s)' % (e.message, type(e)))
        products = []
        basket = None
    return render(request, "catalog.html", {
        'products': products,
        'basket': basket
    })


def show_product(request, product_pk):
    product = get_object_or_404(Product,pk=product_pk)
    return render(request, "product.html", {'product': product})


def show_category(request):
    return render(request, "category.html", {})