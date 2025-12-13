"""Memory Agent - Manages long-term storage, retrieval, and context updates."""

from typing import Dict, Any, List, Optional
from memory.memory_manager import MemoryManager
from utils.logger import setup_logger, log_agent_call

logger = setup_logger(__name__)

class MemoryAgent:
    """Agent responsible for memory management and retrieval."""
    
    def __init__(self, memory_manager: Optional[MemoryManager] = None):
        """Initialize Memory Agent with memory manager."""
        self.memory_manager = memory_manager or MemoryManager()
        self.name = "MemoryAgent"
        logger.info(f"{self.name} initialized")
    
    def store(self, topic: str, content: str, source_agent: str, 
             confidence: float = 1.0, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Store information in memory."""
        log_agent_call(logger, self.name, f"Storing: {topic}", {"source": source_agent})
        
        knowledge_id = self.memory_manager.store_knowledge(
            topic=topic,
            content=content,
            source_agent=source_agent,
            confidence=confidence,
            metadata=metadata or {}
        )
        
        return knowledge_id
    
    def retrieve(self, query: str, search_type: str = "hybrid", 
                top_k: int = 5) -> Dict[str, Any]:
        """Retrieve information from memory."""
        log_agent_call(logger, self.name, f"Retrieving: {query}", {"search_type": search_type})
        
        if search_type == "vector" or search_type == "hybrid":
            vector_results = self.memory_manager.vector_search(query, top_k=top_k)
        else:
            vector_results = []
        
        if search_type == "keyword" or search_type == "hybrid":
            keywords = query.lower().split()
            keyword_results = self.memory_manager.search_by_keywords(keywords, top_k=top_k)
        else:
            keyword_results = []
        
        # Combine results
        combined_results = []
        seen_ids = set()
        
        # Add vector results first (higher priority for semantic similarity)
        for entry, score in vector_results:
            entry_id = entry.get("knowledge_id") or entry.get("conversation_id") or entry.get("id")
            if entry_id and entry_id not in seen_ids:
                combined_results.append({
                    **entry,
                    "similarity_score": score,
                    "source": "vector_search"
                })
                seen_ids.add(entry_id)
        
        # Add keyword results
        for entry in keyword_results:
            entry_id = entry.get("id")
            if entry_id and entry_id not in seen_ids:
                combined_results.append({
                    **entry,
                    "source": "keyword_search"
                })
                seen_ids.add(entry_id)
        
        # Format results
        if not combined_results:
            return {
                "agent": self.name,
                "query": query,
                "result": "No relevant information found in memory.",
                "confidence": 0.3,
                "results": []
            }
        
        result_text = f"Found {len(combined_results)} relevant memory entries:\n\n"
        
        for i, entry in enumerate(combined_results[:top_k], 1):
            topic = entry.get("topic", "Unknown")
            content = entry.get("content", "")
            timestamp = entry.get("timestamp", "Unknown")
            source = entry.get("source_agent", "Unknown")
            similarity = entry.get("similarity_score", 0)
            
            result_text += f"{i}. [{topic}] (from {source}, {timestamp})\n"
            if similarity > 0:
                result_text += f"   Similarity: {similarity:.3f}\n"
            result_text += f"   {content}\n\n"
        
        confidence = min(0.9, 0.5 + (len(combined_results) * 0.1))
        if combined_results and combined_results[0].get("similarity_score", 0) > 0.7:
            confidence = min(0.95, confidence + 0.1)
        
        return {
            "agent": self.name,
            "query": query,
            "result": result_text,
            "confidence": confidence,
            "results": combined_results[:top_k]
        }
    
    def search_by_topic(self, topic: str, top_k: int = 5) -> Dict[str, Any]:
        """Search memory by topic."""
        log_agent_call(logger, self.name, f"Searching by topic: {topic}")
        
        results = self.memory_manager.search_by_topic(topic, top_k=top_k)
        
        if not results:
            return {
                "agent": self.name,
                "query": f"topic: {topic}",
                "result": f"No information found about '{topic}' in memory.",
                "confidence": 0.3,
                "results": []
            }
        
        result_text = f"Information about '{topic}':\n\n"
        
        for i, entry in enumerate(results, 1):
            content = entry.get("content", "")
            timestamp = entry.get("timestamp", "Unknown")
            source = entry.get("source_agent", "Unknown")
            
            result_text += f"{i}. (from {source}, {timestamp})\n"
            result_text += f"   {content}\n\n"
        
        return {
            "agent": self.name,
            "query": f"topic: {topic}",
            "result": result_text,
            "confidence": 0.8,
            "results": results
        }
    
    def get_conversation_context(self, limit: int = 3) -> Dict[str, Any]:
        """Get recent conversation context."""
        log_agent_call(logger, self.name, f"Retrieving conversation context (last {limit})")
        
        history = self.memory_manager.get_conversation_history(limit=limit)
        
        if not history:
            return {
                "agent": self.name,
                "query": "conversation context",
                "result": "No previous conversations found.",
                "confidence": 0.3,
                "history": []
            }
        
        context_text = f"Recent Conversation History (last {len(history)} interactions):\n\n"
        
        for entry in history:
            timestamp = entry.get("timestamp", "Unknown")
            user_query = entry.get("user_query", "")
            
            context_text += f"[{timestamp}]\n"
            context_text += f"User: {user_query}\n"
            
            responses = entry.get("agent_responses", [])
            if responses:
                context_text += "Agents responded with:\n"
                for resp in responses[:2]:  # Limit to first 2 responses
                    agent = resp.get("agent", "Unknown")
                    result = resp.get("result", "")[:200]  # Truncate
                    context_text += f"  - {agent}: {result}...\n"
            
            context_text += "\n"
        
        return {
            "agent": self.name,
            "query": "conversation context",
            "result": context_text,
            "confidence": 0.85,
            "history": history
        }
    
    def update_agent_state(self, agent_name: str, task_id: str, state: Dict[str, Any]):
        """Update state for a specific agent."""
        log_agent_call(logger, self.name, f"Updating state for {agent_name}", {"task_id": task_id})
        self.memory_manager.update_agent_state(agent_name, task_id, state)
    
    def get_agent_state(self, agent_name: str, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Get state for a specific agent."""
        state = self.memory_manager.get_agent_state(agent_name, task_id)
        return {
            "agent": self.name,
            "query": f"state for {agent_name}",
            "result": f"Retrieved state: {len(state)} entries",
            "confidence": 0.9,
            "state": state
        }

