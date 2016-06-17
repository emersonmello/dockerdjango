from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, HttpResponseRedirect

from accounts.models import Profile
from basket.models import Basket
from basket.basket_utils import get_current_basket
from orders.models import Order
from orders.forms import ShippingForm, PaymentForm

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

@login_required
def checkout(request):
    try:
        basket = get_current_basket(request)
        profile = Profile.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(basket=basket,
            profile=profile)
        request.session['order'] = {
            'profile_pk': profile.pk,
            'basket_pk': basket.pk,
            'order_pk': order.pk
        }

        if basket.size() < 1:
            return HttpResponseRedirect(reverse('basket'))

    except Exception as e:
        logger.error('%s (%s)' % (e.message, type(e)))

    if 'shipping' in request.POST:
        return HttpResponseRedirect(reverse('shipping'))
    elif 'payment' in request.POST:
        return HttpResponseRedirect(reverse('order_payment'))
    else:
        return render(request, "checkout.html", {
            'basket': basket
        })


@login_required
def order_shipping(request):
    shipping_form = ShippingForm()
    try:
        basket = Basket.objects.get(pk=request.session['order']['basket_pk'])
        print basket
        if request.POST:
            shipping_form = ShippingForm(request.POST)
            if shipping_form.is_valid():
                shipping_form.save(request.session['order']['order_pk'])
                request.session['order'].update(
                    shipping_form.set_order_shipping(
                        request.session['order']
                    )
                )
                return HttpResponseRedirect(reverse('payment'))
    except Exception as e:
        logger.error('%s (%s)' % (e.message, type(e)))
    return render(request,'shipping.html', {
        'shipping_form': shipping_form,
        'basket': basket
    })


@login_required
def order_payment(request):
    payment_form = PaymentForm()
    try:
        basket = Basket.objects.get(pk=request.session['order']['basket_pk'])
        if request.POST:
            payment_form = PaymentForm(request.POST)
            if payment_form.is_valid():
                payment_form.save(request.session['order']['order_pk'])
                clean_session(request)
                basket.active = False
                basket.save()
                return HttpResponseRedirect(reverse('details'))
    except Exception as e:
        logger.error('%s (%s)' % (e.message, type(e)))
    return render(request,'payment.html', {
        'payment_form': payment_form,
        'basket': basket
    })


@login_required
def order_details(request):
    try:
        order = Order.objects.get(pk=request.session['order']['order_pk'])
        if request.session.has_key('order'):
            del request.session['order']
    except Exception as e:
        logger.error('%s (%s)' % (e.message, type(e)))
    return render(request, 'details.html', {
        'order': order
    })

def clean_session(request):
    if request.session.has_key('carry_over_basket'):
        del request.session['carry_over_basket']
    if request.session.has_key('anon_basket_id'):
        del request.session['anon_basket_id']
    request.session.modified = True



