from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product, Order, Address, UserProfile


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='testpass123')
        self.profile = UserProfile.objects.create(user=self.user, phone_number='254712345678', role='user')

    def test_user_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.phone_number, '254712345678')


class ProductTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='seller', email='seller@test.com', password='testpass123')
        self.product = Product.objects.create(
            name='Test Product',
            description='A test product',
            price=1000.00,
            category='electronics',
            image_url='http://example.com/image.jpg',
            stock=10,
            seller=self.user
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, 1000.00)
        self.assertEqual(self.product.stock, 10)


class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', email='buyer@test.com', password='testpass123')
        self.address = Address.objects.create(
            user=self.user,
            name='Test Address',
            phone='254712345678',
            street='123 Main St',
            city='Nairobi',
            postal_code='00100',
            country='Kenya'
        )
        self.order = Order.objects.create(
            order_id='ORD-12345678',
            user=self.user,
            total_amount=5000.00,
            shipping_address=self.address,
            payment_method='mpesa'
        )

    def test_order_creation(self):
        self.assertEqual(self.order.order_id, 'ORD-12345678')
        self.assertEqual(self.order.order_status, 'pending')
        self.assertEqual(self.order.payment_status, 'pending')
