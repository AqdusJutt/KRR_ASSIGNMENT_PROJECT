"""Memory manager for structured memory operations."""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from .vector_store import VectorStore

class MemoryManager:
    """Manages structured memory with vector search capabilities."""
    
    def __init__(self, vector_store_path: Optional[str] = None):
        """Initialize memory manager with vector store."""
        self.vector_store = VectorStore()
        self.conversation_history = []
        self.knowledge_base = []
        self.agent_state = {}  # Track agent-specific state
        
        if vector_store_path:
            self.vector_store.load(vector_store_path)
    
    def store_conversation(self, user_query: str, agent_responses: List[Dict[str, Any]], 
                          metadata: Optional[Dict[str, Any]] = None) -> str:
        """Store a conversation turn."""
        conversation_entry = {
            "id": f"conv_{len(self.conversation_history)}",
            "timestamp": datetime.now().isoformat(),
            "user_query": user_query,
            "agent_responses": agent_responses,
            "metadata": metadata or {}
        }
        
        self.conversation_history.append(conversation_entry)
        
        # Also store in vector store for semantic search
        content = f"User: {user_query}\nResponses: {json.dumps(agent_responses)}"
        self.vector_store.add(content, {
            "type": "conversation",
            "conversation_id": conversation_entry["id"],
            **conversation_entry
        })
        
        return conversation_entry["id"]
    
    def store_knowledge(self, topic: str, content: str, source_agent: str, 
                       confidence: float = 1.0, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Store a knowledge fact with provenance."""
        knowledge_entry = {
            "id": f"kb_{len(self.knowledge_base)}",
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "content": content,
            "source_agent": source_agent,
            "confidence": confidence,
            "metadata": metadata or {}
        }
        
        self.knowledge_base.append(knowledge_entry)
        
        # Store in vector store
        text_content = f"Topic: {topic}\nContent: {content}"
        self.vector_store.add(text_content, {
            "type": "knowledge",
            "knowledge_id": knowledge_entry["id"],
            **knowledge_entry
        })
        
        return knowledge_entry["id"]
    
    def update_agent_state(self, agent_name: str, task_id: str, state: Dict[str, Any]):
        """Update state for a specific agent and task."""
        if agent_name not in self.agent_state:
            self.agent_state[agent_name] = {}
        
        self.agent_state[agent_name][task_id] = {
            **state,
            "last_updated": datetime.now().isoformat()
        }
    
    def search_by_topic(self, topic: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search knowledge base by topic keyword."""
        results = []
        topic_lower = topic.lower()
        
        for entry in self.knowledge_base:
            if topic_lower in entry["topic"].lower() or topic_lower in entry["content"].lower():
                results.append(entry)
        
        return results[:top_k]
    
    def search_by_keywords(self, keywords: List[str], top_k: int = 5) -> List[Dict[str, Any]]:
        """Search by multiple keywords."""
        results = []
        keyword_lower = [k.lower() for k in keywords]
        
        for entry in self.knowledge_base:
            text = f"{entry['topic']} {entry['content']}".lower()
            if any(keyword in text for keyword in keyword_lower):
                results.append(entry)
        
        return results[:top_k]
    
    def vector_search(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Perform vector similarity search."""
        return self.vector_store.search(query, top_k)
    
    def get_conversation_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get conversation history."""
        if limit:
            return self.conversation_history[-limit:]
        return self.conversation_history.copy()
    
    def get_agent_state(self, agent_name: str, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Get agent state."""
        if agent_name not in self.agent_state:
            return {}
        
        if task_id:
            return self.agent_state[agent_name].get(task_id, {})
        
        return self.agent_state[agent_name].copy()
    
    def retrieve_relevant_context(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant context using hybrid search (keyword + vector)."""
        # Vector search
        vector_results = self.vector_search(query, top_k=top_k * 2)
        
        # Keyword search
        keywords = query.lower().split()
        keyword_results = self.search_by_keywords(keywords, top_k=top_k * 2)
        
        # Combine and deduplicate
        seen_ids = set()
        combined_results = []
        
        # Prioritize vector results (higher semantic similarity)
        for entry, score in vector_results:
            entry_id = entry.get("conversation_id") or entry.get("knowledge_id")
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
        
        return combined_results[:top_k]

