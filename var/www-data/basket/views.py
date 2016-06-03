import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.utils.translation import ugettext as _

from basket.models import Basket


def view_basket(request):
    basket, created = Basket.objects.get_or_create(
        session=request.session.session_key, active=True)
    return render(request, "view_basket.html", {
        'basket_items': basket.get_basket_items(),
        'basket': basket
        })


def add_to_basket(request, product_pk, quantity=1):
    status = 200
    basket, created = Basket.objects.get_or_create(
        session=request.session.session_key, active=True)
    basket.create_or_update_basket_item(product_pk, quantity)
    response_data = {'success': _('Item successfully added')}
    return HttpResponse(json.dumps(response_data),
        content_type="application/json", status=status)


def remove_from_basket(request, basketitem_pk):
    basket, created = Basket.objects.get_or_create(
        session=request.session.session_key, active=True)
    basket_item = basket.retrieve_basket_item(basketitem_pk)
    basket_item.delete()
    basket.save()
    return HttpResponseRedirect(reverse('basket'))


def update_basket(request):
    pass


