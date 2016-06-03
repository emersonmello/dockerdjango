from django.contrib import admin

from orders.models import Order


class OrderAdmin(admin.ModelAdmin):
    class Meta:
        model = Order

admin.site.register(Order, OrderAdmin)
