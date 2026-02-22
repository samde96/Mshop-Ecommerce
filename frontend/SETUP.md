# Frontend Setup Guide

This directory contains the Next.js frontend application for M-Shop eCommerce platform.

## Directory Structure

```
frontend/
├── app/                    # Next.js App Router
├── components/             # React components
├── hooks/                  # Custom React hooks (Django integration)
├── lib/                    # Utilities and helpers
├── public/                 # Static assets
├── styles/                 # Global styles
├── .env.local.example      # Environment variables template
└── package.json            # Dependencies
```

## Quick Start

1. Copy environment variables:
```bash
cp .env.local.example .env.local
```

2. Update `.env.local` with your Django API URL:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

3. Install dependencies:
```bash
npm install
```

4. Start development server:
```bash
npm run dev
```

Visit http://localhost:3000

## Available Hooks

The following custom hooks connect your frontend to the Django backend:

- `useDjangoAuth()` - Authentication (register, login, logout, user profile)
- `useDjangoProducts()` - Product management and browsing
- `useDjangoOrders()` - Order creation and management
- `useDjangoPayments()` - Payment processing and M-Pesa integration
- `useDjangoAddresses()` - Address management

## API Integration

All API calls go through `/lib/api-client.ts` which:
- Automatically handles authentication tokens
- Manages CORS headers
- Provides error handling
- Implements request/response interceptors

## Environment Variables

See `.env.local.example` for all required environment variables.
