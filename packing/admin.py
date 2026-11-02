from django.contrib import admin
from .models import Product, ShippingBox, CustomerOrder, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "length", "width", "height", "weight")
    search_fields = ("name",)

@admin.register(ShippingBox)
class ShippingBoxAdmin(admin.ModelAdmin):
    list_display = ("name", "inner_length", "inner_width", "inner_height", "max_weight", "cost")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ("reference", "created_at")
    inlines = [OrderItemInline]
