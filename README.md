# Multi-Vendor E-Commerce Platform

Production-like multi-vendor e-commerce project built in two stages:

1. Django Full-Stack
2. Django REST Framework

## Tech Stack

- Django
- PostgreSQL
- Redis
- Celery
- Docker
- Pytest

## Architecture

This project follows a modular monolith architecture:

- thin views
- services for business logic
- selectors for read/query logic
- tasks for async processing

## Apps

- common
- users
- shops
- catalog
- inventory
- cart
- orders
- payments
- promotions
- notifications
- reviews
- shipping
- analytics_app