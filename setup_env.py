"""Helper script to create .env file if it doesn't exist."""

import os

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_path = ".env"
    env_example_path = ".env.example"
    
    if os.path.exists(env_path):
        print(".env file already exists. Skipping creation.")
        return
    
    env_content = """# Groq API Configuration (Optional but recommended)
# Get your free API key from: https://console.groq.com/
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=mixtral-8x7b-32768

# System Configuration
ENABLE_LLM=true
LOG_LEVEL=INFO

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
"""
    
    try:
        with open(env_path, "w") as f:
            f.write(env_content)
        print(f".env file created successfully at {env_path}")
        print("\nNext steps:")
        print("1. Edit .env and add your Groq API key (optional but recommended)")
        print("2. The system will work without LLM using rule-based fallbacks")
    except Exception as e:
        print(f"Error creating .env file: {e}")

if __name__ == "__main__":
    create_env_file()

