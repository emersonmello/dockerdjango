'''
   Basket model based on https://github.com/drivelous/ecmrc
'''
from __future__ import unicode_literals

from django.db import models

from catalog.models import Product, Category

class Basket(models.Model):
    user = models.ForeignKey('accounts.Profile', null=True, blank=True)
    session = models.CharField(max_length=200, default='', null=True, blank=True)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Saves items in basket and re-calculates total each time"""

        self.calculate_basket()

        super(Basket, self).save(*args, **kwargs)

    def get_basket_items(self):
        """Returns list of all basket's basketitems"""

        return self.basketitem_set.all()

    def size(self):
        """Returns number of items in basket"""

        return len(self.get_basket_items())

    def calculate_basket(self):
        """Calculates all basket contents"""

        total = 0
        basket_items = self.get_basket_items()
        for item in basket_items:
            total += (item.quantity * item.price)
        self.total = total

    def create_or_update_basket_item(self, product_pk, quantity=None):
        """ For now just add to basket, without no stock check """

        try:
            product = Product.objects.get(pk=product_pk)
        except Product.DoesNotExist:
            raise Http404

        basketitem, created = BasketItem.objects.get_or_create(basket=self,
                                                            product=product,
                                                            name=product.name)

        # if basketitem is just created, use basketitem's product methods to
        # finish creating basketitem
        if created:
            price = product.get_price()
            basketitem.price = price
            basketitem.quantity += quantity
            basketitem.total = price * quantity
            basketitem.save()
            self.save()

        # if basketitem already existed, then add user specified
        # quantity to update quantity
        elif not created:
            new_quantity = basketitem.quantity + quantity
            basketitem.quantity = new_quantity
            basketitem.save()

        return basketitem

    def retrieve_basket_item(self, basketitem_pk):
        """Retrieves item from basket"""

        try:
            basketitem = BasketItem.objects.get(basket=self, pk=basketitem_pk)
        except BasketItem.DoesNotExist:
            raise Http404
        return basketitem


    def finalize_basket(self, request):
        """ for now just set active to false """

        self.active = False
        self.save()
        return True


    def __unicode__(self):
        return str(self.id)


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket)
    product = models.ForeignKey(Product)
    name = models.CharField(max_length=80, null=True)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    price = models.DecimalField(default=9.99, max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    size = models.CharField(max_length=30, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Creates name attribute if none exists.
        Calculates new total on every save
        """

        if not self.name:
            self.name = self.product.name

        self.calculate_total()

        super(BasketItem, self).save(*args, **kwargs)

    def get_price(self):
        """Gets current price
        using product's get_price method
        """

        product = self.product
        return product.get_price()

    def is_sale(self):
        """Returns boolean if product is on sale"""

        product = self.product
        return product.is_sale(size=self.size)

    def get_stock(self):
        """Checks current stock of basketitem's product"""

        return self.product.get_stock(size=self.size)

    def calculate_total(self):
        """Calculates basketitem total. Called during every save"""

        self.total = self.get_quantity() * self.get_price()

    def get_quantity(self):
        """Returns basket's quantity of current basketitem"""

        return self.quantity

    def __str__(self):
        return "Basket #" + str(self.basket.pk) + " - " + str(self.product)