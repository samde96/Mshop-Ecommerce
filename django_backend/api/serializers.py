from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, Product, Order, OrderItem, Address,
    Payment, Blog
)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'phone_number', 'clerkId', 'role', 'avatar_url', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']


class ProductSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.username', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'category', 'image_url',
            'stock', 'seller', 'seller_name', 'is_active', 'created_at', 'updated_at'
        ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 'name', 'phone', 'street', 'city', 'state',
            'postal_code', 'country', 'is_default', 'created_at', 'updated_at'
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'unit_price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'user', 'total_amount', 'tax_amount', 'shipping_amount',
            'order_status', 'payment_status', 'payment_method', 'shipping_address',
            'notes', 'mpesa_receipt_number', 'stripe_payment_intent_id',
            'items', 'created_at', 'updated_at'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'transaction_id', 'payment_method', 'amount',
            'currency', 'status', 'mpesa_data', 'stripe_data',
            'error_message', 'created_at', 'updated_at'
        ]


class BlogSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'author', 'author_name',
            'image_url', 'category', 'is_published', 'views',
            'created_at', 'updated_at', 'published_at'
        ]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    phone_number = serializers.CharField(max_length=20, required=False)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        UserProfile.objects.create(
            user=user,
            phone_number=validated_data.get('phone_number', '')
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ProfileSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    profile = UserProfileSerializer(read_only=True)
