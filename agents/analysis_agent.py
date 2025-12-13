"""Analysis Agent - Performs comparisons, reasoning, and calculations."""

from typing import Dict, Any, List, Optional
from utils.logger import setup_logger, log_agent_call

logger = setup_logger(__name__)

class AnalysisAgent:
    """Agent responsible for analysis, comparison, and reasoning."""
    
    def __init__(self):
        """Initialize Analysis Agent."""
        self.name = "AnalysisAgent"
        logger.info(f"{self.name} initialized")
    
    def analyze(self, query: str, data: Optional[List[Dict[str, Any]]] = None, 
               context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform analysis on given data and query."""
        log_agent_call(logger, self.name, f"Analyzing: {query}", {"data_items": len(data) if data else 0})
        
        query_lower = query.lower()
        
        # Determine analysis type
        if any(keyword in query_lower for keyword in ["compare", "comparison", "versus", "vs", "difference"]):
            return self._compare_items(query, data or [])
        elif any(keyword in query_lower for keyword in ["effective", "efficiency", "best", "better", "recommend"]):
            return self._evaluate_effectiveness(query, data or [])
        elif any(keyword in query_lower for keyword in ["trade-off", "tradeoff", "pros", "cons", "advantage"]):
            return self._analyze_tradeoffs(query, data or [])
        elif any(keyword in query_lower for keyword in ["challenge", "problem", "difficulty", "issue"]):
            return self._identify_challenges(query, data or [])
        else:
            return self._general_analysis(query, data or [])
    
    def _compare_items(self, query: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare multiple items from research data."""
        if not data:
            return {
                "agent": self.name,
                "query": query,
                "result": "No data available for comparison.",
                "confidence": 0.3
            }
        
        comparison_results = []
        
        # Extract comparison dimensions
        items_to_compare = []
        for item in data[:5]:  # Limit to top 5
            title = item.get("title", "Unknown")
            items_to_compare.append({
                "name": title,
                "data": item
            })
        
        if len(items_to_compare) < 2:
            return {
                "agent": self.name,
                "query": query,
                "result": f"Found only {len(items_to_compare)} item(s) for comparison. Need at least 2 items.",
                "confidence": 0.5
            }
        
        # Perform comparison
        comparison_text = f"Comparison of {len(items_to_compare)} items:\n\n"
        
        for i, item1 in enumerate(items_to_compare):
            for item2 in items_to_compare[i+1:]:
                comparison_text += f"{item1['name']} vs {item2['name']}:\n"
                
                # Compare based on available fields
                if "pros" in item1.get("data", {}) and "pros" in item2.get("data", {}):
                    comparison_text += f"  Advantages:\n"
                    comparison_text += f"    {item1['name']}: {', '.join(item1['data'].get('pros', []))}\n"
                    comparison_text += f"    {item2['name']}: {', '.join(item2['data'].get('pros', []))}\n"
                
                if "cons" in item1.get("data", {}) and "cons" in item2.get("data", {}):
                    comparison_text += f"  Limitations:\n"
                    comparison_text += f"    {item1['name']}: {', '.join(item1['data'].get('cons', []))}\n"
                    comparison_text += f"    {item2['name']}: {', '.join(item2['data'].get('cons', []))}\n"
                
                comparison_text += "\n"
        
        confidence = min(0.9, 0.6 + (len(items_to_compare) * 0.1))
        
        return {
            "agent": self.name,
            "query": query,
            "result": comparison_text,
            "confidence": confidence,
            "comparison_items": [item["name"] for item in items_to_compare]
        }
    
    def _evaluate_effectiveness(self, query: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate effectiveness of items."""
        if not data:
            return {
                "agent": self.name,
                "query": query,
                "result": "No data available for evaluation.",
                "confidence": 0.3
            }
        
        evaluations = []
        
        for item in data[:5]:
            title = item.get("title", "Unknown")
            pros = item.get("pros", [])
            cons = item.get("cons", [])
            confidence_score = item.get("confidence", 0.5)
            
            # Calculate effectiveness score (simple heuristic)
            effectiveness = len(pros) / (len(pros) + len(cons) + 1) * confidence_score
            
            evaluations.append({
                "item": title,
                "effectiveness_score": effectiveness,
                "pros_count": len(pros),
                "cons_count": len(cons),
                "data": item
            })
        
        # Sort by effectiveness
        evaluations.sort(key=lambda x: x["effectiveness_score"], reverse=True)
        
        result_text = "Effectiveness Evaluation:\n\n"
        
        for i, eval_item in enumerate(evaluations, 1):
            result_text += f"{i}. {eval_item['item']}\n"
            result_text += f"   Effectiveness Score: {eval_item['effectiveness_score']:.2f}\n"
            result_text += f"   Advantages: {eval_item['pros_count']}, Limitations: {eval_item['cons_count']}\n\n"
        
        # Recommendation
        if evaluations:
            best = evaluations[0]
            result_text += f"Recommendation: {best['item']} appears most effective "
            result_text += f"with a score of {best['effectiveness_score']:.2f}.\n"
        
        confidence = min(0.85, 0.5 + (len(evaluations) * 0.05))
        
        return {
            "agent": self.name,
            "query": query,
            "result": result_text,
            "confidence": confidence,
            "evaluations": evaluations
        }
    
    def _analyze_tradeoffs(self, query: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze trade-offs."""
        if not data:
            return {
                "agent": self.name,
                "query": query,
                "result": "No data available for trade-off analysis.",
                "confidence": 0.3
            }
        
        result_text = "Trade-off Analysis:\n\n"
        
        for item in data[:5]:
            title = item.get("title", "Unknown")
            pros = item.get("pros", [])
            cons = item.get("cons", [])
            tradeoffs = item.get("trade_offs", "")
            
            result_text += f"{title}:\n"
            
            if pros:
                result_text += f"  Advantages: {', '.join(pros)}\n"
            if cons:
                result_text += f"  Disadvantages: {', '.join(cons)}\n"
            if tradeoffs:
                result_text += f"  Key Trade-offs: {tradeoffs}\n"
            
            result_text += "\n"
        
        return {
            "agent": self.name,
            "query": query,
            "result": result_text,
            "confidence": 0.8
        }
    
    def _identify_challenges(self, query: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify challenges and common issues."""
        if not data:
            return {
                "agent": self.name,
                "query": query,
                "result": "No data available for challenge identification.",
                "confidence": 0.3
            }
        
        all_challenges = []
        challenges_by_item = {}
        
        for item in data:
            title = item.get("title", "Unknown")
            challenges = item.get("challenges", "")
            
            if challenges:
                challenge_list = challenges.split(",") if isinstance(challenges, str) else challenges
                all_challenges.extend(challenge_list)
                challenges_by_item[title] = challenge_list
        
        # Find common challenges
        challenge_frequency = {}
        for challenge in all_challenges:
            challenge_clean = challenge.strip().lower()
            challenge_frequency[challenge_clean] = challenge_frequency.get(challenge_clean, 0) + 1
        
        common_challenges = sorted(challenge_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
        
        result_text = "Challenge Analysis:\n\n"
        result_text += "Common Challenges Identified:\n"
        
        for challenge, frequency in common_challenges:
            result_text += f"  - {challenge.title()} (mentioned {frequency} times)\n"
        
        result_text += "\nChallenges by Item:\n"
        for item, challenges in list(challenges_by_item.items())[:5]:
            result_text += f"\n{item}:\n"
            for challenge in challenges:
                result_text += f"  - {challenge.strip()}\n"
        
        return {
            "agent": self.name,
            "query": query,
            "result": result_text,
            "confidence": 0.75,
            "common_challenges": common_challenges
        }
    
    def _general_analysis(self, query: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform general analysis."""
        if not data:
            return {
                "agent": self.name,
                "query": query,
                "result": "No data available for analysis.",
                "confidence": 0.3
            }
        
        query_lower = query.lower()
        
        # Check if this is a privacy/implications query
        if any(keyword in query_lower for keyword in ["privacy", "implications", "protect", "protection", "security"]):
            return self._analyze_privacy_implications(query, data)
        
        result_text = "Analysis Results:\n\n"
        
        for i, item in enumerate(data[:5], 1):
            title = item.get("title", "Unknown")
            content = item.get("content", "")
            
            result_text += f"{i}. {title}\n"
            if content:
                result_text += f"   {content}\n"
            
            # Include additional analysis dimensions if available
            if "methodology" in item:
                result_text += f"   Methodology: {item['methodology']}\n"
            if "computational_efficiency" in item:
                result_text += f"   Computational Efficiency: {item['computational_efficiency']}\n"
            
            result_text += "\n"
        
        return {
            "agent": self.name,
            "query": query,
            "result": result_text,
            "confidence": 0.7
        }
    
    def _analyze_privacy_implications(self, query: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze privacy implications and protection strategies."""
        if not data:
            return {
                "agent": self.name,
                "query": query,
                "result": "No privacy data available for analysis.",
                "confidence": 0.3
            }
        
        result_text = "Privacy Implications and Data Protection Analysis:\n\n"
        
        # Separate implications from protection strategies
        implications_items = []
        protection_items = []
        
        for item in data:
            title = item.get("title", "").lower()
            content = item.get("content", "")
            
            if "privacy implication" in title or "implication" in title.lower():
                implications_items.append(item)
            elif "protection" in title or "strategy" in title or "technique" in title or "compliance" in title:
                protection_items.append(item)
            else:
                # Check content for keywords
                if "implication" in content.lower() or "concern" in content.lower() or "risk" in content.lower():
                    implications_items.append(item)
                elif "protect" in content.lower() or "strategy" in content.lower() or "technique" in content.lower():
                    protection_items.append(item)
        
        # Analyze Privacy Implications
        if implications_items:
            result_text += "**Privacy Implications of AI:**\n\n"
            for item in implications_items[:3]:
                title = item.get("title", "Unknown")
                content = item.get("content", "")
                implications = item.get("implications", [])
                
                result_text += f"• {title}\n"
                if implications:
                    result_text += "  Key Concerns:\n"
                    for impl in implications:
                        result_text += f"    - {impl}\n"
                elif content:
                    # Extract numbered points from content
                    lines = content.split('.')
                    for line in lines[:5]:
                        line = line.strip()
                        if line and len(line) > 20:
                            result_text += f"    - {line}.\n"
                result_text += "\n"
        
        # Analyze Data Protection Strategies
        if protection_items:
            result_text += "**How to Protect Data in AI Systems:**\n\n"
            for item in protection_items[:3]:
                title = item.get("title", "Unknown")
                content = item.get("content", "")
                strategies = item.get("strategies", item.get("techniques", []))
                
                result_text += f"• {title}\n"
                if strategies:
                    result_text += "  Protection Methods:\n"
                    for strategy in strategies:
                        result_text += f"    - {strategy}\n"
                elif content:
                    # Extract numbered points from content
                    lines = content.split('.')
                    for line in lines[:8]:
                        line = line.strip()
                        if line and len(line) > 20:
                            result_text += f"    - {line}.\n"
                result_text += "\n"
        
        # If no specific items found, use general analysis
        if not implications_items and not protection_items:
            result_text += "**Privacy and Data Protection Overview:**\n\n"
            for item in data[:3]:
                title = item.get("title", "Unknown")
                content = item.get("content", "")
                result_text += f"• {title}\n   {content[:200]}...\n\n"
        
        confidence = min(0.85, 0.6 + (len(implications_items) + len(protection_items)) * 0.05)
        
        return {
            "agent": self.name,
            "query": query,
            "result": result_text,
            "confidence": confidence
        }

