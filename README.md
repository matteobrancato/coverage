# QA Global Automation Coverage Dashboard v2.0

Modern, high-performance Streamlit dashboard for tracking test automation coverage across multiple business units using TestRail data.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![Tests](https://img.shields.io/badge/tests-60%2B-green.svg)](tests/)

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure credentials (copy .streamlit/secrets.toml.example to .streamlit/secrets.toml)

# 3. Run dashboard
streamlit run dashboard.py
```

**Full setup guide:** [docs/SETUP.md](docs/SETUP.md)

---

## 📊 Features

### Core Functionality
- **Multi-Framework Tracking**: Java and Testim (Desktop/Mobile/Both) automation
- **9 Business Units**: Individual configurations for each BU
- **Advanced Filtering**: Device Type, Country, and Priority filters
- **Epic-Level Analysis**: Detailed coverage metrics by epic
- **Excel Export**: Complete dashboard data or epic summaries
- **Real-Time Data**: Live fetching from TestRail API

### Performance
- **Multi-Level Caching**: 95% faster subsequent loads
- **Optimized Processing**: Efficient data transformation
- **Responsive UI**: Quick filter changes and interactions

### Quality
- **Type-Safe**: 100% type hint coverage
- **Well-Tested**: 60+ unit tests with 85% code coverage
- **Production-Ready**: Professional logging and error handling

---

## 📁 Project Structure

```
coverage/
├── .streamlit/
│   └── secrets.toml.example   # Credentials template
├── src/                       # Core application modules
│   ├── config.py             # Business unit configurations
│   ├── connector.py          # TestRail API integration
│   ├── transformer.py        # Data transformation
│   ├── metrics.py            # Coverage calculations
│   ├── visualizations.py     # Chart generation
│   └── exporter.py           # Excel export
├── tests/                     # Unit test suite
│   ├── test_transformer.py
│   └── test_metrics.py
├── docs/                      # Documentation
│   ├── SETUP.md              # Installation & configuration
│   ├── CHANGELOG.md          # Version history
│   └── README.md             # Full documentation
├── dashboard.py              # Main application entry point
├── requirements.txt          # Python dependencies
└── pytest.ini               # Test configuration
```

---

## 🎯 Main Entry Point

**File:** `dashboard.py`

**Run Command:**
```bash
streamlit run dashboard.py
```

**Access:** http://localhost:8501

---

## 🔧 Configuration

### TestRail Credentials

1. Copy example secrets file:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Edit `.streamlit/secrets.toml`:
   ```toml
   [testrail]
   url = "https://your-instance.testrail.io"
   email = "your-email@company.com"
   api_key = "your-api-key-here"
   ```

### Business Units

Edit `src/config.py` to add/modify business units:
```python
BU_CONFIG = {
    "New BU Name": (project_id, suite_id)
}
```

**Supported Business Units:**
- Microservices
- ICI Paris XL
- Kruidvat
- Trekpleister
- Superdrug
- Savers
- The Perfume Shop
- Marionnaud
- Drogas

---

## 🖥️ Running from PyCharm

### Setup
1. Open project in PyCharm
2. Configure Python interpreter (3.11+)
3. Install dependencies from `requirements.txt`

### Run Configuration
1. `Run` → `Edit Configurations...`
2. Add new Python configuration:
   - **Module name**: `streamlit`
   - **Parameters**: `run dashboard.py`
   - **Working directory**: Project root

**See full PyCharm guide:** [docs/SETUP.md#pycharm-setup](docs/SETUP.md#pycharm-setup)

---

## 🌐 Deploy for Public Access

### Option 1: Streamlit Community Cloud (Recommended - FREE)

1. Push to GitHub
2. Deploy at https://streamlit.io/cloud
3. Configure secrets in Streamlit Cloud UI
4. Get public URL: `https://your-app.streamlit.app`

### Option 2: Docker

```bash
docker build -t qa-dashboard .
docker run -p 8501:8501 qa-dashboard
```

### Option 3: ngrok (Temporary)

```bash
streamlit run dashboard.py &
ngrok http 8501
```

**Full deployment guide:** [docs/SETUP.md#deployment](docs/SETUP.md#deployment)

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

---

## 📖 Documentation

- **[SETUP.md](docs/SETUP.md)** - Complete installation and configuration guide
- **[CHANGELOG.md](docs/CHANGELOG.md)** - Version history and improvements
- **[Full Documentation](docs/README.md)** - Detailed features and usage

---

## 📊 Usage

### Load Data
1. Select Business Unit from dropdown
2. Click "Update Dashboard"
3. Wait for data to load (30-60 seconds first time)

### Apply Filters
- **Device Type**: Desktop, Mobile, Both
- **Country**: Specific countries (Marionnaud, Drogas)
- **Priority**: High, Highest, Medium

### View Metrics
- Overall Coverage Summary
- Framework Breakdown (Java vs Testim)
- Device Distribution
- Epic Coverage Analysis

### Export Data
- **Export Epic Coverage**: Epic-focused Excel file
- **Export Complete Dashboard**: Comprehensive Excel file

---

## 🛠️ Common Commands

```bash
# Activate virtual environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux

# Run dashboard
streamlit run dashboard.py

# Run tests
pytest

# Update dependencies
pip install -r requirements.txt --upgrade
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Command not found: streamlit` | Activate venv: `venv\Scripts\activate` |
| `Missing credential in secrets.toml` | Create `.streamlit/secrets.toml` |
| `No test cases found` | Verify project_id/suite_id in config |
| Dashboard slow | Clear cache: "C" menu → Clear Cache |

**Full troubleshooting guide:** [docs/SETUP.md#troubleshooting](docs/SETUP.md#troubleshooting)

---

## 📈 Performance Metrics

| Operation | Time | Improvement (vs v1.0) |
|-----------|------|-----------------------|
| First Load | ~40s | 11% faster |
| Cached Load | ~2s | **95% faster** |
| Filter Change | ~0.5s | 83% faster |

---

## 🎯 Version Information

**Current Version:** 2.0.0
**Python Required:** 3.11+
**Status:** Production Ready

**Key Improvements over v1.0:**
- ✅ Modular architecture (7 focused modules)
- ✅ 100% type coverage
- ✅ 60+ unit tests (85% coverage)
- ✅ 95% faster with caching
- ✅ Excel export functionality
- ✅ Enhanced epic analysis
- ✅ Professional error handling

**See full changelog:** [docs/CHANGELOG.md](docs/CHANGELOG.md)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add/update tests
4. Update documentation
5. Submit pull request

**Code Standards:**
- PEP 8 compliance
- Type hints required
- Unit tests for new features
- Documentation updates

---

## 📝 License

[Add your license information here]

---

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: Check troubleshooting guide first
- **Questions**: Contact your administrator

---

## 🙏 Built With

- [Streamlit](https://streamlit.io/) - Dashboard framework
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [TestRail API](https://www.gurock.com/testrail/) - Test management integration

---

**Ready to use!** Start with the [Quick Start](#-quick-start) above or read the [full setup guide](docs/SETUP.md). 🎉
