from django.conf.urls import url, include

from . import views

app_name = 'catalog'
urlpatterns = [
    url(r'^$', views.catalog, name='show_catalog'),
    url(r'^product/(?P<product_pk>\d+)$', views.show_product, name='show_product'),

]
