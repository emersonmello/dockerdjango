from django.shortcuts import render

from catalog.models import Product
from basket.models import Basket
from basket.basket_utils import get_current_basket

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def home(request):
    try:
        products = Product.objects.all()
        basket = get_current_basket(request)
    except Exception as e:
        logger.error('%s (%s)' % (e.message, type(e)))
        products = []
        basket = []
    return render(request, "base.html", {
        'products': products,
        'basket': basket
    })
