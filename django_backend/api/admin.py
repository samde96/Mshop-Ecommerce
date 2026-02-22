from django.contrib import admin
from .models import UserProfile, Product, Order, OrderItem, Address, Payment, Blog


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone_number', 'created_at']
    search_fields = ['user__username', 'phone_number']
    list_filter = ['role', 'created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'stock', 'seller', 'is_active', 'created_at']
    search_fields = ['name', 'category']
    list_filter = ['category', 'is_active', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'total_amount', 'order_status', 'payment_status', 'created_at']
    search_fields = ['order_id', 'user__username']
    list_filter = ['order_status', 'payment_status', 'payment_method', 'created_at']
    readonly_fields = ['order_id', 'created_at', 'updated_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price', 'total_price']
    search_fields = ['order__order_id', 'product__name']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'city', 'country', 'is_default', 'created_at']
    search_fields = ['name', 'user__username', 'city']
    list_filter = ['is_default', 'country', 'created_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'order', 'amount', 'payment_method', 'status', 'created_at']
    search_fields = ['transaction_id', 'order__order_id']
    list_filter = ['payment_method', 'status', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'views', 'created_at']
    search_fields = ['title', 'author__username', 'category']
    list_filter = ['is_published', 'category', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'views']
    prepopulated_fields = {'slug': ('title',)}
