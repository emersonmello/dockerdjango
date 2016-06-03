from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        help_text='Unique value for product page URL, created from name.',
        unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(
        help_text='Comma-delimited set of SEO keywords for meta tag',
        max_length=255,
        verbose_name='Meta Keywords')
    meta_description = models.CharField(
        help_text='Content for description meta tag',
        max_length=255, verbose_name='Meta Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['name']
        db_table = 'categories'
        verbose_name_plural = 'Categories'

    def __unicode__(self):
            return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(
        help_text='Unique value for product page URL, created from name.',
        unique=True)
    brand = models.CharField(max_length=50)
    sku = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    old_price = models.DecimalField(blank=True, decimal_places=2,
        default=0.0, max_digits=9)
    image = models.ImageField(upload_to='product_images')
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    stock = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()
    meta_keywords = models.CharField(help_text='Comma-delimited set of SEO keywords for meta tag',
        max_length=255, verbose_name='Meta Keywords')
    meta_description = models.CharField(help_text='Content for description meta tag',
        max_length=255,
        verbose_name='Meta Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(to='catalog.Category')

    class Meta:

        ordering = ['-created_at']
        db_table = 'products'

    def __unicode__(self):
        return self.name

    def get_price(self):
        #TODO: check for sales off
        return self.price
    
