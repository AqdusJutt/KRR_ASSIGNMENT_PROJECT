# Project Structure

```
KRR_ASSIGNMENT_PROJECT/
│
├── agents/                          # Agent implementations
│   ├── __init__.py
│   ├── coordinator.py              # Coordinator/Manager agent
│   ├── research_agent.py           # Research agent
│   ├── analysis_agent.py           # Analysis agent
│   └── memory_agent.py             # Memory management agent
│
├── memory/                          # Memory system
│   ├── __init__.py
│   ├── vector_store.py             # FAISS vector store
│   └── memory_manager.py           # Memory operations manager
│
├── utils/                           # Utility modules
│   ├── __init__.py
│   ├── llm_client.py               # Groq LLM integration
│   └── logger.py                   # Logging utilities
│
├── frontend/                        # Next.js web interface
│   ├── pages/
│   │   ├── _app.tsx
│   │   └── index.tsx               # Main chat interface
│   ├── styles/
│   │   └── globals.css             # Global styles
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── Dockerfile
│   └── .gitignore
│
├── outputs/                         # Test scenario outputs
│   └── .gitkeep
│
├── main.py                          # FastAPI application
├── console_client.py                # Console interface
├── run_tests.py                     # Test runner
├── setup_env.py                     # Environment setup helper
│
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Backend Docker image
├── docker-compose.yaml              # Docker Compose config
│
├── start.sh                         # Linux/Mac startup script
├── start.bat                        # Windows startup script
│
├── README.md                        # Main documentation
├── CONTRIBUTING.md                  # Contribution guidelines
├── PROJECT_STRUCTURE.md             # This file
│
└── .gitignore                       # Git ignore rules
```

## Key Files

### Backend (Python)
- **main.py**: FastAPI server with REST API endpoints
- **console_client.py**: Interactive console client for testing
- **run_tests.py**: Executes the 5 required test scenarios
- **agents/coordinator.py**: Main orchestrator agent
- **agents/research_agent.py**: Information retrieval agent
- **agents/analysis_agent.py**: Comparison and reasoning agent
- **agents/memory_agent.py**: Memory management agent
- **memory/vector_store.py**: Vector similarity search implementation
- **memory/memory_manager.py**: Structured memory operations
- **utils/llm_client.py**: Groq API integration with fallbacks

### Frontend (Next.js/React)
- **frontend/pages/index.tsx**: Main chat interface component
- **frontend/styles/globals.css**: Tailwind CSS styling

### Configuration
- **requirements.txt**: Python package dependencies
- **frontend/package.json**: Node.js dependencies
- **docker-compose.yaml**: Multi-container orchestration
- **Dockerfile**: Backend container image
- **frontend/Dockerfile**: Frontend container image

### Documentation
- **README.md**: Complete project documentation
- **CONTRIBUTING.md**: Git workflow and contribution guide
- **PROJECT_STRUCTURE.md**: This file

### Testing
- **outputs/**: Directory for test scenario output files
- **run_tests.py**: Automated test execution

