# Quick Start Guide

Get the QA Coverage Dashboard running in 5 minutes!

## Prerequisites Check

Before starting, verify you have:
- [ ] Python 3.11 or higher installed
- [ ] TestRail account credentials
- [ ] Internet connection

## Installation (5 Steps)

### 1. Navigate to Project
```bash
cd /c/Users/mbrancato/PyCharm/Automation/Report/coverage
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure TestRail Credentials

Create `.streamlit/secrets.toml`:
```toml
[testrail]
url = "https://your-instance.testrail.io"
email = "your-email@company.com"
api_key = "your-api-key-here"
```

### 5. Run Dashboard
```bash
streamlit run dashboard.py
```

Dashboard opens at: http://localhost:8501

## First Use

1. **Select Business Unit** from dropdown (e.g., "Microservices")
2. **Click "Update Dashboard"** button
3. **Wait for data** to load (30-60 seconds first time)
4. **Explore!** Use filters, view charts, export data

## Common Commands

```bash
# Activate virtual environment (run first every time)
venv\Scripts\activate

# Run dashboard
streamlit run dashboard.py

# Run tests
pytest

# Deactivate virtual environment when done
deactivate
```

## Troubleshooting

### "Command not found: streamlit"
→ Activate virtual environment: `venv\Scripts\activate`

### "Missing credential in secrets.toml"
→ Create `.streamlit/secrets.toml` with your TestRail credentials

### "No test cases found"
→ Verify project_id and suite_id in `modules/config.py`

## What's Next?

- Read [README.md](README.md) for detailed documentation
- See [INSTALLATION.md](INSTALLATION.md) for detailed setup guide
- Check [IMPROVEMENTS.md](IMPROVEMENTS.md) to see what's new
- Explore `modules/` to understand the code structure

## Need Help?

1. Check [INSTALLATION.md](INSTALLATION.md) troubleshooting section
2. Review logs in the terminal
3. Contact your administrator

---

**That's it! You're ready to use the dashboard.** 🎉
