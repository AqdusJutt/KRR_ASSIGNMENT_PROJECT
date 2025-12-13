"""Verification script to check if the system is set up correctly."""

import os
import sys

def check_file(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} MISSING: {filepath}")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists."""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✓ {description}: {dirpath}")
        return True
    else:
        print(f"✗ {description} MISSING: {dirpath}")
        return False

def main():
    """Run verification checks."""
    print("="*60)
    print("Multi-Agent Chat System - Setup Verification")
    print("="*60)
    print()
    
    checks_passed = 0
    total_checks = 0
    
    # Core Python files
    print("Core Files:")
    print("-" * 60)
    core_files = [
        ("main.py", "FastAPI application"),
        ("console_client.py", "Console client"),
        ("run_tests.py", "Test runner"),
        ("requirements.txt", "Python dependencies"),
    ]
    
    for filepath, desc in core_files:
        total_checks += 1
        if check_file(filepath, desc):
            checks_passed += 1
    
    print()
    
    # Agent files
    print("Agent Files:")
    print("-" * 60)
    agent_files = [
        ("agents/coordinator.py", "Coordinator agent"),
        ("agents/research_agent.py", "Research agent"),
        ("agents/analysis_agent.py", "Analysis agent"),
        ("agents/memory_agent.py", "Memory agent"),
    ]
    
    for filepath, desc in agent_files:
        total_checks += 1
        if check_file(filepath, desc):
            checks_passed += 1
    
    print()
    
    # Memory files
    print("Memory System Files:")
    print("-" * 60)
    memory_files = [
        ("memory/vector_store.py", "Vector store"),
        ("memory/memory_manager.py", "Memory manager"),
    ]
    
    for filepath, desc in memory_files:
        total_checks += 1
        if check_file(filepath, desc):
            checks_passed += 1
    
    print()
    
    # Utility files
    print("Utility Files:")
    print("-" * 60)
    util_files = [
        ("utils/llm_client.py", "LLM client"),
        ("utils/logger.py", "Logger"),
    ]
    
    for filepath, desc in util_files:
        total_checks += 1
        if check_file(filepath, desc):
            checks_passed += 1
    
    print()
    
    # Frontend files
    print("Frontend Files:")
    print("-" * 60)
    frontend_files = [
        ("frontend/package.json", "Frontend package.json"),
        ("frontend/pages/index.tsx", "Frontend main page"),
    ]
    
    for filepath, desc in frontend_files:
        total_checks += 1
        if check_file(filepath, desc):
            checks_passed += 1
    
    print()
    
    # Docker files
    print("Docker Files:")
    print("-" * 60)
    docker_files = [
        ("Dockerfile", "Backend Dockerfile"),
        ("docker-compose.yaml", "Docker Compose config"),
        ("frontend/Dockerfile", "Frontend Dockerfile"),
    ]
    
    for filepath, desc in docker_files:
        total_checks += 1
        if check_file(filepath, desc):
            checks_passed += 1
    
    print()
    
    # Directories
    print("Required Directories:")
    print("-" * 60)
    directories = [
        ("outputs", "Outputs directory"),
        ("agents", "Agents directory"),
        ("memory", "Memory directory"),
        ("utils", "Utils directory"),
        ("frontend", "Frontend directory"),
    ]
    
    for dirpath, desc in directories:
        total_checks += 1
        if check_directory(dirpath, desc):
            checks_passed += 1
    
    print()
    
    # Python version check
    print("System Check:")
    print("-" * 60)
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 9:
        print(f"✓ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        checks_passed += 1
    else:
        print(f"✗ Python version too old: {python_version.major}.{python_version.minor}.{python_version.micro} (need 3.9+)")
    total_checks += 1
    
    # Environment file
    if os.path.exists(".env"):
        print("✓ .env file exists")
        checks_passed += 1
    else:
        print("⚠ .env file not found (will be created on first run)")
    total_checks += 1
    
    print()
    print("="*60)
    print(f"Results: {checks_passed}/{total_checks} checks passed")
    print("="*60)
    
    if checks_passed == total_checks:
        print("\n🎉 All checks passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run tests: python run_tests.py")
        print("3. Start backend: uvicorn main:app --reload")
    else:
        print("\n⚠️  Some checks failed. Please review the missing files.")
    
    print()

if __name__ == "__main__":
    main()

