from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    clerkId = models.CharField(max_length=255, blank=True, unique=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=[('user', 'User'), ('admin', 'Admin'), ('seller', 'Seller')],
        default='user'
    )
    avatar_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Product(models.Model):
    """Product model"""
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('food', 'Food'),
        ('books', 'Books'),
        ('home', 'Home & Garden'),
        ('sports', 'Sports & Outdoors'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image_url = models.URLField()
    stock = models.IntegerField(default=0)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Address(models.Model):
    """User address model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Kenya')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"


class Order(models.Model):
    """Order model"""
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    order_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(
        max_length=20,
        choices=[('mpesa', 'M-Pesa'), ('stripe', 'Stripe'), ('card', 'Card')],
        default='mpesa'
    )
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='orders')
    notes = models.TextField(blank=True)
    mpesa_receipt_number = models.CharField(max_length=50, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_id} - {self.user.username}"


class OrderItem(models.Model):
    """Order item model"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


class Payment(models.Model):
    """Payment transaction model"""
    PAYMENT_STATUS = [
        ('initiated', 'Initiated'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=255, unique=True)
    payment_method = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='initiated')
    mpesa_data = models.JSONField(null=True, blank=True)
    stripe_data = models.JSONField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"


class Blog(models.Model):
    """Blog post model"""
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    image_url = models.URLField(blank=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('news', 'News'),
            ('tutorial', 'Tutorial'),
            ('review', 'Review'),
            ('tips', 'Tips'),
            ('other', 'Other'),
        ]
    )
    is_published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title
