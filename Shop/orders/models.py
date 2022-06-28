from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from products.models import Product


class Status(models.Model):
    status_name = models.CharField(max_length=20, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Статус %s" % self.status_name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'


class Order(models.Model):
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    customer_name = models.CharField(max_length=68, blank=True, null=True, default=None)
    customer_email = models.EmailField(blank=True, null=True, default=None)
    customer_phone = models.CharField(max_length=24, blank=True, null=True, default=None)
    customer_address = models.CharField(max_length=150, blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Заказ %s %s" % (self.id, self.status.status_name)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    item_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # price*quantity
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.product_name

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
        item_price = self.product.price
        self.item_price = item_price
        self.total_cost = int(self.quantity)*item_price

        super(ProductInOrder, self).save(*args, **kwargs)


def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)
    order_total_cost = 0

    for prod in products_in_order:
        order_total_cost += prod.total_cost

    instance.order.total_cost = order_total_cost
    instance.order.save(force_update=True)


post_save.connect(product_in_order_post_save, sender=ProductInOrder)


class ProductInBasket(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    item_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # price*quantity
    is_active = models.BooleanField(default=True)
    session_key = models.CharField(max_length=156, blank=True, null=True, default=None)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.product_name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        item_price = self.product.price
        self.item_price = item_price
        self.total_cost = int(self.quantity)*item_price

        super(ProductInBasket, self).save(*args, **kwargs)
