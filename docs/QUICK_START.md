# Quick Start Guide - Django Backend

## TL;DR - Get Running in 5 Minutes

### Prerequisites
- Python 3.10+
- PostgreSQL installed and running
- Node.js/npm (for frontend)

### 1. Setup Django Backend

```bash
cd django_backend

# macOS/Linux
chmod +x init_django.sh && ./init_django.sh

# Windows
init_django.bat
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your PostgreSQL credentials and M-Pesa keys
# Required fields:
# - DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
# - MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET, MPESA_SHORTCODE
```

### 3. Run Database Migrations

```bash
cd django_backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python manage.py migrate
```

### 4. Create Admin User

```bash
python manage.py createsuperuser
# Enter username, email, password when prompted
```

### 5. Start Backend Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Backend is now running at: `http://localhost:8000/api/`
Admin panel: `http://localhost:8000/admin/`

### 6. Setup Frontend

```bash
# In project root
cp .env.local.example .env.local

# Update NEXT_PUBLIC_API_URL
# NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 7. Start Frontend (in new terminal)

```bash
npm run dev
# Frontend runs at http://localhost:3000
```

---

## Common Commands

### Backend

```bash
# Start development server
python manage.py runserver 0.0.0.0:8000

# Run migrations
python manage.py migrate

# Create new migration
python manage.py makemigrations

# Access Django admin
python manage.py createsuperuser

# Run tests
python manage.py test

# Migrate data from MongoDB
python migrate_from_mongodb.py

# Collect static files (production)
python manage.py collectstatic --noinput
```

### Frontend

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Run production server
npm start

# Run linting
npm run lint
```

---

## Test API Endpoints

### Test Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Test Get Products
```bash
curl http://localhost:8000/api/products/
```

### Test Create Address
```bash
curl -X POST http://localhost:8000/api/addresses/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "Home",
    "phone": "254712345678",
    "street": "123 Main St",
    "city": "Nairobi",
    "postal_code": "00100",
    "country": "Kenya"
  }'
```

---

## Frontend Hook Usage

### Login
```typescript
import { useDjangoAuth } from '@/hooks/use-django-auth';

const { login } = useDjangoAuth();
await login('username', 'password');
```

### Get Products
```typescript
import { useDjangoProducts } from '@/hooks/use-django-products';

const { products, getProducts } = useDjangoProducts();
useEffect(() => {
  getProducts();
}, []);
```

### Create Order
```typescript
import { useDjangoOrders } from '@/hooks/use-django-orders';

const { createOrder } = useDjangoOrders();
await createOrder(items, addressId, totalAmount);
```

### M-Pesa Payment
```typescript
import { useDjangoPayments } from '@/hooks/use-django-payments';

const { initiateMpesaPayment } = useDjangoPayments();
await initiateMpesaPayment(phoneNumber, amount, orderId);
```

---

## Troubleshooting

### Port Already in Use
```bash
# Django
python manage.py runserver 0.0.0.0:8001

# Frontend
npm run dev -- -p 3001
```

### Database Connection Failed
```bash
# Check PostgreSQL is running
# Check .env credentials
# Verify database exists
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or in virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

### CORS Error
- Update `CORS_ALLOWED_ORIGINS` in `django_backend/mshop/settings.py`
- Add your frontend URL (default: `http://localhost:3000`)

---

## Full Documentation

- **Backend Setup**: `django_backend/README.md`
- **API Documentation**: `django_backend/API_DOCUMENTATION.md`
- **Migration Guide**: `DJANGO_MIGRATION_GUIDE.md`
- **Implementation Details**: `IMPLEMENTATION_SUMMARY.md`

---

## Next Steps

1. Create a user account via `/api/auth/register/`
2. Browse products at `/api/products/`
3. Create an address at `/api/addresses/`
4. Place an order at `/api/orders/`
5. Initiate payment at `/api/payments/mpesa/stkpush/`

Enjoy your new Django backend!
