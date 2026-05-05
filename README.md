# Multi-Vendor E-Commerce Platform

Production-style multi-vendor e-commerce platform built with Django, focused on real-world backend architecture, business logic, and system design.

---

## Project Overview

This project simulates a real e-commerce system with multiple sellers, full order lifecycle, inventory consistency, payment handling, and seller payouts.

It is built in two stages:

1. **Django Full-Stack (Completed)**
2. **Django REST Framework (Planned)**

---

## Tech Stack

* Django
* PostgreSQL
* Redis
* Celery (ready setup)
* Docker / Docker Compose
* Pytest
* Tailwind CSS
* SMTP (email)

---

## Architecture

The project follows a **modular monolith** architecture with clear separation of concerns:

* Thin views (HTTP layer only)
* Service layer for business logic
* Selector layer for read/query logic
* Tasks for async processing
* Models for data layer

```
views.py      → request/response handling  
forms.py      → validation  
services.py   → business logic  
selectors.py  → read/query logic  
tasks.py      → background jobs  
models.py     → database schema  
```

---

## Apps Structure

```
apps/
    common/
    users/
    shops/
    catalog/
    inventory/
    cart/
    orders/
    payments/
    promotions/
    notifications/
    reviews/
    shipping/
    analytics_app/
    payouts/
    backoffice/
```

---

## Features

### User Roles

* Customer
* Seller
* Admin

### Core Modules

* Authentication (register/login)
* Seller shop management
* Product & variant system
* Variant-specific product images
* Cart & checkout
* Order lifecycle management
* Mock payment gateway
* Shipping system
* Coupon system
* Reviews
* Notifications & email logs
* Seller payouts
* Custom backoffice panel

---

## Key Business Logic

### Inventory Management

Stock is handled using reservation:

* On checkout → stock is reserved
* On payment success → stock is finalized
* On payment fail/cancel → stock is released

```
available = total_stock - reserved_stock
```

Prevents overselling and race conditions.

---

### Payment Flow

Mock payment gateway with idempotent callbacks:

* Prevents duplicate processing
* Ensures consistent state

```
success → order = paid  
fail/cancel → order = payment_failed
```

---

### Order & Shipment Logic

* Seller controls **order item status**
* Admin controls **shipment status**
* Order becomes **delivered only when ALL conditions are met**

---

### Seller Payout System

Seller balance is calculated from:

```
delivered items revenue
- paid payouts
- pending payouts
```

Prevents:

* negative balance
* double payouts

---

### Security

* Role-based access control (RBAC)
* Seller isolation (cannot access others’ data)
* Address ownership validation
* Admin role cannot be self-assigned during registration

---

## Backoffice Panel

Custom admin panel for non-technical users:

* User management
* Shop approval/blocking
* Product moderation
* Order & payment monitoring
* Payout management
* Coupon & shipping configuration
* Notifications & logs

---

## Testing

Comprehensive test suite using **pytest** (~70+ tests):

Covered areas:

* Inventory logic
* Payment flows & idempotency
* Order status transitions
* Shipment rules
* Seller payouts
* Permissions & security
* Coupon validation
* Catalog logic

Run tests:

```bash
docker compose exec web pytest
```

---

## Local Setup

### 1. Clone

```bash
git clone <your-repo-url>
cd multi_vendor_ecommerce
```

### 2. Environment

Create `.env`:

```env
DEBUG=True
SECRET_KEY=change-me

POSTGRES_DB=ecommerce_db
POSTGRES_USER=ecommerce_user
POSTGRES_PASSWORD=ecommerce_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

DATABASE_URL=postgres://ecommerce_user:ecommerce_password@db:5432/ecommerce_db

REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

### 3. Run Project

```bash
docker compose up --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

---

## Project Status

Current state:

* Django full-stack version completed
* Core business logic implemented
* Custom backoffice ready
* Email system working
* Test suite implemented
* DRF API layer planned

---

## Future Improvements

* Django REST Framework API
* JWT authentication
* API documentation
* Production deployment
* Media storage (S3)
* CI/CD pipeline
* Advanced analytics
* Refund system
* Commission system

---

## Summary

This project demonstrates:

* Real-world backend architecture
* Complex business logic implementation
* Strong testing practices
* Production-oriented design

---
