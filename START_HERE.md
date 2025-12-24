# 🚀 QA Coverage Dashboard - GUIDA RAPIDA

## ✅ File Principale da Eseguire

**File:** `dashboard.py`

---

## 🏃 Come Avviare l'Applicazione

### Metodo 1: Da PyCharm Terminal (PIÙ SEMPLICE)

1. Apri il progetto in PyCharm
2. Apri il Terminal (in basso)
3. Esegui:

```bash
.venv\Scripts\streamlit.exe run dashboard.py
```

4. Si aprirà automaticamente nel browser: http://localhost:8501

---

### Metodo 2: Run Configuration in PyCharm

1. `Run` → `Edit Configurations...`
2. Clicca `+` → `Python`
3. Configura:
   - **Nome:** Dashboard
   - **Script path:** Lascia vuoto
   - **Module name:** `streamlit`
   - **Parameters:** `run dashboard.py`
   - **Working directory:** `C:\Users\mbrancato\PyCharm\Automation\Report\coverage`
   - **Python interpreter:** Seleziona `.venv`
4. Clicca OK
5. Premi il pulsante verde ▶️

---

## ⚙️ Configurazione Credenziali (IMPORTANTE!)

### Prima di eseguire, configura le credenziali TestRail:

1. Copia il file template:
```bash
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
```

2. Apri `.streamlit\secrets.toml` e inserisci le tue credenziali TestRail:

```toml
[testrail]
url = "https://your-instance.testrail.io"
email = "your-email@company.com"
api_key = "your-api-key-here"
```

---

## 📁 Struttura Progetto (SEMPLIFICATA)

```
coverage/
├── src/                    # Codice sorgente
│   ├── constants.py       # Costanti (cache, API, ecc.)
│   ├── config.py          # Configurazioni business unit
│   ├── connector.py       # Connessione TestRail API
│   ├── transformer.py     # Trasformazione dati
│   ├── metrics.py         # Calcolo metriche
│   ├── visualizations.py  # Grafici
│   └── exporter.py        # Export Excel
├── docs/                   # Documentazione
│   ├── SETUP.md           # Guida installazione completa
│   └── CHANGELOG.md       # Cronologia versioni
├── tests/                  # Test unitari
├── .streamlit/
│   └── secrets.toml       # ⚠️ CREA QUESTO FILE!
├── dashboard.py           # 🎯 FILE PRINCIPALE
├── README.md              # Panoramica progetto
└── START_HERE.md          # 👈 QUESTO FILE
```

---

## 🔧 Risoluzione Problemi

### Errore: "streamlit command not found"
```bash
# Installa Streamlit nel virtual environment
.venv\Scripts\pip.exe install streamlit pandas plotly testrail-api numpy openpyxl
```

### Errore: "Missing credential in secrets.toml"
- Crea il file `.streamlit\secrets.toml` come descritto sopra
- Assicurati di aver inserito URL, email e API key corretti

### Errore: "Module 'src' not found"
- Assicurati di essere nella directory corretta del progetto
- Verifica che la cartella `src/` esista

---

## 🌐 Rendere Accessibile da Link Pubblico

### Opzione 1: Streamlit Community Cloud (GRATIS)

1. Fai push del codice su GitHub
2. Vai su https://streamlit.io/cloud
3. Collega il repository
4. Configura i secrets nella dashboard cloud
5. Ottieni URL pubblico tipo: `https://tuo-app.streamlit.app`

### Opzione 2: ngrok (Test rapidi)

```bash
# In un terminale esegui:
.venv\Scripts\streamlit.exe run dashboard.py

# In un altro terminale:
ngrok http 8501
```

---

## 🎯 Funzionalità Principali

1. **Tracking Multi-Framework** - Java & Testim
2. **9 Business Units** - Configurazioni individuali
3. **Filtri Avanzati** - Device, Country, Priority
4. **Analisi Epic** - Top/Bottom performers
5. **Export Excel** - Dati completi dashboard
6. **Health Check** - Endpoint per monitoraggio

---

## 📚 Documentazione

- **Questa guida**: `START_HERE.md` (italiano)
- **Guida completa**: `docs/SETUP.md` (inglese)
- **Miglioramenti**: `IMPROVEMENTS_APPLIED.md`
- **Guida rapida**: `QUICK_START_GUIDE.md`

---

## ✅ Checklist Avvio Rapido

- [ ] Virtual environment attivo (`.venv`)
- [ ] Dipendenze installate (`pip install -r requirements.txt`)
- [ ] File `.streamlit/secrets.toml` creato con credenziali
- [ ] Esegui: `.venv\Scripts\streamlit.exe run dashboard.py`
- [ ] Apri browser: http://localhost:8501

---

## 🎊 PRONTO ALL'USO!

**Comando veloce:**
```bash
.venv\Scripts\streamlit.exe run dashboard.py
```

**Il browser si aprirà automaticamente su:** http://localhost:8501

---

**Buon lavoro!** 📊✨
