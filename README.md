# IGI Insurance Automation System

Complete backend-driven insurance automation system for IGI Insurance to streamline motor insurance policy issuance and management.

## 📖 Documentation

- **🚀 [Getting Started Guide](GETTING_STARTED.md)** - **START HERE!** Complete setup instructions for new users
- **🔧 [Troubleshooting Guide](TROUBLESHOOTING.md)** - Solutions for common issues and errors
- **📋 [Implementation Summary](IMPLEMENTATION_SUMMARY.md)** - Technical architecture and features
- **🔒 [Security Fixes](SECURITY_FIXES.md)** - Security patches and updates

## ⚡ Quick Start

**Prerequisites:** Docker Desktop installed on your system

```bash
# 1. Clone the repository
git clone https://github.com/tahakhan-22/igi-insurance-automation.git
cd igi-insurance-automation

# 2. Configure environment
cp .env.example .env
# Edit .env with your credentials (optional for testing)

# 3. Start the application
docker compose up --build

# 4. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**First time setup?** → Read the **[Getting Started Guide](GETTING_STARTED.md)** for detailed instructions!

## ✨ Key Features

### Policy Management
- ✅ Complete CRUD operations for 15+ entities (clients, policies, vehicles, perils, clauses, etc.)
- ✅ Multi-module data entry with real-time validations
- ✅ Automated premium calculations (percentage, flat, per-mille basis)
- ✅ Engine/chassis number duplicate detection
- ✅ Agency apportionment validation (must sum to 100%)

### Document Generation
- 📄 Professional PDF policy documents
- 📄 IGI-branded cover letters
- 📄 Professional HTML templates with WeasyPrint conversion

### Automation
- 🔄 **CSV Payment Reminders:** Daily job at 8 AM parsing due payments, sending email/SMS
- 📧 **Gmail Integration:** OAuth 2.0 authenticated, auto-classifies car insurance emails, extracts vehicle data, creates draft policies
- ⏰ APScheduler background jobs running automatically

### API & Integration
- 🚀 60+ RESTful API endpoints with full CRUD
- 📚 Interactive API documentation at `/docs`
- 🔐 OAuth 2.0 for Gmail (no password storage)
- ✉️ SMTP email service with professional templates
- 📱 SMS service (mock implementation, ready for real gateway)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │  PostgreSQL  │  │   Backend    │  │    Frontend     │ │
│  │  Database    │◄─┤  FastAPI +   │◄─┤   React +       │ │
│  │              │  │  Python      │  │   TypeScript    │ │
│  └──────────────┘  └──────┬───────┘  └─────────────────┘ │
│                            │                               │
│                    ┌───────▼────────┐                      │
│                    │  APScheduler   │                      │
│                    │  - Reminders   │                      │
│                    │  - Gmail Poll  │                      │
│                    └────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **ORM:** SQLAlchemy with PostgreSQL 15
- **Validation:** Pydantic schemas
- **PDF Generation:** Jinja2 templates + WeasyPrint
- **Automation:** APScheduler
- **Email:** aiosmtplib (SMTP)
- **APIs:** Gmail API with OAuth 2.0

### Frontend
- **Framework:** React 18
- **Language:** TypeScript
- **Build Tool:** Vite
- **HTTP Client:** Axios
- **Styling:** Custom CSS with IGI branding

### DevOps
- **Containerization:** Docker + Docker Compose
- **Database:** PostgreSQL 15 with health checks
- **Hot Reload:** Enabled for both backend and frontend

## 📊 Project Statistics

- **Backend Files:** 53 Python modules
- **Database Models:** 15 SQLAlchemy models with relationships
- **API Endpoints:** 60+ RESTful endpoints
- **Business Services:** 9 service modules
- **Automation Jobs:** 2 APScheduler jobs
- **Templates:** 3 professional Jinja2 templates
- **Frontend:** 6 TypeScript/React components

## 🎯 Use Cases

1. **Policy Creation:** Complete motor insurance policy workflow from client to final PDF
2. **Premium Calculation:** Automated calculations with multiple perils, charges, and discounts
3. **Payment Reminders:** Automated email/SMS reminders for due payments
4. **Email Processing:** Auto-create policies from incoming car insurance inquiry emails
5. **Document Generation:** Generate professional policy documents and cover letters

## 🔐 Security

- ✅ All identified vulnerabilities patched
- ✅ Input validation via Pydantic schemas
- ✅ OAuth 2.0 for Gmail (no password storage)
- ✅ Environment variables for secrets
- ✅ SQL injection prevention via SQLAlchemy
- ✅ CORS configured for frontend access

See [SECURITY_FIXES.md](SECURITY_FIXES.md) for details.

## 📱 API Endpoints

Full CRUD operations available for:
- Clients, Policies, Banks, Product Setup
- Items, Perils, Vehicles, Discounts
- Deductibles, Clauses, Warranties, Agencies
- Computational Sheet, Final Policy, Reminders
- Gmail Integration

**Interactive Documentation:** http://localhost:8000/docs

## 🧪 Testing

### Manual Testing via API Docs
```bash
# Access interactive API documentation
open http://localhost:8000/docs

# Test endpoints directly in the Swagger UI
```

### Test Automation Jobs
```bash
# Trigger payment reminders manually
curl -X POST http://localhost:8000/api/reminders/trigger

# Trigger Gmail polling manually
curl -X POST http://localhost:8000/api/gmail/poll
```

## 🐛 Troubleshooting

Common issues and solutions are documented in the [Getting Started Guide](GETTING_STARTED.md#-troubleshooting).

Quick checks:
```bash
# View logs
docker compose logs backend
docker compose logs frontend

# Check service health
docker compose ps
curl http://localhost:8000/health
```

## 📚 Additional Resources

- **Getting Started:** [GETTING_STARTED.md](GETTING_STARTED.md)
- **Technical Details:** [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- **Security Info:** [SECURITY_FIXES.md](SECURITY_FIXES.md)
- **API Docs:** http://localhost:8000/docs (when running)

## 🤝 Contributing

This is a proprietary system for IGI Insurance. For internal contributions, please follow the standard Git workflow.

## 📞 Support

For support and inquiries:
- **Email:** support@igiinsurance.com
- **Phone:** +92-51-111-244-244

## 📄 License

Proprietary - IGI Insurance Limited. All rights reserved.

---

**Built with ❤️ for IGI Insurance**

**Need help?** Start with the [Getting Started Guide](GETTING_STARTED.md)!
