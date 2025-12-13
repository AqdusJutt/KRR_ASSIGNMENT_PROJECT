# Multi-Agent Chat System

A sophisticated multi-agent system that uses a Coordinator agent to orchestrate specialized worker agents (Research, Analysis, and Memory) to answer user questions intelligently.

## 🏗️ System Architecture

### Overview
The system consists of four main agents working in harmony:

1. **Coordinator Agent (Manager)**: Orchestrates tasks, analyzes query complexity, routes to appropriate agents, and synthesizes results
2. **Research Agent**: Retrieves information from a pre-loaded knowledge base (simulates web search)
3. **Analysis Agent**: Performs comparisons, reasoning, and calculations on retrieved data
4. **Memory Agent**: Manages long-term storage, retrieval, and context updates with vector similarity search

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface                           │
│              (Next.js Web Frontend / Console)                │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                            │
│                    (Python REST API)                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Coordinator Agent (Manager)                     │
│  • Query Analysis & Complexity Assessment                    │
│  • Task Decomposition & Planning                             │
│  • Agent Routing & Dependency Management                     │
│  • Result Synthesis & Context Management                     │
└─────┬──────────────┬──────────────┬──────────────┬──────────┘
      │              │              │              │
      ▼              ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Research │  │ Analysis │  │  Memory  │  │   LLM    │
│  Agent   │  │  Agent   │  │  Agent   │  │  (Groq)  │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └──────────┘
     │             │              │
     │             │              │
     └─────────────┴──────────────┘
                   │
                   ▼
     ┌─────────────────────────────┐
     │   Structured Memory Layer   │
     │  • Conversation Memory       │
     │  • Knowledge Base            │
     │  • Agent State Memory        │
     │  • Vector Search (FAISS)     │
     └─────────────────────────────┘
```

### Sequence Flow

```
User Query
    │
    ▼
Coordinator receives query
    │
    ▼
Complexity Analysis (with optional LLM)
    │
    ▼
Task Decomposition
    │
    ├──► Research Agent (if needed)
    │        │
    │        ▼
    │    Knowledge Retrieval
    │        │
    │        ▼
    │    Return findings
    │
    ├──► Analysis Agent (if needed)
    │        │
    │        ▼
    │    Compare/Reason/Calculate
    │        │
    │        ▼
    │    Return analysis
    │
    └──► Memory Agent
             │
             ▼
         Store/Retrieve
             │
             ▼
         Return context
    │
    ▼
Coordinator synthesizes results
    │
    ▼
Update Memory with findings
    │
    ▼
Return final answer to User
```

## 🚀 How to Run

### Prerequisites
- Python 3.9+
- Node.js 18+ (for web interface)
- Docker (optional, for containerized deployment)

### Option 1: Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd KRR_ASSIGNMENT_PROJECT
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Groq API key (optional but recommended)
   ```

3. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Access the system:**
   - Web Interface: http://localhost:3000
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

1. **Backend Setup:**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Set environment variables
   export GROQ_API_KEY=your_key_here  # Optional

   # Run the backend
   uvicorn main:app --reload --port 8000
   ```

2. **Frontend Setup (Optional):**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Console Mode:**
   ```bash
   python console_client.py
   ```

### Running Tests

Execute the 5 sample test scenarios:

```bash
python run_tests.py
```

This will generate output files in the `outputs/` directory:
- `simple_query.txt`
- `complex_query.txt`
- `memory_test.txt`
- `multi_step.txt`
- `collaborative.txt`

## 💾 Memory Design

The system implements a three-tier memory architecture:

1. **Conversation Memory**: Stores full interaction history with timestamps, user queries, agent responses, and metadata
2. **Knowledge Base**: Persistent store of learned facts and findings with provenance tracking (which agent discovered what, when)
3. **Agent State Memory**: Tracks what each agent learned/accomplished per task for adaptive behavior

### Retrieval Approach

- **Keyword/Topic Search**: Fast lookup using indexed keywords and topics
- **Vector Similarity Search**: Uses FAISS with sentence transformers (all-MiniLM-L6-v2) for semantic similarity
- **Hybrid Retrieval**: Combines both approaches for optimal relevance

### Memory Schema

```python
{
    "id": str,
    "timestamp": datetime,
    "topic": str,
    "content": str,
    "source_agent": str,
    "confidence": float,
    "metadata": dict,
    "embedding": numpy.array  # for vector search
}
```

## 🤖 Agent Details

### Coordinator Agent
- **Task Decomposition**: Uses LLM (Groq) or rule-based planner to break complex queries into sub-tasks
- **Dependency Management**: Ensures Research Agent completes before Analysis Agent when needed
- **Result Synthesis**: Merges outputs from multiple agents into coherent responses
- **Error Handling**: Implements retry logic and graceful degradation

### Research Agent
- Simulates information retrieval from a pre-loaded knowledge base
- Supports domain knowledge in: Machine Learning, Neural Networks, AI, Optimization Techniques
- Returns structured findings with confidence scores

### Analysis Agent
- Performs comparative analysis, reasoning, and calculations
- Evaluates effectiveness, trade-offs, and recommendations
- Supports multi-criteria decision making

### Memory Agent
- Manages all memory operations (store, retrieve, search)
- Implements vector similarity search for context-aware retrieval
- Maintains conversation context across sessions

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=mixtral-8x7b-32768  # or llama2-70b-4096
ENABLE_LLM=true
LOG_LEVEL=INFO
```

### LLM Integration (Optional)

The system uses Groq's free developer tier for:
- Task decomposition and planning
- Query classification
- Response summarization

**Fallback Behavior**: If LLM is unavailable, the system uses rule-based classification and planning algorithms.

## 📊 Test Scenarios

1. **Simple Query**: "What are the main types of neural networks?"
2. **Complex Query**: "Research transformer architectures, analyze their computational efficiency, and summarize key trade-offs."
3. **Memory Test**: "What did we discuss about neural networks earlier?"
4. **Multi-step**: "Find recent papers on reinforcement learning, analyze their methodologies, and identify common challenges."
5. **Collaborative**: "Compare two machine-learning approaches and recommend which is better for our use case."

## 📁 Project Structure

```
KRR_ASSIGNMENT_PROJECT/
├── agents/
│   ├── __init__.py
│   ├── coordinator.py       # Coordinator/Manager agent
│   ├── research_agent.py    # Research agent
│   ├── analysis_agent.py    # Analysis agent
│   └── memory_agent.py      # Memory management agent
├── memory/
│   ├── __init__.py
│   ├── vector_store.py      # FAISS vector store implementation
│   └── memory_manager.py    # Memory operations manager
├── utils/
│   ├── __init__.py
│   ├── llm_client.py        # Groq LLM integration
│   └── logger.py            # Logging utilities
├── frontend/                # Next.js web interface
│   ├── pages/
│   ├── components/
│   └── ...
├── outputs/                 # Test scenario outputs
│   ├── simple_query.txt
│   ├── complex_query.txt
│   ├── memory_test.txt
│   ├── multi_step.txt
│   └── collaborative.txt
├── main.py                  # FastAPI application
├── console_client.py        # Console interface
├── run_tests.py            # Test runner
├── requirements.txt
├── Dockerfile
├── docker-compose.yaml
└── README.md
```

## 🔍 Traceability

The system provides comprehensive logging:
- Agent call traces with timestamps
- Message payloads between agents
- Memory operations (store/retrieve)
- Decision-making rationale
- Error handling and fallbacks

View logs in console output or check the `logs/` directory (if file logging is enabled).

## 🤝 Team Contributions

This project demonstrates collaboration between team members with clear commit history showing individual contributions.

## 📝 License

This project is created for academic purposes as part of the Knowledge Representation and Reasoning course.

