from django.forms import ModelForm
from django import forms

from django_countries.fields import LazyTypedChoiceField
from django_countries import countries

from orders.models import Order, BRAND_CHOICES

class ShippingForm(forms.Form):
    shipping_nickname = forms.CharField()
    shipping_first_name = forms.CharField()
    shipping_last_name = forms.CharField()
    shipping_phone_number = forms.CharField(required=False)
    shipping_address1 = forms.CharField()
    shipping_address2 = forms.CharField(required=False)
    shipping_city = forms.CharField(widget=forms.TextInput(attrs={'size': '2'}))
    shipping_state = forms.CharField()
    shipping_zip = forms.CharField(widget=forms.TextInput(attrs={'size': '9'}))
    shipping_country = LazyTypedChoiceField(choices=countries)

    def set_order_shipping(self, order_as_json):
        order_as_json.update({
            'shipping_nickname': self.cleaned_data['shipping_nickname'],
            'shipping_first_name': self.cleaned_data['shipping_first_name'],
            'shipping_last_name': self.cleaned_data['shipping_last_name'],
            'shipping_address1': self.cleaned_data['shipping_address1'],
            'shipping_address2': self.cleaned_data['shipping_address2'],
            'shipping_city': self.cleaned_data['shipping_city'],
            'shipping_state': self.cleaned_data['shipping_state'],
            'shipping_zip': self.cleaned_data['shipping_zip'],
            'shipping_country': self.cleaned_data['shipping_country'],
            'shipping_phone_number': self.cleaned_data['shipping_phone_number']
        })

        return order_as_json

    def save(self, order_pk):
        order = Order.objects.get(pk=order_pk)
        order.shipping_nickname = self.cleaned_data['shipping_nickname']
        order.shipping_first_name = self.cleaned_data['shipping_first_name']
        order.shipping_last_name = self.cleaned_data['shipping_last_name']
        order.shipping_address1 = self.cleaned_data['shipping_address1']
        order.shipping_address2 = self.cleaned_data['shipping_address2']
        order.shipping_city = self.cleaned_data['shipping_city']
        order.shipping_state = self.cleaned_data['shipping_state']
        order.shipping_zip = self.cleaned_data['shipping_zip']
        order.shipping_country = self.cleaned_data['shipping_country']
        order.shipping_phone_number = self.cleaned_data['shipping_phone_number']
        order.save()

class PaymentForm(forms.Form):
    card_id = forms.CharField()
    exp_month = forms.CharField()
    exp_year = forms.CharField()
    full_name = forms.CharField()
    cc_four = forms.CharField()
    brand = forms.ChoiceField(choices=BRAND_CHOICES,
                widget=forms.Select(),
                required=True
            )
    billing_address1 = forms.CharField()
    billing_address2 = forms.CharField(required=False)
    billing_city = forms.CharField(widget=forms.TextInput(attrs={'size': '2'}))
    billing_state = forms.CharField()
    billing_zip = forms.CharField()
    billing_country = LazyTypedChoiceField(choices=countries)

    def set_order_payment(self, order_as_json):
        order_as_json.update({
            'billing_nickname': self.self.cleaned_data['billing_nickname'],
            'billing_first_name': self.self.cleaned_data['billing_first_name'],
            'billing_last_name': self.self.cleaned_data['billing_last_name'],
            'billing_address1': self.self.cleaned_data['billing_address1'],
            'billing_address2': self.self.cleaned_data['billing_address2'],
            'billing_city': self.self.cleaned_data['billing_city'],
            'billing_state': self.self.cleaned_data['billing_state'],
            'billing_zip': self.self.cleaned_data['billing_zip'],
            'billing_country': self.self.cleaned_data['billing_country'],
            'billing_phone_number': self.self.cleaned_data['billing_phone_number'],
            'full_name': self.self.cleaned_data['full_name'],
            'card_id': self.self.cleaned_data['card_id'],
            'exp_month': self.self.cleaned_data['exp_month'],
            'exp_year': self.self.cleaned_data['exp_year'],
            'brand': self.self.cleaned_data['brand']
        })

        return order_as_json

    def save(self, order_pk):
        order = Order.objects.get(pk=order_pk)
        order.billing_address1 = self.cleaned_data['billing_address1']
        order.billing_address2 = self.cleaned_data['billing_address2']
        order.billing_city = self.cleaned_data['billing_city']
        order.billing_state = self.cleaned_data['billing_state']
        order.billing_zip = self.cleaned_data['billing_zip']
        order.billing_country = self.cleaned_data['billing_country']
        order.full_name = self.cleaned_data['full_name']
        order.card_id = self.cleaned_data['card_id']
        order.exp_month = self.cleaned_data['exp_month']
        order.exp_year = self.cleaned_data['exp_year']
        order.brand = self.cleaned_data['brand']
        order.save()
