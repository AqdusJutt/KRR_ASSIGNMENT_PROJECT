"""LLM client for Groq API integration."""

import os
import json
from typing import Optional, Dict, Any, List
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    """Client for interacting with Groq LLM API."""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.model = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
        self.enabled = os.getenv("ENABLE_LLM", "true").lower() == "true" and bool(self.api_key)
        
        if self.enabled and self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize Groq client: {e}")
                self.enabled = False
                self.client = None
        else:
            self.client = None
    
    def is_available(self) -> bool:
        """Check if LLM is available."""
        return self.enabled and self.client is not None
    
    def decompose_task(self, query: str) -> Dict[str, Any]:
        """Decompose a complex query into subtasks."""
        if not self.is_available():
            return self._rule_based_decomposition(query)
        
        prompt = f"""Analyze this user query and decompose it into subtasks. 
Return a JSON object with:
- "requires_research": boolean (needs information retrieval)
- "requires_analysis": boolean (needs comparison/reasoning)
- "requires_memory": boolean (needs memory lookup)
- "complexity": string ("simple", "medium", "complex")
- "subtasks": array of strings describing each subtask

User query: "{query}"

Return only valid JSON:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a task decomposition expert. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            return result
            
        except Exception as e:
            print(f"LLM error in task decomposition: {e}")
            return self._rule_based_decomposition(query)
    
    def classify_query(self, query: str) -> str:
        """Classify query type."""
        if not self.is_available():
            return self._rule_based_classification(query)
        
        prompt = f"""Classify this query into one category:
- "research": needs information retrieval
- "analysis": needs comparison/reasoning
- "memory": needs memory lookup
- "hybrid": needs multiple operations

Query: "{query}"

Return only the category name:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a query classification expert. Return only the category name."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=50
            )
            
            category = response.choices[0].message.content.strip().lower()
            return category if category in ["research", "analysis", "memory", "hybrid"] else "hybrid"
            
        except Exception as e:
            print(f"LLM error in classification: {e}")
            return self._rule_based_classification(query)
    
    def summarize_results(self, results: List[Dict[str, Any]]) -> str:
        """Summarize agent results."""
        if not self.is_available() or not results:
            return self._rule_based_summary(results)
        
        results_text = "\n".join([
            f"Agent: {r.get('agent', 'Unknown')}\nResult: {r.get('result', 'N/A')}\n"
            for r in results
        ])
        
        prompt = f"""Summarize these agent results into a coherent answer:

{results_text}

Provide a clear, concise summary:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a summarization expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"LLM error in summarization: {e}")
            return self._rule_based_summary(results)
    
    def _rule_based_decomposition(self, query: str) -> Dict[str, Any]:
        """Rule-based task decomposition fallback."""
        query_lower = query.lower()
        
        requires_research = any(keyword in query_lower for keyword in 
                               ["find", "search", "research", "what", "tell me about", "information"])
        requires_analysis = any(keyword in query_lower for keyword in 
                               ["compare", "analyze", "evaluate", "which", "better", "effectiveness"])
        requires_memory = any(keyword in query_lower for keyword in 
                             ["remember", "discuss", "earlier", "before", "previous", "learned"])
        
        # Determine complexity
        complexity = "simple"
        if requires_research and requires_analysis:
            complexity = "complex"
        elif requires_research or requires_analysis:
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
            "subtasks": subtasks if subtasks else ["Handle query"]
        }
    
    def _rule_based_classification(self, query: str) -> str:
        """Rule-based query classification fallback."""
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in ["remember", "discuss", "earlier", "before", "previous"]):
            return "memory"
        elif any(keyword in query_lower for keyword in ["find", "search", "research", "what", "tell me"]):
            return "research"
        elif any(keyword in query_lower for keyword in ["compare", "analyze", "evaluate", "which", "better"]):
            return "analysis"
        else:
            return "hybrid"
    
    def _rule_based_summary(self, results: List[Dict[str, Any]]) -> str:
        """Rule-based summary fallback."""
        if not results:
            return "No results to summarize."
        
        summary_parts = []
        for result in results:
            agent = result.get('agent', 'Unknown')
            content = result.get('result', '')
            if content:
                summary_parts.append(f"From {agent}: {content}")
        
        return "\n\n".join(summary_parts) if summary_parts else "No results available."

