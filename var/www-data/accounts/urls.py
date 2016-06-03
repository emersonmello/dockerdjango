from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.auth.views import ( password_reset, password_reset_done,
    password_reset_confirm, password_reset_complete, logout)
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

from accounts import views

urlpatterns = [
	url(r'^create/$', views.create_account, name='signup'),
	url(r'^logout/$', logout, {'next_page': 'logged_out'}, name='logout'),
	url(r'^see-ya/$', views.logged_out, name='logged_out'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^password/reset/$', password_reset, {'template_name': 'accounts/password_reset.html',
    	'post_reset_redirect': views.reset_redirect}, name='password_reset'),
    url(r'^password/reset/done/$', password_reset_done, {'template_name': 'accounts/password_reset_done.html'}, name='password_reset_done'),
	url(r'^password/awaiting_reset/$', views.reset_redirect, name='post_reset_redirect'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$', password_reset_confirm, {'template_name': 'accounts/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^password/reset/complete/$', password_reset_complete, {'template_name': 'accounts/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^profile/$', views.view_profile, name='profile'),
]
