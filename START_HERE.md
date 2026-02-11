# 🎯 START HERE - Quick Overview

## What Is This System?

**IGI Insurance Automation System** - Manages motor insurance policies and automates repetitive tasks.

---

## 🚀 3 Main Things It Does

### 1. **Policy Management** (Staff enters data manually)
Create insurance policies through web forms:
- Add clients, vehicles, coverage details
- System calculates premiums automatically
- Download professional PDF documents

### 2. **Payment Reminders** (Runs automatically every day)
Reads a CSV file and sends reminders:
- Checks for payments due in next 30 days
- Sends email + SMS automatically
- Runs daily at 8:00 AM

### 3. **Email to Policy** (Runs automatically every 5 minutes)
Reads Gmail inbox and creates draft policies:
- Looks for car insurance emails
- Extracts client and vehicle info
- Creates draft policy automatically

---

## 📖 Read Next

**Want the full explanation?** → Read **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)**

It includes:
- ✅ Detailed workflows with diagrams
- ✅ Complete automation explanations
- ✅ System architecture
- ✅ How to test each feature
- ✅ Real-world examples

**Want to run it?** → Read **[GETTING_STARTED.md](GETTING_STARTED.md)**

**Have errors?** → Read **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

---

## ⚡ Quick Start (If You're Ready)

```bash
# Start the system
docker compose up --build

# Access:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

---

## 🎓 Summary

This system **saves time** by:
1. ✅ Automating payment reminders (no manual emails)
2. ✅ Automating policy creation from emails (no manual data entry)
3. ✅ Calculating premiums automatically (no manual math)

**Everything runs in the background while staff focuses on important work!**

---

**Next Step:** Read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for complete details! 📋
