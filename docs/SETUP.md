# Setup Guide

Complete installation and configuration guide for the QA Coverage Dashboard.

## Quick Start (5 Minutes)

### Prerequisites
- Python 3.11 or higher
- TestRail account with API access
- Internet connection

### Installation Steps

**1. Navigate to Project**
```bash
cd C:\Users\mbrancato\.claude-worktrees\coverage\infallible-mccarthy
```

**2. Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure TestRail Credentials**

Copy the example secrets file:
```bash
# Windows
copy .streamlit\secrets.toml.example .streamlit\secrets.toml

# macOS/Linux
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` and add your TestRail credentials:
```toml
[testrail]
url = "https://your-instance.testrail.io"
email = "your-email@company.com"
api_key = "your-api-key-here"
```

**How to get your TestRail API key:**
1. Log into TestRail
2. Click your profile (top-right) → "My Settings"
3. Under "API Keys" section, click "Add Key"
4. Copy the generated key

**5. Run Dashboard**
```bash
streamlit run dashboard.py
```

Dashboard opens at: http://localhost:8501

---

## PyCharm Setup

### Configure Python Interpreter

1. Open PyCharm
2. `File` → `Open` → Select project folder
3. `File` → `Settings` → `Project` → `Python Interpreter`
4. Click gear icon ⚙️ → `Add Interpreter` → `Add Local Interpreter`
5. Select `Virtual Environment` → `New`
6. Base interpreter: Python 3.11 or higher
7. Click `OK`

### Install Dependencies in PyCharm

**Option A - PyCharm Terminal:**
```bash
pip install -r requirements.txt
```

**Option B - PyCharm UI:**
1. Open `requirements.txt`
2. Click "Install requirements" banner
3. Wait for installation

### Create Run Configuration

**Method 1 - Terminal (Simplest):**
```bash
streamlit run dashboard.py
```

**Method 2 - Run Configuration (Recommended):**
1. `Run` → `Edit Configurations...`
2. Click `+` → `Python`
3. Configure:
   - **Name**: `Streamlit Dashboard`
   - **Module name**: `streamlit` (not script path)
   - **Parameters**: `run dashboard.py`
   - **Working directory**: Project root
   - **Python interpreter**: Select venv
4. Click `OK`
5. Click green ▶️ to run

---

## First Use

1. **Select Business Unit** from dropdown (e.g., "Microservices")
2. **Click "Update Dashboard"** button
3. **Wait for data** to load (30-60 seconds first time)
4. **Explore!** Use filters, view charts, export data

---

## Configuration

### Business Units

Business units are configured in `src/config.py`. Each requires:
- **name**: Display name
- **project_id**: TestRail project ID
- **suite_id**: TestRail suite ID

To add a new business unit:
```python
"New BU Name": (project_id, suite_id)
```

### Country Mappings

For BUs with multiple countries (Marionnaud, Drogas), configure in `COUNTRY_MAPPINGS`:
```python
COUNTRY_MAPPINGS = {
    "Marionnaud": {
        '3': 'MRN',
        '9': 'MFR',
        # Add more mappings
    }
}
```

### Custom Field Names

The dashboard auto-detects TestRail custom field names. Add variations in `FIELD_VARIATIONS` if needed.

---

## Development Setup

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_transformer.py -v

# View coverage report
# Open htmlcov/index.html in browser
```

### Enable Debug Logging

Edit `dashboard.py`:
```python
logging.basicConfig(level=logging.DEBUG)  # Change from INFO to DEBUG
```

### VS Code Dev Container

If using Docker and VS Code:
1. Install "Dev Containers" extension
2. Press `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"
3. Container builds automatically
4. Dashboard starts on port 8501

---

## Deployment

### Streamlit Community Cloud (FREE)

**Deploy to cloud for public access:**

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Sign in with GitHub
4. Click `New app`
5. Select repository, branch (`master`), and main file (`dashboard.py`)
6. Click `Advanced settings` → Add secrets:
   ```toml
   [testrail]
   url = "https://your-instance.testrail.io"
   email = "your-email@company.com"
   api_key = "your-api-key-here"
   ```
7. Click `Deploy`

**Result:** Public URL like `https://your-app.streamlit.app`

### Using ngrok (Temporary Public URL)

```bash
# Run dashboard locally
streamlit run dashboard.py

# In another terminal
ngrok http 8501
```

**Result:** Temporary URL like `https://abc123.ngrok.io`

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "dashboard.py", "--server.address", "0.0.0.0"]
```

Build and run:
```bash
docker build -t qa-dashboard .
docker run -p 8501:8501 qa-dashboard
```

---

## Troubleshooting

### "Command not found: streamlit"
**Solution:** Activate virtual environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### "Missing credential in secrets.toml"
**Solution:**
1. Verify `.streamlit/secrets.toml` exists
2. Check all fields present (url, email, api_key)
3. Ensure section name is `[testrail]`

### "No test cases found"
**Solution:**
1. Verify project_id and suite_id in `src/config.py`
2. Check suite contains test cases in TestRail
3. Ensure user has access to project

### "Connection refused" or API errors
**Solution:**
1. Verify TestRail URL is correct (include `https://`)
2. Check email and API key are correct
3. Test API key in TestRail UI
4. Ensure TestRail instance is accessible

### Port 8501 already in use
**Solution:** Use different port
```bash
streamlit run dashboard.py --server.port 8502
```

### Dashboard is slow
**Solution:**
1. First load is always slower (fetching data)
2. Subsequent loads use cache (1 hour)
3. Clear cache: Click "C" menu → Clear Cache

### Import errors after restructuring
**Solution:**
1. Ensure virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check Python path includes project root

---

## Common Commands

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run dashboard
streamlit run dashboard.py

# Run tests
pytest

# Run tests with coverage
pytest --cov=src

# Deactivate environment
deactivate

# Update dependencies
pip install -r requirements.txt --upgrade

# Clear Streamlit cache
# Use "C" menu in running app → Clear Cache
```

---

## Updating

To update to newer version:

1. **Backup secrets:**
   ```bash
   cp .streamlit/secrets.toml .streamlit/secrets.toml.backup
   ```

2. **Pull changes** (if using Git):
   ```bash
   git pull origin master
   ```

3. **Update dependencies:**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. **Restart dashboard:**
   ```bash
   streamlit run dashboard.py
   ```

---

## Getting Help

1. Check this guide
2. Review [README.md](README.md) for features
3. Check logs in terminal
4. Enable debug logging
5. Contact administrator

---

**You're ready to use the dashboard!** 🎉
