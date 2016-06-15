from django.conf.urls import url

from orders import views


urlpatterns = [
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^shipping/$', views.order_shipping, name='shipping'),
    url(r'^payment/$', views.order_payment, name='payment'),
    url(r'^details/$', views.order_details, name='details'),

]