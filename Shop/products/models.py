from django.db import models
from django.urls import reverse


class ProductCategory(models.Model):
    category_name = models.CharField(max_length=68, blank=True, null=True, default=None)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.category_name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категория товаров'

    def get_absolute_url(self):
        return reverse('shop:catalog', args=[self.slug, ])


class Product(models.Model):
    product_name = models.CharField(max_length=68, blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    category = models.ForeignKey(ProductCategory, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product_name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products_images/')
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

