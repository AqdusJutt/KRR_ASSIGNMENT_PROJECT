"""
Script to generate one-pager abstract PDF with system diagram.
Requires: pip install markdown2 pdfkit weasyprint reportlab pillow
Or use: pip install -r requirements_pdf.txt (if created)
"""

import os
from pathlib import Path

def create_diagram_mermaid():
    """Create Mermaid diagram code for system architecture."""
    mermaid_code = """
graph TB
    subgraph "User Layer"
        UI[Next.js Web Interface<br/>Port 3000]
    end
    
    subgraph "API Layer"
        API[FastAPI Backend<br/>Port 8000]
    end
    
    subgraph "Agent Layer"
        COORD[Coordinator Agent<br/>Task Decomposition<br/>Result Synthesis]
        
        subgraph "Specialized Agents"
            RESEARCH[Research Agent<br/>Knowledge Base Search]
            ANALYSIS[Analysis Agent<br/>Data Analysis & Reasoning]
            MEMORY_AGENT[Memory Agent<br/>Vector Search]
        end
    end
    
    subgraph "Memory Layer"
        MEMORY_MGR[Memory Manager]
        VECTOR[FAISS Vector Store<br/>Conversation Memory]
        KB[Knowledge Base<br/>Storage]
    end
    
    subgraph "External Services"
        LLM[Groq LLM API<br/>Llama 3.3 70B]
    end
    
    UI -->|HTTP/REST| API
    API -->|Query| COORD
    COORD -->|Search Request| RESEARCH
    COORD -->|Analyze Request| ANALYSIS
    COORD -->|Memory Query| MEMORY_AGENT
    COORD <-->|Task Decomp/Summary| LLM
    RESEARCH -->|Store Findings| MEMORY_MGR
    ANALYSIS -->|Store Results| MEMORY_MGR
    MEMORY_AGENT -->|Retrieve| MEMORY_MGR
    MEMORY_MGR --> VECTOR
    MEMORY_MGR --> KB
    RESEARCH -->|Results| COORD
    ANALYSIS -->|Results| COORD
    MEMORY_AGENT -->|Results| COORD
    COORD -->|Final Answer| API
    API -->|Response| UI
    
    style COORD fill:#ff9800
    style RESEARCH fill:#9c27b0
    style ANALYSIS fill:#9c27b0
    style MEMORY_AGENT fill:#9c27b0
    style MEMORY_MGR fill:#ffeb3b
    style LLM fill:#9e9e9e
    style UI fill:#2196f3
    style API fill:#4caf50
"""
    return mermaid_code

def print_instructions():
    """Print instructions for generating the one-pager PDF."""
    print("="*70)
    print("ONE-PAGER ABSTRACT GENERATION GUIDE")
    print("="*70)
    print("\n📄 Files Created:")
    print("  1. ONE_PAGER_PDF_CONTENT.md - Main content for PDF")
    print("  2. SYSTEM_DIAGRAM_TEXT.md - Diagram generation instructions")
    print("  3. CREATE_PDF_GUIDE.md - Step-by-step PDF creation guide")
    print("  4. ONE_PAGER_ABSTRACT.md - Full abstract (reference)")
    print("\n🎨 STEP 1: Generate System Diagram")
    print("  Option A - Mermaid Live Editor (Easiest):")
    print("    1. Go to: https://mermaid.live")
    print("    2. Copy the Mermaid code from SYSTEM_DIAGRAM_TEXT.md")
    print("    3. Paste and click 'Download PNG'")
    print("    4. Save as 'system_diagram.png' in this folder")
    print("\n  Option B - ChatGPT + Figma:")
    print("    1. Use the prompt from SYSTEM_DIAGRAM_TEXT.md")
    print("    2. Ask ChatGPT to create the diagram")
    print("    3. Export as PNG")
    print("\n  Option C - Draw.io:")
    print("    1. Go to: https://app.diagrams.net")
    print("    2. Create diagram using component list")
    print("    3. Export as PNG")
    print("\n📝 STEP 2: Add Diagram to Content")
    print("  1. Open ONE_PAGER_PDF_CONTENT.md")
    print("  2. Find '[INSERT DIAGRAM HERE]'")
    print("  3. Replace with: ![System Diagram](system_diagram.png)")
    print("\n📄 STEP 3: Convert to PDF")
    print("  Option A - Online (Easiest):")
    print("    1. Go to: https://dillinger.io")
    print("    2. Paste content from ONE_PAGER_PDF_CONTENT.md")
    print("    3. Click 'Export as' → 'PDF'")
    print("\n  Option B - Pandoc (if installed):")
    print("    pandoc ONE_PAGER_PDF_CONTENT.md -o ONE_PAGER_ABSTRACT.pdf")
    print("\n  Option C - Word/Google Docs:")
    print("    1. Copy content to Word/Google Docs")
    print("    2. Insert diagram image")
    print("    3. Export/Save as PDF")
    print("\n✅ Quick Start:")
    print("  1. Generate diagram at https://mermaid.live")
    print("  2. Save as system_diagram.png")
    print("  3. Use https://dillinger.io to convert to PDF")
    print("\n" + "="*70)

if __name__ == "__main__":
    # Save Mermaid code to file
    mermaid_code = create_diagram_mermaid()
    with open("system_diagram.mmd", "w", encoding="utf-8") as f:
        f.write(mermaid_code.strip())
    print("✅ Created system_diagram.mmd (Mermaid diagram code)")
    print()
    
    # Print instructions
    print_instructions()
    
    print("\n💡 Tip: The easiest way is:")
    print("   1. Go to https://mermaid.live")
    print("   2. Open system_diagram.mmd and copy the code")
    print("   3. Paste in Mermaid Live Editor → Download PNG")
    print("   4. Use https://dillinger.io to convert ONE_PAGER_PDF_CONTENT.md to PDF")

