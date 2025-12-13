# How to Run the Multi-Agent Chat System

## 🚀 Quick Start Guide

### Option 1: Run Everything Separately (Recommended for Development)

#### Step 1: Start the Backend (Python/FastAPI)

1. **Open a terminal/PowerShell window**

2. **Navigate to project directory:**
   ```powershell
   cd E:\KRR_ASSIGNMENT_PROJECT
   ```

3. **Activate virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   You should see `(venv)` in your prompt.

4. **Start the backend server:**
   ```powershell
   uvicorn main:app --reload --port 8000
   ```

5. **Verify it's running:**
   - You should see: `Uvicorn running on http://0.0.0.0:8000`
   - Open browser: http://localhost:8000
   - API docs: http://localhost:8000/docs

#### Step 2: Start the Frontend (Next.js)

1. **Open a NEW terminal/PowerShell window** (keep backend running)

2. **Navigate to frontend directory:**
   ```powershell
   cd E:\KRR_ASSIGNMENT_PROJECT\frontend
   ```

3. **Install dependencies (first time only):**
   ```powershell
   npm install
   ```

4. **Start the frontend:**
   ```powershell
   npm run dev
   ```

5. **Access the web interface:**
   - Open browser: http://localhost:3000

### Option 2: Using Docker (All-in-One)

1. **Make sure Docker Desktop is running**

2. **Navigate to project directory:**
   ```powershell
   cd E:\KRR_ASSIGNMENT_PROJECT
   ```

3. **Start everything:**
   ```powershell
   docker-compose up --build
   ```

4. **Access:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 3: Console Client (No Frontend)

1. **Activate virtual environment:**
   ```powershell
   cd E:\KRR_ASSIGNMENT_PROJECT
   .\venv\Scripts\Activate.ps1
   ```

2. **Run console client:**
   ```powershell
   python console_client.py
   ```

## 📋 Step-by-Step Visual Guide

### Terminal 1 - Backend:
```
E:\KRR_ASSIGNMENT_PROJECT> .\venv\Scripts\Activate.ps1
(venv) E:\KRR_ASSIGNMENT_PROJECT> uvicorn main:app --reload --port 8000
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Terminal 2 - Frontend:
```
E:\KRR_ASSIGNMENT_PROJECT\frontend> npm install
... (first time only)
E:\KRR_ASSIGNMENT_PROJECT\frontend> npm run dev
  ▲ Next.js 14.0.3
  - Local:        http://localhost:3000
```

## 🔧 Troubleshooting

### Backend won't start?
- **Port 8000 already in use?**
  ```powershell
  # Use a different port
  uvicorn main:app --reload --port 8001
  ```
  Then update frontend: Change `NEXT_PUBLIC_API_URL` in `frontend/.env.local` to `http://localhost:8001`

- **Dependencies not installed?**
  ```powershell
  pip install -r requirements.txt
  ```

- **Virtual environment not activated?**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

### Frontend won't connect?
- **Backend not running?** Make sure backend is running on port 8000
- **CORS errors?** Backend should allow all origins (already configured)
- **API URL wrong?** Check `frontend/next.config.js` - it should proxy to `http://localhost:8000`

### Frontend dependencies?
```powershell
cd frontend
npm install
```

## 🎯 Quick Commands Reference

| Task | Command |
|------|---------|
| Start Backend | `uvicorn main:app --reload --port 8000` |
| Start Frontend | `cd frontend && npm run dev` |
| Run Tests | `python run_tests.py` |
| Console Client | `python console_client.py` |
| Docker (all) | `docker-compose up --build` |

## ✅ Verification Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Can access http://localhost:8000/docs (API documentation)
- [ ] Frontend running on http://localhost:3000
- [ ] Can see the chat interface in browser
- [ ] Can send a query and get a response

## 🎬 Example Workflow

1. **Terminal 1:** Start backend → `uvicorn main:app --reload`
2. **Terminal 2:** Start frontend → `cd frontend && npm run dev`
3. **Browser:** Open http://localhost:3000
4. **Test:** Type "What is AI?" and see the response!

---

**Note:** Keep both terminals open while using the system. Press `Ctrl+C` in each terminal to stop the servers.

