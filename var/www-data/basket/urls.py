from django.conf.urls import url

from basket import views


urlpatterns = [
    url(r'^$', views.view_basket, name='basket'),
    url(r'^add/(?P<product_pk>\d+)$', views.add_to_basket, name='add_to_basket'),
    url(r'^remove/(?P<basketitem_pk>\d+)$', views.remove_from_basket, name='remove_from_basket'),

]
