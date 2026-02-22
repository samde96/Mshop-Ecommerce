from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
import requests
import os
from base64 import b64encode
from datetime import datetime

from .models import (
    UserProfile, Product, Order, OrderItem, Address,
    Payment, Blog
)
from .serializers import (
    UserSerializer, ProductSerializer, OrderSerializer, AddressSerializer,
    PaymentSerializer, BlogSerializer, RegisterSerializer, LoginSerializer,
    ProfileSerializer, OrderItemSerializer
)
from .mpesa_service import MPesaService


# Auth Views
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                return Response({
                    'message': 'Login successful',
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response(
            {'message': 'Logout successful'},
            status=status.HTTP_200_OK
        )


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'user': UserSerializer(user).data,
            'profile': UserProfileSerializer(user.profile).data if hasattr(user, 'profile') else None
        })

    def put(self, request):
        user = request.user
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.email = request.data.get('email', user.email)
        user.save()

        if hasattr(user, 'profile'):
            profile = user.profile
            profile.phone_number = request.data.get('phone_number', profile.phone_number)
            profile.avatar_url = request.data.get('avatar_url', profile.avatar_url)
            profile.save()

        return Response(UserSerializer(user).data)


# ViewSets
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        user = self.get_object()
        return Response(UserSerializer(user).data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)

        if category:
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(description__icontains=search)

        return queryset

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        categories = [
            {'value': 'electronics', 'label': 'Electronics'},
            {'value': 'clothing', 'label': 'Clothing'},
            {'value': 'food', 'label': 'Food'},
            {'value': 'books', 'label': 'Books'},
            {'value': 'home', 'label': 'Home & Garden'},
            {'value': 'sports', 'label': 'Sports & Outdoors'},
            {'value': 'other', 'label': 'Other'},
        ]
        return Response(categories)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        items_data = request.data.get('items', [])
        shipping_address_id = request.data.get('shipping_address_id')
        payment_method = request.data.get('payment_method', 'mpesa')
        total_amount = request.data.get('total_amount', 0)

        if not items_data or not shipping_address_id:
            return Response(
                {'error': 'Items and shipping address are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            shipping_address = Address.objects.get(id=shipping_address_id, user=request.user)
        except Address.DoesNotExist:
            return Response(
                {'error': 'Shipping address not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        order = Order.objects.create(
            order_id=order_id,
            user=request.user,
            total_amount=total_amount,
            shipping_address=shipping_address,
            payment_method=payment_method
        )

        for item_data in items_data:
            product = get_object_or_404(Product, id=item_data.get('product_id'))
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data.get('quantity', 1),
                unit_price=product.price,
                total_price=product.price * item_data.get('quantity', 1)
            )

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.order_status not in ['pending', 'processing']:
            return Response(
                {'error': 'Cannot cancel this order'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.order_status = 'cancelled'
        order.save()
        return Response(OrderSerializer(order).data)


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.filter(is_published=True)
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        blog = self.get_object()
        blog.views += 1
        blog.save()
        return Response(BlogSerializer(blog).data)


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


# M-Pesa Views
class MPesaSTKPushView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        amount = request.data.get('amount')
        order_id = request.data.get('order_id')

        if not all([phone_number, amount, order_id]):
            return Response(
                {'error': 'Phone number, amount, and order_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        mpesa_service = MPesaService()
        result = mpesa_service.initiate_stk_push(phone_number, amount, order.order_id)

        if result.get('success'):
            return Response(result, status=status.HTTP_200_OK)
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


class MPesaCallbackView(APIView):
    permission_classes = [permissions.AllowAny]

    @csrf_exempt
    def post(self, request):
        try:
            data = json.loads(request.body)
            result = data.get('Body', {}).get('stkCallback', {})

            if result.get('ResultCode') == 0:
                merchant_request_id = result.get('MerchantRequestID')
                checkout_request_id = result.get('CheckoutRequestID')
                amount = result.get('CallbackMetadata', {}).get('Item', [{}])[0].get('Value')
                mpesa_receipt = result.get('CallbackMetadata', {}).get('Item', [])

                # Find the receipt number
                receipt = None
                for item in mpesa_receipt:
                    if item.get('Name') == 'MpesaReceiptNumber':
                        receipt = item.get('Value')

                # Update order and payment
                payments = Payment.objects.filter(stripe_data__checkout_request_id=checkout_request_id)
                for payment in payments:
                    payment.status = 'completed'
                    payment.mpesa_data = {'receipt': receipt, 'amount': amount}
                    payment.save()
                    payment.order.payment_status = 'completed'
                    payment.order.mpesa_receipt_number = receipt
                    payment.order.save()

            return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
        except Exception as e:
            print(f"Callback error: {str(e)}")
            return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Error'})


class StripeWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    @csrf_exempt
    def post(self, request):
        # Handle Stripe webhook
        try:
            event_data = json.loads(request.body)
            event_type = event_data.get('type')

            if event_type == 'payment_intent.succeeded':
                intent = event_data.get('data', {}).get('object', {})
                payment_intent_id = intent.get('id')

                orders = Order.objects.filter(stripe_payment_intent_id=payment_intent_id)
                for order in orders:
                    order.payment_status = 'completed'
                    order.order_status = 'processing'
                    order.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f"Webhook error: {str(e)}")
            return JsonResponse({'status': 'error'}, status=400)
