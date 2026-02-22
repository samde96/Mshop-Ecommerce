"""
URL configuration for mshop project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'addresses', views.AddressViewSet, basename='address')
router.register(r'blog', views.BlogViewSet, basename='blog')
router.register(r'payments', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include([
        path('register/', views.RegisterView.as_view(), name='register'),
        path('login/', views.LoginView.as_view(), name='login'),
        path('logout/', views.LogoutView.as_view(), name='logout'),
        path('profile/', views.ProfileView.as_view(), name='profile'),
    ])),
    path('api/payments/', include([
        path('mpesa/stkpush/', views.MPesaSTKPushView.as_view(), name='mpesa_stkpush'),
        path('mpesa/callback/', views.MPesaCallbackView.as_view(), name='mpesa_callback'),
        path('stripe/webhook/', views.StripeWebhookView.as_view(), name='stripe_webhook'),
    ])),
]
