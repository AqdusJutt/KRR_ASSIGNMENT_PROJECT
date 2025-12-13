"""Coordinator Agent - Orchestrates worker agents and manages task flow."""

import uuid
from typing import Dict, Any, List, Optional
from utils.logger import setup_logger, log_agent_call
from utils.llm_client import LLMClient
from .research_agent import ResearchAgent
from .analysis_agent import AnalysisAgent
from .memory_agent import MemoryAgent
from memory.memory_manager import MemoryManager

logger = setup_logger(__name__)

class CoordinatorAgent:
    """Manager agent that coordinates worker agents."""
    
    def __init__(self, memory_manager: Optional[MemoryManager] = None, enable_llm: bool = True):
        """Initialize Coordinator with worker agents."""
        self.memory_manager = memory_manager or MemoryManager()
        self.llm_client = LLMClient() if enable_llm else None
        
        # Initialize worker agents
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.memory_agent = MemoryAgent(self.memory_manager)
        
        self.name = "CoordinatorAgent"
        self.conversation_state = {}
        
        logger.info(f"{self.name} initialized with LLM: {self.llm_client.is_available() if self.llm_client else False}")
    
    def process_query(self, user_query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a user query by coordinating appropriate agents."""
        task_id = str(uuid.uuid4())[:8]
        
        log_agent_call(logger, self.name, f"Processing query: {user_query[:100]}...", {"task_id": task_id})
        
        # Step 1: Analyze query complexity and decompose task
        task_plan = self._decompose_task(user_query)
        log_agent_call(logger, self.name, "Task decomposition complete", task_plan)
        
        # Step 2: Check memory for relevant context
        memory_context = None
        query_lower = user_query.lower()
        is_memory_query = (task_plan.get("requires_memory") or 
                          any(keyword in query_lower for keyword in 
                              ["earlier", "before", "discuss", "remember", "learned", "we talked", "previous", "past"]))
        
        if is_memory_query:
            # Try to extract topic/keywords from query for better search
            # Extract words after "about", "on", "regarding" for better matching
            search_query = user_query
            if "about" in query_lower:
                search_query = query_lower.split("about")[-1].strip()
            elif "on" in query_lower and "earlier" in query_lower or "before" in query_lower:
                parts = query_lower.split("on")
                if len(parts) > 1:
                    search_query = parts[-1].split("earlier")[0].split("before")[0].strip()
            
            # Also search conversation history
            memory_result = self.memory_agent.retrieve(search_query, search_type="hybrid", top_k=5)
            
            # If no results, try searching conversation history directly
            if not memory_result.get("results"):
                history = self.memory_manager.get_conversation_history(limit=10)
                # Search through history for relevant conversations
                for conv in history:
                    user_q = conv.get("user_query", "").lower()
                    if any(word in user_q for word in search_query.split() if len(word) > 3):
                        # Found relevant conversation, extract agent responses
                        responses = conv.get("agent_responses", [])
                        if responses:
                            # Create a memory entry from this conversation
                            memory_result = {
                                "agent": "MemoryAgent",
                                "query": user_query,
                                "result": f"From earlier conversation: {conv.get('user_query', '')}\n\n" + 
                                         "\n".join([r.get("result", "")[:200] for r in responses[:2]]),
                                "confidence": 0.8,
                                "results": [{
                                    "type": "conversation",
                                    "user_query": conv.get("user_query", ""),
                                    "agent_responses": responses,
                                    "timestamp": conv.get("timestamp", "")
                                }]
                            }
                            break
            
            if memory_result.get("results"):
                memory_context = memory_result
                log_agent_call(logger, self.name, "Retrieved memory context", 
                             {"entries_found": len(memory_result.get("results", []))})
        
        # Step 3: Execute task plan
        agent_results = []
        
        # Research phase
        research_data = None
        if task_plan.get("requires_research"):
            research_result = self.research_agent.research(user_query, context=memory_context)
            agent_results.append(research_result)
            research_data = research_result.get("results", [])
            log_agent_call(logger, self.name, "Research phase complete", 
                         {"results_count": len(research_data)})
            
            # Store findings in memory
            if research_data:
                for item in research_data[:3]:  # Store top 3 findings
                    topic = item.get("topic", "general")
                    content = item.get("content", str(item))
                    self.memory_agent.store(
                        topic=topic,
                        content=content,
                        source_agent="ResearchAgent",
                        confidence=item.get("confidence", 0.8)
                    )
        
        # Analysis phase (may depend on research)
        if task_plan.get("requires_analysis"):
            analysis_result = self.analysis_agent.analyze(
                user_query, 
                data=research_data, 
                context=memory_context
            )
            agent_results.append(analysis_result)
            log_agent_call(logger, self.name, "Analysis phase complete",
                         {"confidence": analysis_result.get("confidence", 0.5)})
            
            # Store analysis findings
            if analysis_result.get("result"):
                self.memory_agent.store(
                    topic="analysis",
                    content=analysis_result.get("result", "")[:500],  # Truncate
                    source_agent="AnalysisAgent",
                    confidence=analysis_result.get("confidence", 0.7)
                )
        
        # Memory-only queries
        if task_plan.get("requires_memory") and not task_plan.get("requires_research") and not task_plan.get("requires_analysis"):
            # If we already have memory context from Step 2, use it
            if memory_context and memory_context.get("results"):
                agent_results.append(memory_context)
            elif not memory_context or not memory_context.get("results"):
                # Try broader search - extract topic from query
                query_words = user_query.lower().split()
                # Find topic keywords (words after "about", "on", or key nouns)
                topic_keywords = []
                for i, word in enumerate(query_words):
                    if word in ["about", "on", "regarding", "concerning"] and i + 1 < len(query_words):
                        topic_keywords = query_words[i+1:]
                        break
                
                # If no "about" found, use all words except common stop words
                if not topic_keywords:
                    stop_words = ["what", "did", "we", "learn", "earlier", "before", "discuss", "remember", "the", "a", "an"]
                    topic_keywords = [w for w in query_words if w not in stop_words and len(w) > 3]
                
                search_topic = " ".join(topic_keywords[:3]) if topic_keywords else user_query
                
                # Try topic search
                memory_result = self.memory_agent.search_by_topic(search_topic, top_k=5)
                
                # If still no results, try vector search with full query
                if not memory_result.get("results"):
                    memory_result = self.memory_agent.retrieve(user_query, search_type="hybrid", top_k=5)
                
                if memory_result.get("results"):
                    agent_results.append(memory_result)
                    memory_context = memory_result
                else:
                    # Last resort: search all conversation history
                    history = self.memory_manager.get_conversation_history(limit=20)
                    relevant_convs = []
                    for conv in history:
                        conv_text = (conv.get("user_query", "") + " " + 
                                   " ".join([r.get("result", "") for r in conv.get("agent_responses", [])])).lower()
                        if any(word in conv_text for word in topic_keywords if len(word) > 3):
                            relevant_convs.append(conv)
                    
                    if relevant_convs:
                        result_text = "Found in previous conversations:\n\n"
                        for conv in relevant_convs[:3]:
                            result_text += f"Q: {conv.get('user_query', '')}\n"
                            for resp in conv.get("agent_responses", [])[:2]:
                                result_text += f"A: {resp.get('result', '')[:300]}...\n"
                            result_text += "\n"
                        
                        memory_result = {
                            "agent": "MemoryAgent",
                            "query": user_query,
                            "result": result_text,
                            "confidence": 0.75,
                            "results": relevant_convs
                        }
                        agent_results.append(memory_result)
                        memory_context = memory_result
        
        # Handle conversational queries when no agents were used
        if not agent_results and not task_plan.get("requires_research") and not task_plan.get("requires_analysis") and not task_plan.get("requires_memory"):
            # Provide a friendly conversational response
            query_lower = user_query.lower().strip()
            if any(word in query_lower for word in ["hello", "hi", "hey", "greetings"]):
                final_answer = "Hello! I'm a multi-agent AI system. I can help you with research, analysis, and memory tasks. How can I assist you today?"
            elif any(word in query_lower for word in ["thanks", "thank you"]):
                final_answer = "You're welcome! Feel free to ask me anything else."
            elif any(word in query_lower for word in ["how are you", "how do you do"]):
                final_answer = "I'm functioning well! I'm ready to help with your queries. What would you like to know?"
            else:
                # Default helpful response
                final_answer = "I'm here to help! You can ask me about AI, machine learning, neural networks, or any other technical topics. What would you like to know?"
        else:
            # Step 4: Synthesize results
            final_answer = self._synthesize_results(user_query, agent_results, task_plan)
        
        # Step 5: Store conversation
        self.memory_manager.store_conversation(
            user_query=user_query,
            agent_responses=agent_results,
            metadata={
                "task_id": task_id,
                "complexity": task_plan.get("complexity", "unknown"),
                "agents_used": [r.get("agent") for r in agent_results]
            }
        )
        
        # Step 6: Update agent state
        self.memory_agent.update_agent_state(self.name, task_id, {
            "query": user_query,
            "plan": task_plan,
            "agents_used": [r.get("agent") for r in agent_results],
            "final_confidence": self._calculate_overall_confidence(agent_results)
        })
        
        return {
            "task_id": task_id,
            "user_query": user_query,
            "task_plan": task_plan,
            "agent_results": agent_results,
            "final_answer": final_answer,
            "memory_context_used": memory_context is not None,
            "overall_confidence": self._calculate_overall_confidence(agent_results)
        }
    
    def _decompose_task(self, query: str) -> Dict[str, Any]:
        """Decompose task using LLM or rule-based approach."""
        if self.llm_client and self.llm_client.is_available():
            try:
                return self.llm_client.decompose_task(query)
            except Exception as e:
                logger.warning(f"LLM decomposition failed: {e}, using rule-based")
        
        # Rule-based fallback
        return self._rule_based_decomposition(query)
    
    def _rule_based_decomposition(self, query: str) -> Dict[str, Any]:
        """Rule-based task decomposition."""
        query_lower = query.lower().strip()
        
        # Handle conversational queries (greetings, simple questions)
        conversational_keywords = ["hello", "hi", "hey", "greetings", "how are you", "thanks", "thank you"]
        if any(keyword in query_lower for keyword in conversational_keywords) or len(query_lower.split()) <= 2:
            # For very short queries, treat as research to give a helpful response
            return {
                "requires_research": True,
                "requires_analysis": False,
                "requires_memory": False,
                "complexity": "simple",
                "subtasks": ["Provide a conversational response"]
            }
        
        requires_research = any(keyword in query_lower for keyword in 
                               ["find", "search", "research", "what", "tell me about", "information", "types", 
                                "examples", "example", "give examples", "give", "list", "show", "define", "explain", "describe",
                                "who", "when", "where", "why", "how", "agent", "agents"])
        requires_analysis = any(keyword in query_lower for keyword in 
                               ["compare", "analyze", "evaluate", "which", "better", "effectiveness", "efficiency", 
                                "trade-off", "recommend", "should", "best"])
        requires_memory = any(keyword in query_lower for keyword in 
                             ["remember", "discuss", "earlier", "before", "previous", "learned", "we talked", 
                              "discussed", "mentioned"])
        
        # Default to research if query is a question or seems informational
        if not requires_research and not requires_analysis and not requires_memory:
            # If it looks like a question or has question words, default to research
            if "?" in query or any(word in query_lower for word in ["what", "who", "how", "why", "when", "where", 
                                                                     "examples", "example", "give", "list"]):
                requires_research = True
        
        # Determine complexity
        complexity = "simple"
        agent_count = sum([requires_research, requires_analysis, requires_memory])
        if agent_count >= 2:
            complexity = "complex"
        elif agent_count == 1:
            complexity = "medium"
        
        subtasks = []
        if requires_research:
            subtasks.append("Research information on the topic")
        if requires_analysis:
            subtasks.append("Analyze and compare findings")
        if requires_memory:
            subtasks.append("Retrieve relevant past conversations")
        
        return {
            "requires_research": requires_research,
            "requires_analysis": requires_analysis,
            "requires_memory": requires_memory,
            "complexity": complexity,
            "subtasks": subtasks if subtasks else ["Handle query directly"]
        }
    
    def _synthesize_results(self, query: str, agent_results: List[Dict[str, Any]], 
                          task_plan: Dict[str, Any]) -> str:
        """Synthesize results from multiple agents into final answer."""
        if not agent_results:
            return "I apologize, but I couldn't process your query. Please try rephrasing it."
        
        # Use LLM for summarization if available
        if self.llm_client and self.llm_client.is_available() and len(agent_results) > 1:
            try:
                summary = self.llm_client.summarize_results(agent_results)
                return summary
            except Exception as e:
                logger.warning(f"LLM summarization failed: {e}, using rule-based")
        
        # Rule-based synthesis
        if len(agent_results) == 1:
            return agent_results[0].get("result", "No result available.")
        
        # Combine multiple results
        synthesized = []
        
        for result in agent_results:
            agent_name = result.get("agent", "Unknown")
            result_text = result.get("result", "")
            
            if result_text:
                synthesized.append(f"**{agent_name}**:\n{result_text}\n")
        
        return "\n".join(synthesized)
    
    def _calculate_overall_confidence(self, agent_results: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence from agent results."""
        if not agent_results:
            return 0.3
        
        confidences = [r.get("confidence", 0.5) for r in agent_results if r.get("confidence")]
        
        if not confidences:
            return 0.5
        
        # Average confidence, with slight penalty for multiple agents (uncertainty)
        avg_confidence = sum(confidences) / len(confidences)
        
        # Slight penalty if many agents (more complexity = more uncertainty)
        if len(agent_results) > 2:
            avg_confidence *= 0.95
        
        return min(0.95, avg_confidence)

