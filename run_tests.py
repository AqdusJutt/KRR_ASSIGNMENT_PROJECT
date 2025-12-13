"""Test runner for the 5 sample scenarios."""

import os
from datetime import datetime
from agents.coordinator import CoordinatorAgent
from memory.memory_manager import MemoryManager
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Ensure outputs directory exists
os.makedirs("outputs", exist_ok=True)

def run_test(scenario_name: str, query: str, coordinator: CoordinatorAgent) -> str:
    """Run a test scenario and return formatted output."""
    output = []
    output.append("="*80)
    output.append(f"TEST SCENARIO: {scenario_name.upper()}")
    output.append("="*80)
    output.append(f"\nTimestamp: {datetime.now().isoformat()}")
    output.append(f"Query: {query}\n")
    output.append("-"*80)
    output.append("PROCESSING...")
    output.append("-"*80 + "\n")
    
    try:
        result = coordinator.process_query(query)
        
        # Task Plan
        output.append("TASK PLAN:")
        output.append("-"*40)
        plan = result.get('task_plan', {})
        output.append(f"Complexity: {plan.get('complexity', 'unknown')}")
        output.append(f"Requires Research: {plan.get('requires_research', False)}")
        output.append(f"Requires Analysis: {plan.get('requires_analysis', False)}")
        output.append(f"Requires Memory: {plan.get('requires_memory', False)}")
        output.append(f"Subtasks: {', '.join(plan.get('subtasks', []))}")
        output.append("")
        
        # Agent Results
        output.append("AGENT RESULTS:")
        output.append("-"*40)
        for i, agent_result in enumerate(result.get('agent_results', []), 1):
            agent_name = agent_result.get('agent', 'Unknown')
            confidence = agent_result.get('confidence', 0)
            output.append(f"\n[{i}] {agent_name}")
            output.append(f"Confidence: {confidence:.2%}")
            output.append(f"Result:")
            output.append(agent_result.get('result', 'N/A'))
            output.append("")
        
        # Final Answer
        output.append("="*80)
        output.append("FINAL ANSWER:")
        output.append("="*80)
        output.append(result.get('final_answer', 'No answer available.'))
        output.append("")
        
        # Metadata
        output.append("-"*80)
        output.append("METADATA:")
        output.append("-"*40)
        output.append(f"Task ID: {result.get('task_id')}")
        output.append(f"Overall Confidence: {result.get('overall_confidence', 0):.2%}")
        output.append(f"Memory Context Used: {result.get('memory_context_used', False)}")
        output.append(f"Agents Used: {', '.join([r.get('agent') for r in result.get('agent_results', [])])}")
        output.append("")
        output.append("="*80)
        output.append("\n")
        
    except Exception as e:
        output.append(f"ERROR: {str(e)}")
        logger.error(f"Error in test scenario {scenario_name}: {e}")
    
    return "\n".join(output)

def main():
    """Run all test scenarios."""
    print("\n" + "="*80)
    print("MULTI-AGENT CHAT SYSTEM - Test Runner")
    print("="*80 + "\n")
    
    # Initialize coordinator (shared across tests for memory continuity)
    memory_manager = MemoryManager()
    coordinator = CoordinatorAgent(memory_manager=memory_manager, enable_llm=True)
    
    llm_status = "enabled" if (coordinator.llm_client and coordinator.llm_client.is_available()) else "disabled (fallback mode)"
    print(f"System initialized. LLM: {llm_status}\n")
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "simple_query",
            "query": "What are the main types of neural networks?",
            "file": "outputs/simple_query.txt"
        },
        {
            "name": "complex_query",
            "query": "Research transformer architectures, analyze their computational efficiency, and summarize key trade-offs.",
            "file": "outputs/complex_query.txt"
        },
        {
            "name": "memory_test",
            "query": "What did we discuss about neural networks earlier?",
            "file": "outputs/memory_test.txt"
        },
        {
            "name": "multi_step",
            "query": "Find recent papers on reinforcement learning, analyze their methodologies, and identify common challenges.",
            "file": "outputs/multi_step.txt"
        },
        {
            "name": "collaborative",
            "query": "Compare two machine-learning approaches and recommend which is better for our use case.",
            "file": "outputs/collaborative.txt"
        }
    ]
    
    print("Running test scenarios...\n")
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"[{i}/{len(test_scenarios)}] Running: {scenario['name']}...")
        
        output = run_test(scenario['name'], scenario['query'], coordinator)
        
        # Write to file
        with open(scenario['file'], 'w', encoding='utf-8') as f:
            f.write(output)
        
        print(f"  ✓ Saved to {scenario['file']}")
        print()
    
    print("="*80)
    print("All tests completed!")
    print("="*80)
    print(f"\nOutput files saved in the 'outputs/' directory:\n")
    for scenario in test_scenarios:
        print(f"  - {scenario['file']}")
    print()

if __name__ == "__main__":
    main()

