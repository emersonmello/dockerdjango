from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, resolve_url, get_object_or_404, HttpResponseRedirect
from django.utils.http import is_safe_url


from .forms import UserCreationForm
from .models import Customer, Profile


def create_account(request):
	"""Displays user signup form"""

	# Don't allow logged in users to acces login_view
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('profile'))

	form = UserCreationForm(request.POST or None)

	if request.POST and form.is_valid():
		form.save()
		messages.info(request, "You're signed up! Use the login form below to get started." )
		return HttpResponseRedirect(reverse('login'))
	return render(request, 'create_account.html', {
		'form': form,
	})

def login_view(request):
	"""Displays user login view. If user has had a previously anonymous
	account with a shopping cart, assigns that cart to them when logged in
	"""

	# Don't allow logged in users to acces login_view
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('profile'))

	redirect_to = request.GET.get('next' or None)

	if redirect_to is None and 'carry_over_cart' in request.session:
		redirect_to = reverse('view_cart')

	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			if not is_safe_url(url=redirect_to, host=request.get_host()):
				redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
			login(request, form.get_user())
			if 'carry_over_cart' in request.session:
				assign_anon_cart_to_user(request)
			return HttpResponseRedirect(redirect_to)
	else:
		form = AuthenticationForm(request)

	return render(request, 'registration/login.html', {
		'form': form
	})

def logged_out(request):
	"""Logs user out using provided logout function from django.contrib.auth"""

	clean_session(request)

	if request.user.is_anonymous():
		return HttpResponseRedirect(reverse('home'))

	logout(request)
	return render(request, 'accounts/logged_out.html')

def reset_redirect(request):
	"""If user requests to change password, redirects them until
	change is processed
	"""

	return render(request, 'accounts/password_awaiting_change.html')

@login_required
def view_profile(request):
	"""Views user's account overview"""

	user = request.user
	profile = Profile.objects.get(user=user)

	return render(request, 'profile.html', {
		'profile': profile,
	})

def clean_session(request):
    if request.session.has_key('carry_over_basket'):
        del request.session['carry_over_basket']
    if request.session.has_key('anon_basket_id'):
        del request.session['anon_basket_id']
    if request.session.has_key('order'):
        del request.session['order']

