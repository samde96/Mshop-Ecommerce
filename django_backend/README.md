# M-Shop Django Backend

A Django REST Framework backend for the M-Shop e-commerce application.

## Setup Instructions

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- pip and virtualenv

### Installation

1. **Clone the repository and navigate to django_backend:**
```bash
cd django_backend
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create environment file:**
```bash
cp .env.example .env
```

5. **Update `.env` with your configuration:**
   - Set PostgreSQL database credentials
   - Add M-Pesa credentials
   - Add Stripe API keys

6. **Run migrations:**
```bash
python manage.py migrate
```

7. **Create superuser:**
```bash
python manage.py createsuperuser
```

8. **Collect static files:**
```bash
python manage.py collectstatic --noinput
```

9. **Run development server:**
```bash
python manage.py runserver 0.0.0.0:8000
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create product (authenticated)
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product
- `GET /api/products/categories/` - Get product categories

### Orders
- `GET /api/orders/` - List user orders
- `POST /api/orders/` - Create order
- `GET /api/orders/{id}/` - Get order details
- `POST /api/orders/{id}/cancel/` - Cancel order

### Addresses
- `GET /api/addresses/` - List user addresses
- `POST /api/addresses/` - Create address
- `PUT /api/addresses/{id}/` - Update address
- `DELETE /api/addresses/{id}/` - Delete address

### Blog
- `GET /api/blog/` - List published blog posts
- `GET /api/blog/{id}/` - Get blog post details
- `POST /api/blog/{id}/increment_views/` - Increment post views

### Payments
- `POST /api/payments/mpesa/stkpush/` - Initiate M-Pesa STK push
- `POST /api/payments/mpesa/callback/` - M-Pesa callback handler
- `POST /api/payments/stripe/webhook/` - Stripe webhook handler

## Admin Panel

Access Django admin at `http://localhost:8000/admin/` with your superuser credentials.

## Database Schema

The application uses the following main models:
- **User** - Django built-in user model
- **UserProfile** - Extended user profile
- **Product** - Product listings
- **Order** - Customer orders
- **OrderItem** - Items in an order
- **Address** - Shipping addresses
- **Payment** - Payment transactions
- **Blog** - Blog posts

## Running Tests

```bash
python manage.py test
```

## Deployment

For production deployment, follow these steps:

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` in `settings.py`
3. Use PostgreSQL instead of SQLite
4. Set strong `DJANGO_SECRET_KEY`
5. Use environment-specific settings
6. Run with Gunicorn: `gunicorn mshop.wsgi`
