# Overview

This is a Brazilian Import Tax Calculator web application built with Flask. It helps importers calculate all taxes, costs, and project profit margins when reselling imported products in Brazil. The application integrates with government APIs and currency conversion services to provide accurate, real-time calculations for import duties, taxes (II, IPI, PIS, COFINS, ICMS), and total landed costs.

The system supports user authentication, calculation history, saved scenarios, and provides a comprehensive dashboard for managing import analyses. It's designed for importers, tax consultants, and purchasing analysts who need to evaluate the economic viability of importing products to Brazil.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Web Framework
- **Flask**: Lightweight Python web framework chosen for rapid development and flexibility
- **Flask-SQLAlchemy**: ORM for database operations with PostgreSQL
- **Flask-Login**: User session management and authentication
- **Flask-WTF**: Form handling with built-in CSRF protection

## Frontend Architecture
- **Bootstrap 5**: CSS framework with dark theme for responsive UI
- **Feather Icons**: Consistent iconography throughout the application
- **Chart.js**: Data visualization for calculation results and analytics
- **Vanilla JavaScript**: Custom functionality for NCM search, form validation, and dynamic calculations

## Database Design
- **PostgreSQL**: Primary database for production environments
- **SQLAlchemy ORM**: Database abstraction layer with declarative models
- **User Management**: Authentication with password hashing using Werkzeug
- **Data Models**: Users, Calculations, Product Scenarios with proper relationships and cascading deletes

## Authentication & Authorization
- **Flask-Login**: Session-based authentication
- **Password Security**: Werkzeug password hashing with salt
- **User Types**: Support for IMPORTER, TAX_CONSULTANT, and ADMIN roles
- **Session Management**: Secure session handling with configurable secret keys

## Service Layer Architecture
- **Tax Calculator Service**: Implements Brazilian import tax rules (II, IPI, PIS, COFINS, ICMS)
- **Currency Service**: Multi-source exchange rate fetching with caching (AwesomeAPI, Brazilian Central Bank)
- **NCM Service**: Product classification code lookup with tax rate determination
- **Modular Design**: Separated business logic from web routes for maintainability

## Application Structure
- **MVC Pattern**: Clear separation between models, views (templates), and controllers (routes)
- **Service Layer**: Business logic abstracted into dedicated service classes
- **Form Validation**: Server-side validation with WTForms
- **Error Handling**: Custom error pages (404, 500) with user-friendly messaging

# External Dependencies

## APIs and External Services
- **AwesomeAPI**: Primary source for USD/BRL exchange rates
- **Brazilian Central Bank API**: Fallback currency service for official rates
- **Portal Único Siscomex**: Government API integration planned for NCM tax rates (currently using static database)

## Third-Party Libraries
- **Bootstrap 5**: Frontend CSS framework from CDN
- **Feather Icons**: Icon library from CDN
- **Chart.js**: JavaScript charting library from CDN
- **Flask Extensions**: SQLAlchemy, Login, WTF for core functionality

## Database
- **PostgreSQL**: Production database with connection pooling
- **SQLite**: Development fallback option
- **Database Features**: Connection pooling, pre-ping health checks, automatic table creation

## Environment Configuration
- **Environment Variables**: DATABASE_URL, SESSION_SECRET for deployment flexibility
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies
- **Debug Mode**: Configurable for development vs production environments