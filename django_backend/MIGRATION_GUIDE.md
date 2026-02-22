# Django Backend Migration Guide

This guide explains how to migrate from the Express.js backend to Django and update your Next.js frontend.

## Quick Start

### 1. Setup Django Backend

```bash
# Navigate to django_backend directory
cd django_backend

# Run initialization script
# On macOS/Linux:
chmod +x init_django.sh
./init_django.sh

# On Windows:
init_django.bat
```

### 2. Configure Environment Variables

Create a `.env` file in the `django_backend` directory:

```bash
cp .env.example .env
```

Update the `.env` file with:
- PostgreSQL database credentials
- M-Pesa API credentials
- Stripe API keys

### 3. Migrate Data from MongoDB

```bash
cd django_backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python migrate_from_mongodb.py
```

### 4. Run Django Development Server

```bash
python manage.py runserver 0.0.0.0:8000
```

The API will be available at `http://localhost:8000/api/`

---

## Frontend Integration Steps

### Step 1: Update Environment Variables

Update `.env.local` in the Next.js project:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Step 2: Create API Client

Create `/lib/api-client.ts` for API communication:

```typescript
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

// Add token to requests if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
```

### Step 3: Update Authentication

Replace Clerk with Django built-in authentication:

```typescript
// Example: Login with Django
async function loginWithDjango(username: string, password: string) {
  try {
    const response = await apiClient.post('/auth/login/', {
      username,
      password
    });
    
    localStorage.setItem('auth_token', response.data.token);
    return response.data.user;
  } catch (error) {
    console.error('Login failed:', error);
  }
}
```

### Step 4: Update API Calls

Replace all API calls with Django endpoints:

#### Old (Express):
```typescript
const response = await fetch('http://localhost:5000/api/products/list');
```

#### New (Django):
```typescript
const response = await apiClient.get('/products/');
```

### Step 5: Update Product Fetching

```typescript
// Fetch all products
export async function getProducts() {
  const response = await apiClient.get('/products/');
  return response.data.results;
}

// Search products
export async function searchProducts(query: string) {
  const response = await apiClient.get('/products/', {
    params: { search: query }
  });
  return response.data.results;
}

// Filter by category
export async function getProductsByCategory(category: string) {
  const response = await apiClient.get('/products/', {
    params: { category }
  });
  return response.data.results;
}
```

### Step 6: Update Order Management

```typescript
// Create order
export async function createOrder(items: any[], addressId: number) {
  const response = await apiClient.post('/orders/', {
    items,
    shipping_address_id: addressId,
    payment_method: 'mpesa',
    total_amount: calculateTotal(items)
  });
  return response.data;
}

// Get user orders
export async function getUserOrders() {
  const response = await apiClient.get('/orders/');
  return response.data.results;
}

// Cancel order
export async function cancelOrder(orderId: number) {
  const response = await apiClient.post(`/orders/${orderId}/cancel/`);
  return response.data;
}
```

### Step 7: Update Payment Processing

```typescript
// M-Pesa STK Push
export async function initiateMpesaPayment(phoneNumber: string, amount: number, orderId: number) {
  const response = await apiClient.post('/payments/mpesa/stkpush/', {
    phone_number: phoneNumber,
    amount,
    order_id: orderId
  });
  return response.data;
}
```

### Step 8: Update User Profile

```typescript
// Get user profile
export async function getUserProfile() {
  const response = await apiClient.get('/auth/profile/');
  return response.data;
}

// Update user profile
export async function updateUserProfile(data: any) {
  const response = await apiClient.put('/auth/profile/', data);
  return response.data;
}
```

### Step 9: Update Address Management

```typescript
// Get user addresses
export async function getUserAddresses() {
  const response = await apiClient.get('/addresses/');
  return response.data.results;
}

// Create address
export async function createAddress(addressData: any) {
  const response = await apiClient.post('/addresses/', addressData);
  return response.data;
}

// Update address
export async function updateAddress(addressId: number, data: any) {
  const response = await apiClient.put(`/addresses/${addressId}/`, data);
  return response.data;
}

// Delete address
export async function deleteAddress(addressId: number) {
  await apiClient.delete(`/addresses/${addressId}/`);
}
```

### Step 10: Update Blog Fetching

```typescript
// Get published blog posts
export async function getBlogPosts(page = 1) {
  const response = await apiClient.get('/blog/', {
    params: { page }
  });
  return response.data;
}

// Get blog post by ID
export async function getBlogPost(id: number) {
  const response = await apiClient.get(`/blog/${id}/`);
  return response.data;
}

// Increment blog views
export async function incrementBlogViews(id: number) {
  const response = await apiClient.post(`/blog/${id}/increment_views/`);
  return response.data;
}
```

---

## API Endpoint Changes Reference

### Authentication Endpoints

| Old (Express) | New (Django) |
|---|---|
| N/A | POST `/auth/register/` |
| N/A | POST `/auth/login/` |
| N/A | POST `/auth/logout/` |
| N/A | GET `/auth/profile/` |
| N/A | PUT `/auth/profile/` |

### Product Endpoints

| Old | New |
|---|---|
| GET `/api/products/list` | GET `/products/` |
| GET `/api/products/{id}` | GET `/products/{id}/` |
| POST `/api/products/create` | POST `/products/` |
| GET `/api/products/categories` | GET `/products/categories/` |

### Order Endpoints

| Old | New |
|---|---|
| POST `/api/orders/place` | POST `/orders/` |
| GET `/api/orders/{userId}` | GET `/orders/` |
| GET `/api/orders/{id}` | GET `/orders/{id}/` |
| N/A | POST `/orders/{id}/cancel/` |

### Address Endpoints

| Old | New |
|---|---|
| GET `/api/addresses/{userId}` | GET `/addresses/` |
| POST `/api/addresses/add` | POST `/addresses/` |
| PUT `/api/addresses/{id}` | PUT `/addresses/{id}/` |
| DELETE `/api/addresses/{id}` | DELETE `/addresses/{id}/` |

### Payment Endpoints

| Old | New |
|---|---|
| POST `/api/mpesa/stkpush` | POST `/payments/mpesa/stkpush/` |
| POST `/api/mpesa/callback` | POST `/payments/mpesa/callback/` |

---

## Database Schema Mapping

### Users

**MongoDB:**
```javascript
{
  _id: String,
  clerkId: String,
  name: String,
  email: String,
  imageUrl: String,
  cartItems: Object,
  wishList: Object
}
```

**PostgreSQL (Django):**
```python
# User (built-in Django model)
id, username, email, first_name, last_name, password

# UserProfile (custom model)
user_id, phone_number, clerkId, role, avatar_url
```

### Products

**MongoDB:**
```javascript
{
  _id: ObjectId,
  userId: String,
  name: String,
  description: String,
  price: Number,
  offerPrice: Number,
  image: Array,
  category: String,
  stockStatus: String,
  color: String,
  brand: String
}
```

**PostgreSQL (Django):**
```python
{
  id, name, description, price, category, image_url,
  stock, seller_id, is_active, created_at, updated_at
}
```

---

## Testing the Migration

### 1. Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Get products
curl http://localhost:8000/api/products/

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}'
```

### 2. Test Frontend Integration

- Visit `http://localhost:3000`
- Register a new account
- Browse products
- Create an order
- Initiate M-Pesa payment

### 3. Monitor Logs

Django development server logs:
```bash
# Check console output from Django server
```

Browser console:
- Check Network tab for API requests
- Look for any CORS or auth errors

---

## Troubleshooting

### CORS Errors

Update `CORS_ALLOWED_ORIGINS` in `django_backend/mshop/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://yourdomain.com",  # Add your production domain
]
```

### Database Connection Issues

1. Verify PostgreSQL is running
2. Check database credentials in `.env`
3. Run migrations: `python manage.py migrate`

### Authentication Errors

- Clear browser cookies and localStorage
- Ensure tokens are being stored correctly
- Check token expiration

### M-Pesa Integration

- Verify credentials in `.env`
- Check M-Pesa environment (sandbox vs production)
- Review callback logs

---

## Deployment

### Production Checklist

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` in `settings.py`
3. Use strong `DJANGO_SECRET_KEY`
4. Configure PostgreSQL with backups
5. Use environment-specific settings
6. Enable HTTPS/SSL
7. Update CORS for production domain
8. Run security checks: `python manage.py check --deploy`

### Deploy to Vercel

1. Create separate repository for Django backend
2. Configure environment variables in Vercel
3. Use Gunicorn for production server
4. Point frontend to production API URL

---

## Support

For issues or questions:
1. Check API_DOCUMENTATION.md for endpoint details
2. Review Django logs for error messages
3. Test with curl or Postman
4. Check browser Network tab for API responses
