# 🚀 Quick Start - Run Backend & Frontend

## Method 1: Two Terminal Windows (Recommended)

### Terminal 1 - Backend (Python/FastAPI)

```powershell
# Navigate to project
cd E:\KRR_ASSIGNMENT_PROJECT

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start backend server
uvicorn main:app --reload --port 8000
```

**✅ Success indicators:**
- You see: `Uvicorn running on http://0.0.0.0:8000`
- Visit: http://localhost:8000/docs (API documentation)

**Keep this terminal open!**

---

### Terminal 2 - Frontend (Next.js)

```powershell
# Navigate to frontend directory
cd E:\KRR_ASSIGNMENT_PROJECT\frontend

# Install dependencies (first time only)
npm install

# Start frontend
npm run dev
```

**✅ Success indicators:**
- You see: `Local: http://localhost:3000`
- Visit: http://localhost:3000 (Web interface)

**Keep this terminal open!**

---

## Method 2: Docker (All-in-One)

```powershell
# Navigate to project
cd E:\KRR_ASSIGNMENT_PROJECT

# Start everything
docker-compose up --build
```

**✅ Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Method 3: Console Client (No Frontend)

```powershell
# Navigate to project
cd E:\KRR_ASSIGNMENT_PROJECT

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run console client
python console_client.py
```

---

## 🎯 Quick Test

1. **Start backend** (Terminal 1)
2. **Start frontend** (Terminal 2)
3. **Open browser:** http://localhost:3000
4. **Try a query:** "What is AI?"
5. **See the response!**

---

## 🛑 How to Stop

- **Backend:** Press `Ctrl+C` in Terminal 1
- **Frontend:** Press `Ctrl+C` in Terminal 2
- **Docker:** Press `Ctrl+C` or run `docker-compose down`

---

## ❓ Troubleshooting

### Backend Issues?
- **Port 8000 busy?** Use `--port 8001` and update frontend config
- **Module not found?** Run `pip install -r requirements.txt`
- **Virtual env not active?** Run `.\venv\Scripts\Activate.ps1`

### Frontend Issues?
- **Can't connect?** Make sure backend is running first
- **npm errors?** Run `npm install` in frontend directory
- **Port 3000 busy?** Next.js will automatically use 3001

---

## 📝 Summary

| Component | Command | Port | URL |
|-----------|---------|------|-----|
| Backend | `uvicorn main:app --reload` | 8000 | http://localhost:8000 |
| Frontend | `npm run dev` | 3000 | http://localhost:3000 |
| API Docs | (auto) | 8000 | http://localhost:8000/docs |

**Remember:** Keep both terminals open while using the system!

