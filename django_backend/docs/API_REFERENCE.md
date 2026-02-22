# M-Shop Django REST API Documentation

Base URL: `http://localhost:8000/api/`

## Authentication

Most endpoints require authentication. Use Session Authentication or Token-based auth.

### Login/Register Endpoints

#### Register User
```
POST /auth/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "254712345678"
}

Response (201):
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

#### Login
```
POST /auth/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword123"
}

Response (200):
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

#### Get Profile
```
GET /auth/profile/
Authorization: Bearer <token> or Cookie-based session
Response (200): User and profile details
```

#### Update Profile
```
PUT /auth/profile/
Authorization: Bearer <token>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "newemail@example.com",
  "phone_number": "254712345678",
  "avatar_url": "https://example.com/avatar.jpg"
}

Response (200): Updated user details
```

#### Logout
```
POST /auth/logout/
Authorization: Bearer <token>
Response (200): {"message": "Logout successful"}
```

---

## Products API

### List Products
```
GET /products/
Query Parameters:
  - category: string (electronics, clothing, food, books, home, sports, other)
  - search: string (search in name and description)
  - page: integer (pagination)

Response (200):
{
  "count": 100,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Product Name",
      "description": "Product description",
      "price": "1000.00",
      "category": "electronics",
      "image_url": "https://example.com/image.jpg",
      "stock": 10,
      "seller": 1,
      "seller_name": "john_doe",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Get Product Details
```
GET /products/{id}/
Response (200): Product object
```

### Create Product (Authenticated)
```
POST /products/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "New Product",
  "description": "Product description",
  "price": "1500.00",
  "category": "electronics",
  "image_url": "https://example.com/image.jpg",
  "stock": 20
}

Response (201): Created product object
```

### Update Product
```
PUT /products/{id}/
PATCH /products/{id}/
Authorization: Bearer <token>
Content-Type: application/json

Response (200): Updated product object
```

### Delete Product
```
DELETE /products/{id}/
Authorization: Bearer <token>
Response (204): No content
```

### Get Product Categories
```
GET /products/categories/
Response (200):
[
  {"value": "electronics", "label": "Electronics"},
  {"value": "clothing", "label": "Clothing"},
  ...
]
```

---

## Orders API

### List User Orders
```
GET /orders/
Authorization: Bearer <token>

Response (200):
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "order_id": "ORD-ABC12345",
      "user": 1,
      "total_amount": "5000.00",
      "tax_amount": "500.00",
      "shipping_amount": "0.00",
      "order_status": "pending",
      "payment_status": "pending",
      "payment_method": "mpesa",
      "items": [
        {
          "id": 1,
          "product": {...},
          "quantity": 2,
          "unit_price": "2000.00",
          "total_price": "4000.00"
        }
      ],
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Get Order Details
```
GET /orders/{id}/
Authorization: Bearer <token>
Response (200): Order object with items
```

### Create Order
```
POST /orders/
Authorization: Bearer <token>
Content-Type: application/json

{
  "items": [
    {"product_id": 1, "quantity": 2},
    {"product_id": 2, "quantity": 1}
  ],
  "shipping_address_id": 1,
  "payment_method": "mpesa",
  "total_amount": "5000.00"
}

Response (201): Created order object
```

### Cancel Order
```
POST /orders/{id}/cancel/
Authorization: Bearer <token>
Response (200): Updated order object with cancelled status
```

---

## Addresses API

### List User Addresses
```
GET /addresses/
Authorization: Bearer <token>

Response (200):
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "name": "Home",
      "phone": "254712345678",
      "street": "123 Main St",
      "city": "Nairobi",
      "state": "",
      "postal_code": "00100",
      "country": "Kenya",
      "is_default": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Create Address
```
POST /addresses/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Home",
  "phone": "254712345678",
  "street": "123 Main St",
  "city": "Nairobi",
  "postal_code": "00100",
  "country": "Kenya",
  "is_default": true
}

Response (201): Created address object
```

### Update Address
```
PUT /addresses/{id}/
PATCH /addresses/{id}/
Authorization: Bearer <token>
Response (200): Updated address object
```

### Delete Address
```
DELETE /addresses/{id}/
Authorization: Bearer <token>
Response (204): No content
```

---

## Blog API

### List Published Blog Posts
```
GET /blog/
Query Parameters:
  - page: integer
  - category: string

Response (200):
{
  "count": 20,
  "results": [
    {
      "id": 1,
      "title": "Blog Post Title",
      "slug": "blog-post-title",
      "content": "Full content...",
      "excerpt": "Short excerpt...",
      "author": 1,
      "author_name": "john_doe",
      "image_url": "https://example.com/image.jpg",
      "category": "tutorial",
      "is_published": true,
      "views": 150,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Get Blog Post
```
GET /blog/{id}/
Response (200): Blog post object
```

### Increment Blog Views
```
POST /blog/{id}/increment_views/
Response (200): Updated blog post object
```

---

## Payment API

### M-Pesa STK Push
```
POST /payments/mpesa/stkpush/
Authorization: Bearer <token>
Content-Type: application/json

{
  "phone_number": "254712345678",
  "amount": 5000,
  "order_id": 1
}

Response (200):
{
  "success": true,
  "message": "STK push initiated successfully",
  "data": {
    "MerchantRequestID": "...",
    "CheckoutRequestID": "...",
    "ResponseCode": "0",
    "ResponseDescription": "Success"
  }
}
```

### M-Pesa Callback
```
POST /payments/mpesa/callback/
Content-Type: application/json

{
  "Body": {
    "stkCallback": {
      "MerchantRequestID": "...",
      "CheckoutRequestID": "...",
      "ResultCode": 0,
      "ResultDesc": "...",
      "CallbackMetadata": {
        "Item": [...]
      }
    }
  }
}

Response (200): Callback accepted
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Error message",
  "details": "Additional details"
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid credentials or token required"
}
```

### 403 Forbidden
```json
{
  "error": "You don't have permission to perform this action"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Rate Limiting

Currently not enforced. Production deployment should include rate limiting.

## Pagination

Default page size: 10 items per page
Use `?page=2` to get the next page.

## Filtering and Searching

Products support:
- Filter by category: `?category=electronics`
- Search: `?search=iphone`

Blog posts support:
- Filter by category: `?category=tutorial`

## CORS

CORS is enabled for `http://localhost:3000` for development.
Update `CORS_ALLOWED_ORIGINS` in `settings.py` for production.
