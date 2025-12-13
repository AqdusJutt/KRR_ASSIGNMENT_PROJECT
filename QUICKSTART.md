# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Option 1: Using Docker (Recommended)

1. **Clone the repository** (or navigate to project directory)
   ```bash
   cd KRR_ASSIGNMENT_PROJECT
   ```

2. **Set up environment variables**
   ```bash
   # Edit .env file and add your Groq API key (optional)
   # Get free API key from: https://console.groq.com/
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the system**
   - Web Interface: http://localhost:3000
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables** (optional)
   ```bash
   # Edit .env file or export:
   export GROQ_API_KEY=your_key_here
   ```

4. **Run the backend**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

#### Frontend Setup (Optional)

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the frontend**
   ```bash
   npm run dev
   ```

4. **Access the web interface**
   - http://localhost:3000

#### Console Client (Alternative to Web Interface)

1. **Run console client**
   ```bash
   python console_client.py
   ```

## 🧪 Running Tests

Execute the 5 required test scenarios:

```bash
python run_tests.py
```

This will generate output files in `outputs/`:
- `simple_query.txt`
- `complex_query.txt`
- `memory_test.txt`
- `multi_step.txt`
- `collaborative.txt`

## 📝 First Steps After Setup

1. **Test the system** with a simple query:
   ```
   "What are the main types of neural networks?"
   ```

2. **Try a complex query**:
   ```
   "Research transformer architectures and analyze their efficiency"
   ```

3. **Test memory**:
   ```
   "What did we discuss about neural networks earlier?"
   ```

## 🔑 Getting Groq API Key (Optional)

1. Visit https://console.groq.com/
2. Sign up for a free account
3. Create an API key
4. Add it to your `.env` file:
   ```
   GROQ_API_KEY=your_actual_key_here
   ```

**Note**: The system works without an LLM API key using rule-based fallbacks, but LLM integration provides better task decomposition and summarization.

## 🐛 Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Verify Python 3.9+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`

### Frontend won't connect
- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in frontend environment
- Check browser console for CORS errors

### Tests fail
- Ensure backend dependencies are installed
- Check that sentence-transformers model can download (requires internet)
- Verify outputs directory exists: `mkdir outputs`

### Docker issues
- Ensure Docker and Docker Compose are installed
- Try rebuilding: `docker-compose up --build`
- Check logs: `docker-compose logs`

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for code organization
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow

## 🎯 Assignment Deliverables Checklist

- ✅ Public GitHub Repository
- ✅ Python Codebase with all agents
- ✅ Test Runs with outputs in `outputs/` folder
- ✅ README with architecture overview
- ✅ Dockerfile and docker-compose.yaml
- ✅ Web Interface (Next.js)
- ✅ Console Interface
- ✅ LLM Integration (Optional, with fallback)

