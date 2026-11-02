from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    length = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    width = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    height = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    weight = models.DecimalField(max_digits=8, decimal_places=3, validators=[MinValueValidator(0.001)])

    def __str__(self):
        return self.name


class ShippingBox(models.Model):
    name = models.CharField(max_length=120, unique=True)
    inner_length = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    inner_width = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    inner_height = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    max_weight = models.DecimalField(max_digits=8, decimal_places=3, validators=[MinValueValidator(0.001)])
    cost = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


class CustomerOrder(models.Model):
    reference = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference


class OrderItem(models.Model):
    order = models.ForeignKey(CustomerOrder, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order", "product"], name="unique_product_per_order")
        ]

    def __str__(self):
        return f"{self.product} x {self.quantity}"
