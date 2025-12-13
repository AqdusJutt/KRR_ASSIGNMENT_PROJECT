"""Console client for interacting with the multi-agent system."""

import sys
from agents.coordinator import CoordinatorAgent
from memory.memory_manager import MemoryManager
from utils.logger import setup_logger

logger = setup_logger(__name__)

def print_result(result: dict):
    """Pretty print the result."""
    print("\n" + "="*80)
    print("RESULT")
    print("="*80)
    print(f"\nTask ID: {result.get('task_id')}")
    print(f"Query: {result.get('user_query')}")
    print(f"Complexity: {result.get('task_plan', {}).get('complexity', 'unknown')}")
    print(f"Overall Confidence: {result.get('overall_confidence', 0):.2%}")
    
    print("\n" + "-"*80)
    print("TASK PLAN")
    print("-"*80)
    plan = result.get('task_plan', {})
    print(f"Requires Research: {plan.get('requires_research', False)}")
    print(f"Requires Analysis: {plan.get('requires_analysis', False)}")
    print(f"Requires Memory: {plan.get('requires_memory', False)}")
    print(f"Subtasks: {', '.join(plan.get('subtasks', []))}")
    
    print("\n" + "-"*80)
    print("AGENT RESULTS")
    print("-"*80)
    for i, agent_result in enumerate(result.get('agent_results', []), 1):
        agent_name = agent_result.get('agent', 'Unknown')
        confidence = agent_result.get('confidence', 0)
        print(f"\n[{i}] {agent_name} (confidence: {confidence:.2%})")
        print(f"Result:\n{agent_result.get('result', 'N/A')}")
    
    print("\n" + "-"*80)
    print("FINAL ANSWER")
    print("-"*80)
    print(result.get('final_answer', 'No answer available.'))
    print("\n" + "="*80 + "\n")

def main():
    """Main console client loop."""
    print("\n" + "="*80)
    print("MULTI-AGENT CHAT SYSTEM - Console Client")
    print("="*80)
    print("\nEnter your queries (type 'exit' or 'quit' to end, 'help' for commands)\n")
    
    # Initialize system
    memory_manager = MemoryManager()
    coordinator = CoordinatorAgent(memory_manager=memory_manager, enable_llm=True)
    
    llm_status = "enabled" if (coordinator.llm_client and coordinator.llm_client.is_available()) else "disabled (fallback mode)"
    print(f"System initialized. LLM: {llm_status}\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye!")
                break
            
            if user_input.lower() == 'help':
                print("\nCommands:")
                print("  exit/quit/q - Exit the program")
                print("  help - Show this help message")
                print("  history - Show conversation history")
                print("  clear - Clear memory")
                print("\nJust type your question normally to get an answer!\n")
                continue
            
            if user_input.lower() == 'history':
                history = coordinator.memory_manager.get_conversation_history(limit=5)
                if history:
                    print("\nRecent Conversation History:")
                    for entry in history:
                        print(f"\n[{entry.get('timestamp')}]")
                        print(f"Q: {entry.get('user_query')}")
                else:
                    print("\nNo conversation history found.")
                print()
                continue
            
            if user_input.lower() == 'clear':
                response = input("Are you sure you want to clear all memory? (yes/no): ")
                if response.lower() == 'yes':
                    coordinator.memory_manager.vector_store.clear()
                    coordinator.memory_manager.conversation_history = []
                    coordinator.memory_manager.knowledge_base = []
                    print("Memory cleared.\n")
                else:
                    print("Memory clear cancelled.\n")
                continue
            
            # Process query
            print("\nProcessing...\n")
            result = coordinator.process_query(user_input)
            print_result(result)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"\nError: {e}\n")

if __name__ == "__main__":
    main()

