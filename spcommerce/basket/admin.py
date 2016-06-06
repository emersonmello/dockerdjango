from django.contrib import admin

from basket.models import Basket, BasketItem


class BasketAdmin(admin.ModelAdmin):
    class Meta:
        model = Basket

admin.site.register(Basket, BasketAdmin)

class BasketItemAdmin(admin.ModelAdmin):
    class Meta:
        model = BasketItem

admin.site.register(BasketItem, BasketItemAdmin)
