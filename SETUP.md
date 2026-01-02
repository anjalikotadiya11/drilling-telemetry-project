# 🚀 Quick Setup Guide

## For VS Code + Git

### Step 1: Clone Repository (if not already)
```bash
git clone <your-repo-url>
cd drilling-telemetry-project
```

### Step 2: Open in VS Code
```bash
code .
```

### Step 3: Create Virtual Environment
```bash
python -m venv venv
```

**Activate it:**
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Start the System

**Option A: Automated (Recommended)**
```bash
# Mac/Linux
./scripts/start_all.sh

# Windows - run each in separate terminal:
python backend/streaming/broker.py
python backend/subscribers/db_saver.py
python backend/subscribers/prediction_engine.py
python backend/flask_app/app.py
python backend/utils/test_publisher.py
```

**Option B: Manual (for debugging)**

Open 5 terminals in VS Code (Terminal > New Terminal):

```bash
# Terminal 1
python backend/streaming/broker.py

# Terminal 2
python backend/subscribers/db_saver.py

# Terminal 3
python backend/subscribers/prediction_engine.py

# Terminal 4
python backend/flask_app/app.py

# Terminal 5
python backend/utils/test_publisher.py
```

### Step 6: Open Dashboard
Open browser: **http://localhost:5000**

---

## Git Workflow

### Initial Commit
```bash
git add .
git commit -m "Initial commit: Complete drilling telemetry system"
git push origin main
```

### Auto-commit on Changes (VS Code)
1. Install **Git Graph** extension
2. Install **GitLens** extension
3. Enable auto-save: File > Auto Save

### Recommended VS Code Extensions
- **Python** (Microsoft)
- **Pylance** (Microsoft)
- **GitLens** (GitKraken)
- **Git Graph** (mhutchie)
- **Better Comments** (Aaron Bond)

---

## Project Structure in VS Code

```
drilling-telemetry-project/
├── 📂 backend/
│   ├── 📂 streaming/          (Ctrl+Click to navigate)
│   ├── 📂 subscribers/
│   ├── 📂 flask_app/
│   └── 📂 utils/
├── 📂 frontend/
│   └── 📂 templates/
├── 📂 scripts/
├── 📄 requirements.txt
└── 📄 README.md
```

---

## Debugging in VS Code

### Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask App",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "backend/flask_app/app.py",
                "FLASK_DEBUG": "1"
            },
            "args": ["run"],
            "jinja": true
        },
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        }
    ]
}
```

### Set Breakpoints:
- Click left of line number to add red dot
- Press F5 to start debugging
- Use Debug Console to inspect variables

---

## Common Tasks

### View Logs
```bash
tail -f logs/*.log
```

### Check Database
```bash
sqlite3 drilling_data.db "SELECT * FROM drilling_data ORDER BY id DESC LIMIT 10;"
```

### Stop All Services
```bash
./scripts/stop_all.sh
```

### Git Commit
```bash
git add .
git commit -m "Your message here"
git push
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process
lsof -i :5000    # Mac/Linux
netstat -ano | findstr :5000    # Windows

# Kill process
kill -9 <PID>    # Mac/Linux
taskkill /PID <PID> /F    # Windows
```

### Module Not Found
```bash
# Make sure virtual environment is activated
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Charts Not Updating
1. Check browser console (F12)
2. Check Flask logs
3. Verify test publisher is running
4. Check WebSocket connection

---

## Next Steps

1. ✅ Get system running
2. ✅ Watch live dashboard
3. ✅ Make your first commit
4. 📝 Add your PySide6 integration
5. 🎨 Customize the dashboard
6. 🚀 Deploy to production

---

**Need help?** Check `README.md` or project logs.
