# IGI Insurance Automation - Simple Overview

## 🎯 What Is This Project?

A complete insurance management system for IGI Insurance that:
1. **Manages motor insurance policies** (cars, vehicles)
2. **Automates repetitive tasks** (email reading, payment reminders)
3. **Generates professional documents** (policy PDFs, cover letters)

---

## 📋 Main Functionalities

### 1. **Policy Management** (Manual Data Entry)
Create and manage complete insurance policies through a web interface:

```
┌─────────────────────────────────────────┐
│  User enters data through web forms:    │
│  - Client information                   │
│  - Vehicle details (make, model, etc.)  │
│  - Coverage selection (perils)          │
│  - Bank information                     │
│  - Deductibles, clauses, warranties     │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  System automatically:                  │
│  - Calculates premiums                  │
│  - Validates data (duplicates, etc.)    │
│  - Applies discounts                    │
│  - Generates policy number              │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  Output: Complete insurance policy      │
│  ready for download as PDF              │
└─────────────────────────────────────────┘
```

**What you can do:**
- ✅ Add clients (name, address, contact info)
- ✅ Create policies with unique policy numbers
- ✅ Add vehicles (engine #, chassis #, make, model)
- ✅ Select coverage (perils like theft, accident, liability)
- ✅ Set discounts and deductibles
- ✅ Add clauses and warranties
- ✅ Calculate premiums automatically
- ✅ Download professional PDF documents

---

### 2. **Automation #1: Payment Reminders** (CSV-Based)

Automatically send payment reminders to clients:

```
┌─────────────────────────────────────────┐
│  CSV File (due_payments.csv)            │
│  Contains: Client name, email, phone,   │
│            due amount, due date         │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  Scheduler (Runs Daily at 8 AM)         │
│  - Reads CSV file                       │
│  - Finds payments due in next 30 days   │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  Automatic Actions:                     │
│  - Sends email reminder                 │
│  - Sends SMS reminder (mock)            │
│  - Marks reminder as sent               │
└─────────────────────────────────────────┘
```

**How it works:**
1. Put client payment data in `backend/app/data/due_payments.csv`
2. Every day at 8:00 AM, system checks for upcoming due dates
3. Automatically sends email + SMS reminders
4. Logs all actions

**Example CSV:**
```csv
client_name,email,phone,due_amount,due_date
Muhammad Ali Khan,ali.khan@example.com,+923001234567,150000,2026-03-01
Sara Ahmed,sara.ahmed@example.com,+923009876543,75000,2026-02-15
```

---

### 3. **Automation #2: Gmail Policy Creation** (Email-Based)

Automatically create draft policies from emails:

```
┌─────────────────────────────────────────┐
│  Client sends email with vehicle info:  │
│  "I want insurance for my car           │
│   Name: Ahmed Malik                     │
│   Make: Honda, Model: Civic, Year: 2022 │
│   Engine: ABC123, Chassis: XYZ789"      │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  Gmail Poller (Every 5 minutes)         │
│  - Fetches unread emails via Gmail API  │
│  - Classifies: Is it about insurance?   │
│  - Looks for keywords: car, motor, etc. │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  Smart Extraction:                      │
│  - Extracts: Name, Make, Model, Engine  │
│  - Uses regex patterns                  │
│  - Validates extracted data             │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  Auto-creates DRAFT policy in database  │
│  Staff reviews and completes it         │
└─────────────────────────────────────────┘
```

**How it works:**
1. Connect Gmail account via OAuth 2.0 (secure, no password sharing)
2. System checks Gmail inbox every 5 minutes
3. Finds emails about "car insurance", "motor insurance", "vehicle policy"
4. Extracts client and vehicle information
5. Creates a draft policy in the database
6. Marks email as read
7. Staff can then complete and finalize the policy

**Keywords it looks for:**
- car insurance, motor insurance, vehicle policy
- registration, chassis, engine number
- sum insured, premium, comprehensive cover

---

## 🔄 Complete Workflow Example

### Scenario: New Car Insurance Policy

**Step 1: Client Contacts** (Multiple ways)
```
Option A: Walk-in → Staff enters data manually
Option B: Phone call → Staff enters data manually  
Option C: Email → System auto-creates draft
```

**Step 2: Data Entry** (Web interface)
```
Module 1: Insured Address → Enter client details
Module 2: Bank → Add bank information
Module 3: Vehicle Details → Engine, chassis, make, model
Module 4: Product Setup → Select perils (theft, accident)
Module 5: Item Details → Sum insured
Module 6: Peril Calculation → Rates and premiums
... (15 modules total)
```

**Step 3: Automatic Calculations**
```
System calculates:
- Basic premium (based on perils selected)
- Charges (admin, sales tax, federal fee, stamp duty)
- Discounts (if applicable)
- Net premium = Gross premium - Discounts
```

**Step 4: Review & Generate**
```
Computational Sheet → See all calculations
Final Policy → Review complete policy
Download PDF → Get professional documents
```

**Step 5: Payment Tracking**
```
Add client to due_payments.csv
System sends automatic reminders before due date
```

---

## 🎯 Key Automation Benefits

### Without Automation:
❌ Staff manually tracks payment due dates
❌ Staff manually sends reminder emails
❌ Staff manually reads emails and creates policies
❌ High chance of missing deadlines
❌ Time-consuming repetitive work

### With Automation:
✅ System automatically sends reminders (email + SMS)
✅ System automatically reads emails and extracts data
✅ System automatically creates draft policies
✅ Zero missed deadlines
✅ Staff focuses on high-value tasks

---

## 🏗️ System Architecture (Simple)

```
┌─────────────────────────────────────────────────────────┐
│                    WEB BROWSER                          │
│              (Staff uses this interface)                │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│                   FRONTEND (React)                      │
│        - Forms for data entry                           │
│        - Tables to view data                            │
│        - Buttons to download PDFs                       │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                     │
│        - Processes all business logic                   │
│        - Calculates premiums                            │
│        - Validates data                                 │
│        - Generates PDFs                                 │
│        - Runs automation jobs                           │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│                   DATABASE (PostgreSQL)                 │
│        - Stores all policy data                         │
│        - Stores client information                      │
│        - Stores vehicle details                         │
└─────────────────────────────────────────────────────────┘

              ┌──────────────────┐
              │   AUTOMATIONS    │
              │  (Background)    │
              ├──────────────────┤
              │ 1. CSV Reminder  │
              │    (Daily 8 AM)  │
              │                  │
              │ 2. Gmail Poller  │
              │    (Every 5 min) │
              └──────────────────┘
```

---

## 📊 Data Modules (15 Total)

The system manages data in 15 organized modules:

| # | Module | Purpose |
|---|--------|---------|
| 1 | **Clients** | Client name, address, contact |
| 2 | **Policies** | Policy number, dates, status |
| 3 | **Banks** | Bank details for financing |
| 4 | **Documents** | Terms, conditions, notes |
| 5 | **Product Setup** | Which perils/charges to include |
| 6 | **Items** | Insured items (vehicles) |
| 7 | **Perils** | Coverage details (theft, fire, etc.) |
| 8 | **Vehicles** | Make, model, engine, chassis |
| 9 | **Discounts** | Item-level discounts |
| 10 | **Deductibles** | D/E & D/I amounts |
| 11 | **Policy Discounts** | Policy-level discounts |
| 12 | **Clauses** | Endorsements (terrorism, hypothecation) |
| 13 | **Warranties** | Tracker/device warranties |
| 14 | **Agencies** | Agent commission split |
| 15 | **Computational Sheet** | View all calculations (read-only) |

**Plus:**
- **Final Policy View** - Complete policy ready for download
- **Reminders** - Track due payments

---

## 🚀 How to Use the System

### For Staff (Daily Use):

**1. Create a New Policy:**
```
1. Open browser → http://localhost:3000
2. Click "Clients" → Add new client
3. Click "Policies" → Create new policy
4. Fill all required modules (vehicle, perils, etc.)
5. Review "Computational Sheet"
6. Download PDF from "Final Policy"
```

**2. Check Auto-Created Policies:**
```
1. Go to Gmail Integration section
2. View "Draft Policies" from emails
3. Complete missing information
4. Finalize and download
```

**3. Monitor Payment Reminders:**
```
1. View "Reminders" module
2. See which reminders were sent
3. Check success/failure status
```

### For Automation Setup:

**CSV Reminders:**
```
1. Edit backend/app/data/due_payments.csv
2. Add clients with due dates
3. System automatically sends reminders daily
```

**Gmail Integration:**
```
1. Get Gmail OAuth credentials from Google
2. Add to .env file
3. Click "Gmail Auth" in system
4. Authorize access
5. System automatically polls inbox
```

---

## 🎬 Automation Schedule

| Automation | Frequency | What It Does |
|------------|-----------|--------------|
| **Payment Reminders** | Daily at 8:00 AM | Checks CSV, sends emails/SMS for upcoming dues |
| **Gmail Poller** | Every 5 minutes | Fetches emails, creates draft policies |

Both run automatically in the background when the system is running.

---

## 📁 Key Files

### Backend:
- `backend/app/main.py` - Main application entry point
- `backend/app/automation/scheduler.py` - Sets up automation jobs
- `backend/app/automation/reminder_job.py` - CSV reminder logic
- `backend/app/automation/gmail_poller.py` - Gmail polling logic
- `backend/app/data/due_payments.csv` - Payment tracking data

### Frontend:
- `frontend/src/App.tsx` - Main UI application
- `frontend/src/components/forms/ClientsForm.tsx` - Client management
- `frontend/src/components/forms/PoliciesForm.tsx` - Policy management

### Configuration:
- `.env` - Environment variables (database, Gmail, SMTP)
- `docker-compose.yml` - Runs all services together

---

## ⚙️ Starting the System

### Simple Start:
```bash
docker compose up --build
```

This starts:
1. ✅ PostgreSQL database (port 5432)
2. ✅ Backend API (port 8000)
3. ✅ Frontend UI (port 3000)
4. ✅ Automation jobs (background)

### Access Points:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

---

## 🔍 Quick Test

### Test Policy Creation:
1. Open http://localhost:3000
2. Click "Clients" → Add new client
3. Click "Policies" → Create new policy
4. See automatic policy number generated

### Test CSV Reminders:
1. Check `backend/app/data/due_payments.csv`
2. Trigger manually: POST http://localhost:8000/api/reminders/trigger
3. Check logs for "Sending reminder to..."

### Test Gmail Integration:
1. Get OAuth URL: GET http://localhost:8000/api/gmail/auth-url
2. Authorize access
3. Trigger poll: POST http://localhost:8000/api/gmail/poll
4. Check for draft policies

---

## 🎓 Summary

**This system does 3 main things:**

1. **Manual Policy Management** 
   - Staff enters data through web forms
   - System calculates everything automatically
   - Downloads professional PDF documents

2. **CSV-Based Payment Reminders**
   - Reads due payments from CSV file
   - Automatically sends email + SMS reminders
   - Runs daily at 8 AM

3. **Gmail-Based Policy Creation**
   - Reads insurance emails automatically
   - Extracts client and vehicle information
   - Creates draft policies for staff review
   - Runs every 5 minutes

**Everything is automated in the background!**

---

## 📞 Need Help?

- **Setup Issues?** → Read `GETTING_STARTED.md`
- **Errors?** → Check `TROUBLESHOOTING.md`
- **Quick Commands?** → See `QUICK_REFERENCE.md`
- **All Documentation?** → Check `DOCUMENTATION_INDEX.md`

---

**That's it! The system is designed to save time by automating repetitive insurance tasks.** 🎉
