# Installation Guide

## Quick Start

### 1. Prerequisites

Ensure you have the following installed:
- Python 3.11 or higher
- pip (Python package manager)
- Git
- TestRail account with API access

### 2. Clone or Copy the Project

```bash
# Navigate to your projects directory
cd /path/to/your/projects

# If using Git
git clone <repository-url> coverage
cd coverage

# Or simply copy the 'coverage' folder to your desired location
```

### 3. Set Up Python Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Your terminal should now show `(venv)` at the beginning of the prompt.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- streamlit (Dashboard framework)
- pandas (Data manipulation)
- plotly (Visualizations)
- testrail-api (TestRail integration)
- numpy (Numerical computing)
- openpyxl (Excel export)
- pytest (Testing framework)

### 5. Configure TestRail Credentials

#### Step 5a: Create secrets directory
```bash
mkdir .streamlit
```

#### Step 5b: Get your TestRail API Key

1. Log in to your TestRail instance
2. Click your name in the top-right corner
3. Select "My Settings"
4. Click the "API Keys" tab
5. Click "Add Key" to generate a new API key
6. Copy the generated key

#### Step 5c: Create secrets.toml file

Create a file named `.streamlit/secrets.toml`:

**Windows PowerShell:**
```powershell
New-Item -Path ".streamlit\secrets.toml" -ItemType File
notepad .streamlit\secrets.toml
```

**Windows Command Prompt:**
```cmd
type nul > .streamlit\secrets.toml
notepad .streamlit\secrets.toml
```

**macOS/Linux:**
```bash
touch .streamlit/secrets.toml
nano .streamlit/secrets.toml
```

#### Step 5d: Add your credentials

Paste the following into `secrets.toml` and replace with your actual credentials:

```toml
[testrail]
url = "https://your-instance.testrail.io"
email = "your-email@company.com"
api_key = "your-api-key-here"
```

**Important**: Never commit this file to version control! It's already in `.gitignore`.

### 6. Verify Installation

Test that everything is configured correctly:

```bash
streamlit run dashboard.py
```

Your default browser should open to `http://localhost:8501` showing the dashboard.

### 7. First Use

1. Select a Business Unit from the dropdown (e.g., "Microservices")
2. Click "🔄 Update Dashboard"
3. Wait for data to load (first load may take 30-60 seconds depending on data volume)
4. Explore the dashboard!

## Development Setup (Optional)

If you plan to contribute or modify the code:

### Install Development Dependencies

Already included in `requirements.txt`:
- pytest
- pytest-cov

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=modules --cov-report=html

# View coverage report
# Open htmlcov/index.html in your browser
```

### Set Up IDE (VS Code)

If using Visual Studio Code:

1. Install Python extension
2. Install Pylance extension
3. Select your virtual environment:
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
   - Type "Python: Select Interpreter"
   - Choose the venv you created

### Use Dev Container (Optional)

If you use Docker and VS Code:

1. Install "Dev Containers" extension in VS Code
2. Press `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"
3. Container will build and install dependencies automatically
4. Dashboard will start automatically on port 8501

## Troubleshooting

### Issue: "Command 'streamlit' not found"

**Solution**: Ensure your virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Missing credential in secrets.toml"

**Solution**:
1. Verify `.streamlit/secrets.toml` exists
2. Check that it contains all required fields (url, email, api_key)
3. Ensure there are no typos in the section name `[testrail]`

### Issue: "Connection refused" or "API Connection Failed"

**Solution**:
1. Verify your TestRail URL is correct (include https://)
2. Check your email and API key are correct
3. Ensure your TestRail instance is accessible
4. Test API key in TestRail UI (My Settings → API Keys → Test)

### Issue: "No test cases found in this suite"

**Solution**:
1. Verify the project_id and suite_id in `modules/config.py`
2. Check that the suite actually contains test cases
3. Ensure your TestRail user has access to the project

### Issue: Port 8501 already in use

**Solution**: Use a different port:
```bash
streamlit run dashboard.py --server.port 8502
```

### Issue: Dashboard won't load in browser

**Solution**:
1. Check console for errors
2. Verify firewall isn't blocking port 8501
3. Try accessing `http://localhost:8501` manually
4. Check logs for error messages

## Updating

To update to a newer version:

1. **Backup your secrets file**:
   ```bash
   cp .streamlit/secrets.toml .streamlit/secrets.toml.backup
   ```

2. **Pull new changes** (if using Git):
   ```bash
   git pull origin main
   ```

3. **Update dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. **Restore secrets** if needed:
   ```bash
   cp .streamlit/secrets.toml.backup .streamlit/secrets.toml
   ```

5. **Restart dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

## Uninstalling

To completely remove the dashboard:

1. **Deactivate virtual environment**:
   ```bash
   deactivate
   ```

2. **Delete project folder**:
   ```bash
   # Windows
   rmdir /s coverage

   # macOS/Linux
   rm -rf coverage
   ```

## Next Steps

- Read [README.md](README.md) for detailed feature documentation
- Explore `modules/config.py` to customize business units
- Check `tests/` directory for example usage
- See [CONFIGURATION.md](CONFIGURATION.md) for advanced configuration options

## Getting Help

If you encounter issues not covered here:

1. Check the main [README.md](README.md)
2. Review logs in the terminal
3. Enable debug logging (see README.md)
4. Contact your system administrator or project maintainer
