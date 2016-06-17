from django.conf import settings
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models



class CustomerManager(BaseUserManager):
	"""
	Default user model for project is custom 'Customer',
	not default user
	"""
	def create_user(self, username, email, password=None):
		if not email:
			raise ValueError('users must have an email address')

		user = self.model(
			username=username,
			email=CustomerManager.normalize_email(email),
		)

		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, username, email, password):
		user = self.create_user(
			username=username,
			email=email,
			password=password,
		)

		user.is_superuser = True
		user.is_admin = True
		user.is_staff = True
		user.save(using=self._db)
		return user

class Customer(AbstractBaseUser, PermissionsMixin):
	"""Custom user model"""

	username = models.CharField(max_length=40, unique=True, db_index=True)
	email = models.EmailField(max_length=254)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email',]

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	objects = CustomerManager()

	def get_full_name(self):
		return "{0} | {1}".format(self.username, self.email)

	def get_short_name(self):
		return self.username

class Profile(models.Model):

	user = models.ForeignKey(Customer)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)


	def __str__(self):
		return str(self.user)

	def last_order(self):
		return self.order_set.all().last()
