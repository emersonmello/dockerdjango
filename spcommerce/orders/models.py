from __future__ import unicode_literals
import string, random

from django.db import models

from django_countries.fields import CountryField

from accounts.models import Profile
from basket.models import Basket


BRAND_CHOICES = (
    ('VISA', 'VISA'),
    ('MASTERCARD', 'MASTERCARD'),
    ('AMERICAN EXPRESS', 'AMERICAN EXPRESS'),

)

class Order(models.Model):
    profile = models.ForeignKey(Profile, null=True, blank=True)
    basket = models.ForeignKey(Basket)
    order_id = models.CharField(max_length=50, null=True, unique=True)
    full_name = models.CharField(max_length=100, null=True, blank=False) # card full name
    card_id = models.CharField(max_length=100, null=True)
    shipping_nickname = models.CharField(max_length=100, null=True)
    shipping_first_name = models.CharField(max_length=100, null=True)
    shipping_last_name = models.CharField(max_length=100, null=True)
    shipping_address1 = models.CharField(max_length=100, null=True)
    shipping_address2 = models.CharField(max_length=100, null=True)
    shipping_city = models.CharField(max_length=2, null=True)
    shipping_state = models.CharField(max_length=100, null=True)
    shipping_zip = models.CharField(max_length=16, null=True)
    shipping_country = CountryField()
    shipping_phone_number = models.CharField(max_length=16, null=True)
    billing_address1 = models.CharField(max_length=100, null=True)
    billing_address2 = models.CharField(max_length=100, null=True, blank=True)
    billing_city = models.CharField(max_length=2, null=True)
    billing_state = models.CharField(max_length=50, null=True)
    billing_zip = models.CharField(max_length=16, null=True)
    billing_country = CountryField()
    exp_month = models.PositiveSmallIntegerField(null=True)
    exp_year = models.PositiveSmallIntegerField(null=True)
    cc_four = models.CharField(max_length=4, null=True, blank=True)
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    active = models.BooleanField(default=True)
    date_completed = models.DateTimeField(null=True, blank=True, auto_now_add=False)

    def save(self, *args, **kwargs):
        """Generates guaranteed unique ID for each order"""
        if not self.order_id:
            while not self.order_id:
                order_id = order_id_generator()
                gen_order_id = str(order_id[:3]) + str(self.basket.pk) + str(order_id[3:])
                if not Order.objects.filter(order_id=gen_order_id):
                    self.order_id = gen_order_id
        super(Order,self).save()


def order_id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
