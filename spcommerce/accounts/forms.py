from datetime import datetime

from django import forms
from django.conf import settings
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _


from .models import Customer, Profile

class UserCreationForm(forms.ModelForm):
	"""
	Creates user after checking that basic checks are met. After checks
	are passed, creates a user profile and Stripe account for user email
	address
	"""
	error_messages = {
		'duplicate_username': _("A user with that username already exists."),
		'password_mismatch': _("The two password fields didn't match."),
		'too_short': _("Passwords must be at least 6 characters long."),
		'user_same_pass': _("Username cannot be same as password")
	}

	username = forms.RegexField(label="Username", max_length=30, regex=r'^[\w.@+-]+$')
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

	class Meta:
		model = Customer
		fields = ['username', 'email']

	def clean_password1(self):
		password1 = self.cleaned_data.get("password1")
		if len(password1) < 6:
			raise forms.ValidationError(
				self.error_messages['too_short'],
			)
		return password1

	def clean_password2(self):
		# Check that the two password entries match
		username = self.cleaned_data.get('username')
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(
				self.error_messages['password_mismatch']
			)
		elif password2 == username:
			raise forms.ValidationError(
				self.error_messages['user_same_pass']
			)
		return password2

	def clean_email(self):
		email = self.cleaned_data.get('email')
		check_duplicate = Customer.objects.filter(email=email).exists()
		if check_duplicate:
			msg = "Account already exists for email {0}.".format(email)
			raise forms.ValidationError(msg)
		return email

	def save(self, commit=True):
		"""Creates user profile on saving """
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
			new_profile = Profile(user=user)
			new_profile.save()
		return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Customer
        fields = '__all__'

    def clean_password(self):
        # always return the initial value
        return self.initial['password']
