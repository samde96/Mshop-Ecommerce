# M-Shop eCommerce Platform

A full-stack eCommerce application built with **Next.js** frontend and **Django** backend, featuring M-Pesa payment integration.

## Project Structure

```
mshop-ecommerce/
├── django_backend/            # Django REST API
│   ├── api/                   # REST API application
│   ├── mshop/                 # Django project settings
│   ├── scripts/               # Migration and setup scripts
│   ├── docs/                  # API documentation
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Backend setup guide
│
├── frontend/                   # Next.js frontend application
│   ├── app/                   # App Router pages
│   ├── components/            # React components
│   ├── hooks/                 # Custom Django integration hooks
│   ├── lib/                   # Utilities (API client, etc.)
│   ├── public/                # Static assets
│   ├── styles/                # Global styles
│   ├── package.json           # Node dependencies
│   └── SETUP.md               # Frontend setup guide
│
├── QUICK_START.md             # Get started in 5 minutes
├── MIGRATION_COMPLETE.md      # Migration details
└── IMPLEMENTATION_CHECKLIST.md # Verification checklist
```

## Quick Start

### Option 1: Run Both Locally (Recommended for Development)

**Backend Setup:**
```bash
cd django_backend
bash scripts/init_django.sh  # macOS/Linux
# or
scripts\init_django.bat      # Windows

# Then start the server
python manage.py runserver 0.0.0.0:8000
```

**Frontend Setup:**
```bash
cd frontend
cp .env.local.example .env.local
# Edit .env.local and set NEXT_PUBLIC_API_URL=http://localhost:8000/api

npm install
npm run dev
```

Visit:
- Frontend: http://localhost:3000
- Backend Admin: http://localhost:8000/admin
- API: http://localhost:8000/api

## Key Features

- **Authentication**: JWT-based authentication with Django built-in auth
- **Products**: Full product catalog with filtering and search
- **Orders**: Order management with status tracking
- **Payments**: M-Pesa STK Push integration for mobile payments
- **Addresses**: User address management
- **Blog**: Content management system
- **Admin Panel**: Django admin interface for data management

## Technology Stack

### Backend
- Django 4.2.11
- Django REST Framework
- PostgreSQL
- Python 3.9+

### Frontend
- Next.js 15+
- React 19+
- TypeScript
- Tailwind CSS
- ShadcN/UI

## API Documentation

Full API documentation is available at:
- `django_backend/docs/API_REFERENCE.md` - Complete endpoint reference
- `django_backend/MIGRATION_GUIDE.md` - Migration guide from MongoDB

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Backend (.env)
```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/mshop
MPESA_CONSUMER_KEY=your-mpesa-key
MPESA_CONSUMER_SECRET=your-mpesa-secret
```

See `django_backend/.env.example` for complete backend environment variables.

## Data Migration

To migrate data from MongoDB to PostgreSQL:

```bash
cd django_backend
python scripts/migrate_from_mongodb.py
```

This script will:
- Connect to your MongoDB instance
- Create PostgreSQL tables via Django ORM
- Migrate all users, products, orders, and blogs
- Preserve Clerk IDs for backward compatibility

## Custom Hooks (Frontend)

Use these React hooks for API integration:

```typescript
// Authentication
const { user, register, login, logout } = useDjangoAuth();

// Products
const { products, loading } = useDjangoProducts();

// Orders
const { orders, createOrder } = useDjangoOrders();

// Payments
const { initiatePayment } = useDjangoPayments();

// Addresses
const { addresses, addAddress } = useDjangoAddresses();
```

## API Client

All API requests use the centralized client in `frontend/lib/api-client.ts`:
- Automatic authentication token management
- CORS header handling
- Error handling and logging
- Request/response interceptors

## Development

### Backend Development
```bash
cd django_backend
source venv/bin/activate  # Activate virtual environment
python manage.py runserver
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Running Tests

**Backend:**
```bash
cd django_backend
python manage.py test
```

**Frontend:**
```bash
cd frontend
npm test
```

## Additional Documentation

- `QUICK_START.md` - Quick reference guide
- `MIGRATION_COMPLETE.md` - Complete migration details
- `IMPLEMENTATION_CHECKLIST.md` - Verification checklist
- `django_backend/README.md` - Backend-specific guide
- `frontend/SETUP.md` - Frontend-specific guide

## Support

For issues or questions:
1. Check the documentation files
2. Review the API reference
3. Check Django admin panel
4. Review browser console for frontend errors

## License

MIT License - See LICENSE file for details
