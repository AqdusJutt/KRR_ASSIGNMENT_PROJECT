"""Research Agent - Simulates information retrieval from knowledge base."""

from typing import Dict, Any, List, Optional
from utils.logger import setup_logger, log_agent_call

logger = setup_logger(__name__)

class ResearchAgent:
    """Agent responsible for information retrieval and research."""
    
    def __init__(self):
        """Initialize Research Agent with knowledge base."""
        self.knowledge_base = self._initialize_knowledge_base()
        self.name = "ResearchAgent"
        logger.info(f"{self.name} initialized with {len(self.knowledge_base)} knowledge entries")
    
    def _initialize_knowledge_base(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize pre-loaded knowledge base (simulates web search)."""
        return {
            "artificial intelligence": [
                {
                    "title": "What is Artificial Intelligence?",
                    "content": "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think, learn, and make decisions like humans. AI systems can perform tasks such as visual perception, speech recognition, decision-making, and language translation.",
                    "confidence": 0.95
                },
                {
                    "title": "Types of AI",
                    "content": "AI can be categorized into Narrow AI (specialized in specific tasks like image recognition), General AI (human-level intelligence across all domains), and Superintelligent AI (surpassing human intelligence). Most current AI systems are Narrow AI.",
                    "confidence": 0.95
                },
                {
                    "title": "AI Applications",
                    "content": "AI is used in various fields including healthcare (diagnosis and treatment), autonomous vehicles, natural language processing, robotics, recommendation systems, and computer vision.",
                    "confidence": 0.90
                },
                {
                    "title": "Machine Learning as AI",
                    "content": "Machine learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed. It includes supervised learning, unsupervised learning, and reinforcement learning.",
                    "confidence": 0.95
                },
                {
                    "title": "Deep Learning",
                    "content": "Deep learning is a subset of machine learning that uses neural networks with multiple layers to learn representations of data. It has revolutionized fields like image recognition, natural language processing, and speech recognition.",
                    "confidence": 0.95
                }
            ],
            "ai agents": [
                {
                    "title": "Research Agent",
                    "content": "A Research Agent retrieves and gathers information from knowledge bases, databases, or web sources. It specializes in finding relevant data and documents based on queries.",
                    "confidence": 0.95,
                    "examples": ["Information retrieval systems", "Document search agents", "Knowledge base query agents"]
                },
                {
                    "title": "Analysis Agent",
                    "content": "An Analysis Agent performs data analysis, comparisons, and reasoning tasks. It can evaluate options, identify patterns, and make recommendations based on data.",
                    "confidence": 0.95,
                    "examples": ["Data analysis agents", "Comparison agents", "Decision support systems"]
                },
                {
                    "title": "Memory Agent",
                    "content": "A Memory Agent manages long-term storage and retrieval of information. It maintains conversation history, knowledge bases, and can search through stored data using various methods.",
                    "confidence": 0.95,
                    "examples": ["Conversation memory systems", "Vector database agents", "Knowledge management agents"]
                },
                {
                    "title": "Coordinator Agent",
                    "content": "A Coordinator Agent (also called Manager Agent) orchestrates multiple specialized agents. It decomposes tasks, routes subtasks to appropriate agents, and synthesizes results.",
                    "confidence": 0.95,
                    "examples": ["Multi-agent system coordinators", "Task orchestrators", "Workflow management agents"]
                },
                {
                    "title": "Chatbot Agent",
                    "content": "A Chatbot Agent engages in natural language conversations with users. It understands user intent, maintains context, and provides helpful responses.",
                    "confidence": 0.90,
                    "examples": ["Customer service chatbots", "Virtual assistants", "Conversational AI agents"]
                },
                {
                    "title": "Recommendation Agent",
                    "content": "A Recommendation Agent suggests products, content, or actions based on user preferences and behavior. It uses collaborative filtering and content-based filtering techniques.",
                    "confidence": 0.90,
                    "examples": ["Product recommendation systems", "Content recommendation engines", "Personalized suggestion agents"]
                },
                {
                    "title": "Planning Agent",
                    "content": "A Planning Agent creates action plans to achieve goals. It can break down complex tasks into sequences of actions and adjust plans based on changing conditions.",
                    "confidence": 0.90,
                    "examples": ["Task planning systems", "Strategic planning agents", "Automated workflow planners"]
                },
                {
                    "title": "Monitoring Agent",
                    "content": "A Monitoring Agent continuously observes systems, processes, or environments. It detects anomalies, tracks performance metrics, and alerts when issues are found.",
                    "confidence": 0.90,
                    "examples": ["System monitoring agents", "Anomaly detection agents", "Performance monitoring systems"]
                }
            ],
            "neural networks": [
                {
                    "title": "Feedforward Neural Networks",
                    "content": "Feedforward neural networks are the simplest type, where information flows in one direction from input to output layers.",
                    "confidence": 0.95
                },
                {
                    "title": "Convolutional Neural Networks (CNNs)",
                    "content": "CNNs are specialized for processing grid-like data such as images, using convolutional layers to detect spatial patterns.",
                    "confidence": 0.95
                },
                {
                    "title": "Recurrent Neural Networks (RNNs)",
                    "content": "RNNs process sequential data by maintaining hidden states, making them suitable for time series and natural language processing.",
                    "confidence": 0.95
                },
                {
                    "title": "Long Short-Term Memory (LSTM)",
                    "content": "LSTMs are a type of RNN designed to remember long-term dependencies, solving the vanishing gradient problem.",
                    "confidence": 0.95
                },
                {
                    "title": "Transformer Networks",
                    "content": "Transformer networks use attention mechanisms to process sequences in parallel, revolutionizing NLP and becoming the foundation for models like BERT and GPT.",
                    "confidence": 0.95
                },
                {
                    "title": "Graph Neural Networks (GNNs)",
                    "content": "GNNs operate on graph-structured data, enabling learning from relationships and connections between entities.",
                    "confidence": 0.90
                }
            ],
            "optimization techniques": [
                {
                    "title": "Gradient Descent",
                    "content": "Gradient descent is a first-order optimization algorithm that finds local minima by following the negative gradient of the loss function.",
                    "confidence": 0.95,
                    "pros": ["Simple to implement", "Works well for convex functions"],
                    "cons": ["Can get stuck in local minima", "Sensitive to learning rate"]
                },
                {
                    "title": "Adam Optimizer",
                    "content": "Adam combines adaptive learning rates with momentum, adjusting learning rates for each parameter individually. Adam maintains per-parameter learning rates by computing running averages of both the gradients and their squared values (first and second moment estimates).",
                    "confidence": 0.95,
                    "pros": ["Fast convergence", "Adaptive learning rates", "Works well with sparse gradients"],
                    "cons": ["Requires tuning hyperparameters", "Can be memory intensive"],
                    "memory_usage": "Adam requires approximately 3x more memory than SGD because it stores: 1) First moment estimates (m) - running average of gradients for each parameter, 2) Second moment estimates (v) - running average of squared gradients for each parameter, 3) Model parameters (same as SGD). For a model with N parameters, Adam stores N (parameters) + N (first moments) + N (second moments) = 3N values, while SGD only stores N (parameters) + N (gradients during backprop) = 2N values temporarily.",
                    "memory_details": "Adam stores per-parameter state: momentum estimates (m_t) and squared gradient estimates (v_t), each requiring the same memory as model parameters. This doubles the memory footprint compared to SGD, which only needs to store gradients temporarily during backpropagation."
                },
                {
                    "title": "RMSprop",
                    "content": "RMSprop adapts learning rates by maintaining a moving average of squared gradients.",
                    "confidence": 0.90,
                    "pros": ["Adaptive learning rate", "Good for non-stationary objectives"],
                    "cons": ["Still requires manual tuning", "May converge to suboptimal solutions"]
                },
                {
                    "title": "Stochastic Gradient Descent (SGD)",
                    "content": "SGD uses random batches of data instead of the entire dataset, making it more efficient for large datasets. SGD only stores model parameters and computes gradients on-the-fly during backpropagation without maintaining additional per-parameter state.",
                    "confidence": 0.95,
                    "pros": ["Efficient for large datasets", "Can escape local minima", "Simple", "Lower memory usage"],
                    "cons": ["Noisy gradients", "Requires learning rate scheduling"],
                    "memory_usage": "SGD has lower memory requirements than Adam. It only stores: 1) Model parameters (weights and biases), 2) Gradients (temporarily during backpropagation, then discarded). SGD does not maintain persistent per-parameter state between iterations, making it more memory-efficient for large models.",
                    "memory_details": "SGD memory footprint: N (parameters) + N (gradients during backprop, then freed). No persistent state is maintained, so memory usage is approximately 2N during training and N during inference, compared to Adam's 3N persistent storage."
                }
            ],
            "transformer architectures": [
                {
                    "title": "Transformer Architecture",
                    "content": "The original transformer uses encoder-decoder architecture with self-attention mechanisms, enabling parallel processing of sequences.",
                    "confidence": 0.95,
                    "computational_efficiency": "Medium - requires quadratic memory for attention",
                    "trade_offs": "High accuracy but computationally expensive for long sequences"
                },
                {
                    "title": "BERT (Bidirectional Encoder Representations)",
                    "content": "BERT uses only the encoder part of transformers, pre-trained on masked language modeling and next sentence prediction.",
                    "confidence": 0.95,
                    "computational_efficiency": "Medium-High - bidirectional attention increases computation",
                    "trade_offs": "Excellent for understanding but requires fine-tuning for tasks"
                },
                {
                    "title": "GPT (Generative Pre-trained Transformer)",
                    "content": "GPT uses decoder-only architecture with autoregressive generation, trained on next-token prediction.",
                    "confidence": 0.95,
                    "computational_efficiency": "Medium - sequential generation limits parallelization",
                    "trade_offs": "Great for generation but requires careful prompt engineering"
                },
                {
                    "title": "Vision Transformers (ViT)",
                    "content": "ViTs apply transformer architecture to images by splitting them into patches and treating them as sequences.",
                    "confidence": 0.90,
                    "computational_efficiency": "Low-Medium - quadratic complexity with image size",
                    "trade_offs": "Excellent accuracy but needs large datasets for training"
                }
            ],
            "reinforcement learning": [
                {
                    "title": "Q-Learning",
                    "content": "Q-Learning is a model-free reinforcement learning algorithm that learns action-value functions through temporal difference learning.",
                    "confidence": 0.95,
                    "methodology": "Value-based, off-policy learning",
                    "challenges": "Requires discretization of state/action spaces, can be slow to converge"
                },
                {
                    "title": "Policy Gradient Methods",
                    "content": "Policy gradient methods directly optimize the policy by following gradients of expected rewards.",
                    "confidence": 0.95,
                    "methodology": "Policy-based, on-policy learning",
                    "challenges": "High variance in gradients, requires careful hyperparameter tuning"
                },
                {
                    "title": "Actor-Critic Methods",
                    "content": "Actor-Critic combines policy gradient (actor) with value function estimation (critic) to reduce variance.",
                    "confidence": 0.95,
                    "methodology": "Hybrid approach combining policy and value methods",
                    "challenges": "Complex to tune, requires two networks, can be unstable"
                },
                {
                    "title": "Deep Q-Networks (DQN)",
                    "content": "DQN combines Q-learning with deep neural networks to handle high-dimensional state spaces.",
                    "confidence": 0.95,
                    "methodology": "Deep value-based learning with experience replay",
                    "challenges": "Sample inefficient, requires careful hyperparameter tuning, instability issues"
                },
                {
                    "title": "Proximal Policy Optimization (PPO)",
                    "content": "PPO is an on-policy algorithm that constrains policy updates to prevent large changes.",
                    "confidence": 0.95,
                    "methodology": "Trust region policy optimization with clipping",
                    "challenges": "Can be sample inefficient, sensitive to hyperparameters"
                }
            ],
            "privacy and data protection": [
                {
                    "title": "AI Privacy Implications",
                    "content": "AI systems raise significant privacy concerns including: 1) Data collection and surveillance - AI requires vast amounts of data, often personal information, 2) Data breaches - centralized data storage creates security vulnerabilities, 3) Profiling and discrimination - AI can create detailed user profiles and perpetuate biases, 4) Lack of transparency - complex AI models make it hard to understand what data is used and how, 5) Re-identification risks - anonymized data can be re-identified using AI techniques, 6) Inference attacks - AI can infer sensitive information from non-sensitive data.",
                    "confidence": 0.95,
                    "implications": ["Data collection", "Surveillance", "Profiling", "Discrimination", "Lack of transparency", "Re-identification"]
                },
                {
                    "title": "Data Protection Strategies",
                    "content": "To protect data in AI systems: 1) Data minimization - collect only necessary data, 2) Encryption - encrypt data at rest and in transit, 3) Differential privacy - add noise to datasets to protect individual records, 4) Federated learning - train models on decentralized data without sharing raw data, 5) Homomorphic encryption - perform computations on encrypted data, 6) Access controls - implement strict authentication and authorization, 7) Regular audits - monitor data access and usage, 8) User consent - obtain explicit consent for data collection, 9) Anonymization - remove or mask identifying information, 10) Compliance - follow GDPR, CCPA, and other privacy regulations.",
                    "confidence": 0.95,
                    "strategies": ["Data minimization", "Encryption", "Differential privacy", "Federated learning", "Access controls", "User consent", "Anonymization", "Compliance"]
                },
                {
                    "title": "Privacy-Preserving AI Techniques",
                    "content": "Privacy-preserving AI techniques include: 1) Differential Privacy - adds mathematical noise to prevent identification of individuals, 2) Federated Learning - trains models across distributed devices without centralizing data, 3) Secure Multi-Party Computation - allows computation on data from multiple parties without revealing inputs, 4) Homomorphic Encryption - enables computation on encrypted data, 5) Synthetic Data - generates artificial data that preserves statistical properties without exposing real individuals, 6) Privacy-preserving Machine Learning - techniques that protect data during model training and inference.",
                    "confidence": 0.90,
                    "techniques": ["Differential Privacy", "Federated Learning", "Secure Multi-Party Computation", "Homomorphic Encryption", "Synthetic Data"]
                },
                {
                    "title": "Regulatory Compliance",
                    "content": "Key privacy regulations for AI systems: 1) GDPR (EU) - requires consent, data minimization, right to explanation, and privacy by design, 2) CCPA (California) - gives consumers rights to know, delete, and opt-out of data sales, 3) HIPAA (US healthcare) - protects health information, 4) PIPEDA (Canada) - governs data collection and use, 5) AI Act (EU) - specifically regulates high-risk AI systems with privacy requirements. Compliance requires data protection impact assessments, privacy policies, breach notification, and user rights implementation.",
                    "confidence": 0.95,
                    "regulations": ["GDPR", "CCPA", "HIPAA", "PIPEDA", "AI Act"]
                },
                {
                    "title": "AI Ethics and Privacy",
                    "content": "AI ethics regarding privacy involves: 1) Fairness - ensuring AI doesn't discriminate based on protected characteristics, 2) Accountability - holding organizations responsible for AI decisions, 3) Transparency - explaining how AI uses data and makes decisions, 4) Human agency - giving users control over their data, 5) Privacy and security - protecting personal information, 6) Social benefit - ensuring AI benefits society while respecting privacy. Organizations should implement ethical AI frameworks that prioritize privacy as a fundamental right.",
                    "confidence": 0.90,
                    "ethical_principles": ["Fairness", "Accountability", "Transparency", "Human agency", "Privacy and security", "Social benefit"]
                }
            ],
            "machine learning approaches": [
                {
                    "title": "Supervised Learning",
                    "content": "Supervised learning uses labeled data to train models that can make predictions on new data.",
                    "confidence": 0.95,
                    "use_cases": ["Classification", "Regression", "Image recognition"],
                    "pros": ["High accuracy with enough data", "Interpretable results"],
                    "cons": ["Requires labeled data", "Can overfit"]
                },
                {
                    "title": "Unsupervised Learning",
                    "content": "Unsupervised learning finds patterns in unlabeled data without explicit guidance.",
                    "confidence": 0.95,
                    "use_cases": ["Clustering", "Dimensionality reduction", "Anomaly detection"],
                    "pros": ["No labels needed", "Can discover hidden patterns"],
                    "cons": ["Harder to evaluate", "Less precise"]
                },
                {
                    "title": "Reinforcement Learning",
                    "content": "Reinforcement learning learns through interaction with an environment, receiving rewards or penalties.",
                    "confidence": 0.95,
                    "use_cases": ["Game playing", "Robotics", "Recommendation systems"],
                    "pros": ["Learns optimal strategies", "Adapts to dynamic environments"],
                    "cons": ["Slow to train", "Requires careful reward design"]
                }
            ]
        }
    
    def research(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform research on a given query."""
        log_agent_call(logger, self.name, f"Researching: {query}")
        
        query_lower = query.lower()
        results = []
        matched_topics = []
        
        # Handle conversational queries
        conversational_keywords = ["hello", "hi", "hey", "greetings", "how are you", "thanks", "thank you"]
        if any(keyword in query_lower for keyword in conversational_keywords):
            return {
                "agent": self.name,
                "query": query,
                "results": [],
                "matched_topics": [],
                "confidence": 0.5,
                "result": "I can help you with research on AI, machine learning, neural networks, and related topics. What would you like to know?"
            }
        
        # Handle "ai" or "what is ai" queries specifically
        ai_keywords = ["ai", "artificial intelligence", "what is ai", "define ai"]
        is_ai_query = any(keyword in query_lower for keyword in ai_keywords) or query_lower.strip() in ["ai", "what is ai?"]
        
        # Handle "ai agents" queries
        agent_keywords = ["agent", "agents", "ai agents", "examples of agents", "types of agents"]
        is_agent_query = any(keyword in query_lower for keyword in agent_keywords)
        
        # Handle privacy and data protection queries
        privacy_keywords = ["privacy", "data protection", "data privacy", "protect data", "privacy implications", 
                           "data security", "personal information", "gdpr", "ccpa", "anonymization", "encryption"]
        is_privacy_query = any(keyword in query_lower for keyword in privacy_keywords)
        
        # Handle optimizer queries
        optimizer_keywords = ["optimizer", "optimization", "adam", "sgd", "gradient descent", "rmsprop"]
        is_optimizer_query = any(keyword in query_lower for keyword in optimizer_keywords)
        
        # PRIORITY: Handle optimizer queries FIRST before other matching
        if is_optimizer_query and "optimization techniques" in self.knowledge_base:
            if "optimization techniques" not in matched_topics:
                matched_topics.append("optimization techniques")
            # Add optimization technique entries, filtering for Adam/SGD if mentioned
            entries_added = 0
            for entry in self.knowledge_base["optimization techniques"]:
                entry_text = (entry.get("title", "") + " " + entry.get("content", "")).lower()
                # If query specifically mentions Adam or SGD, prioritize those entries
                if "adam" in query_lower or "sgd" in query_lower:
                    if "adam" in entry_text or "sgd" in entry_text or "stochastic" in entry_text:
                        results.append({
                            "topic": "optimization techniques",
                            **entry,
                            "match_score": 1.0  # High priority for optimizer queries
                        })
                        entries_added += 1
                else:
                    # General optimizer query - include all
                    results.append({
                        "topic": "optimization techniques",
                        **entry,
                        "match_score": 0.9
                    })
                    entries_added += 1
            log_agent_call(logger, self.name, f"Priority handler added {entries_added} optimizer entries")
        
        # First, check for exact topic matches (highest priority)
        for topic, entries in self.knowledge_base.items():
            topic_lower = topic.lower()
            
            # Exact topic match or topic words in query
            topic_matched = False
            if topic_lower in query_lower or any(keyword in query_lower for keyword in topic_lower.split()):
                topic_matched = True
            elif (is_ai_query and topic_lower == "artificial intelligence"):
                topic_matched = True
            elif (is_agent_query and topic_lower == "ai agents"):
                topic_matched = True
            elif (is_privacy_query and topic_lower == "privacy and data protection"):
                topic_matched = True
            elif (is_optimizer_query and topic_lower == "optimization techniques"):
                topic_matched = True
            
            if topic_matched:
                if topic not in matched_topics:
                    matched_topics.append(topic)
                
                # Determine if this is an exact match (include all entries) or partial (filter)
                is_exact_match = (topic_lower in query_lower or 
                                 (is_ai_query and topic_lower == "artificial intelligence") or
                                 (is_agent_query and topic_lower == "ai agents") or
                                 (is_privacy_query and topic_lower == "privacy and data protection") or
                                 (is_optimizer_query and topic_lower == "optimization techniques"))
                
                if is_exact_match:
                    # For optimizer queries with Adam/SGD, filter to those entries
                    if is_optimizer_query and topic_lower == "optimization techniques" and ("adam" in query_lower or "sgd" in query_lower):
                        for entry in entries:
                            entry_text = (entry.get("title", "") + " " + entry.get("content", "")).lower()
                            if "adam" in entry_text or "sgd" in entry_text or "stochastic" in entry_text:
                                results.append({
                                    "topic": topic,
                                    **entry,
                                    "match_score": 1.0
                                })
                    else:
                        # Include all entries for exact match
                        for entry in entries:
                            results.append({
                                "topic": topic,
                                **entry,
                                "match_score": 1.0  # Exact topic match
                            })
                else:
                    # Partial match - check entry relevance
                    for entry in entries:
                        entry_text = (entry.get("title", "") + " " + entry.get("content", "")).lower()
                        # Count matching keywords
                        matching_keywords = sum(1 for keyword in query_lower.split() if keyword in entry_text and len(keyword) > 2)
                        if matching_keywords > 0:
                            results.append({
                                "topic": topic,
                                **entry,
                                "match_score": matching_keywords / max(len(query_lower.split()), 1)
                            })
        
        # If no matches found, search more broadly
        if not results:
            for topic, entries in self.knowledge_base.items():
                for entry in entries:
                    entry_text = (entry.get("title", "") + " " + entry.get("content", "")).lower()
                    # Check if any query keyword appears in entry
                    query_words = [w for w in query_lower.split() if len(w) > 2]
                    if any(keyword in entry_text for keyword in query_words):
                        results.append({
                            "topic": topic,
                            **entry,
                            "match_score": 0.5  # Broad match
                        })
        
        # Sort results by match score (best matches first)
        # Prioritize privacy-related topics when privacy keywords are present
        if is_privacy_query:
            for result in results:
                topic = result.get("topic", "").lower()
                if "privacy" in topic or "data protection" in topic:
                    result["match_score"] = result.get("match_score", 0) + 1.0  # Boost privacy matches
        
        # Prioritize optimizer-related results when optimizer keywords are present
        if is_optimizer_query:
            for result in results:
                entry_text = (result.get("title", "") + " " + result.get("content", "")).lower()
                if "adam" in entry_text or "sgd" in entry_text or "optimizer" in entry_text:
                    result["match_score"] = result.get("match_score", 0) + 0.5  # Boost optimizer matches
        
        results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        
        # Calculate confidence
        confidence = 0.8 if results else 0.3
        if len(matched_topics) > 1:
            confidence = min(0.95, confidence + 0.1)
        
        log_agent_call(logger, self.name, f"Found {len(results)} results", {"topics": matched_topics})
        
        # Remove internal match_score before returning
        clean_results = []
        for result in results[:10]:
            clean_result = {k: v for k, v in result.items() if k != "match_score"}
            clean_results.append(clean_result)
        
        return {
            "agent": self.name,
            "query": query,
            "results": clean_results,  # Limit to top 10, sorted by relevance
            "matched_topics": matched_topics,
            "confidence": confidence,
            "result": self._format_results(clean_results[:5]) if clean_results else "No relevant information found in knowledge base."
        }
    
    def _format_results(self, results: List[Dict[str, Any]]) -> str:
        """Format research results as readable text."""
        if not results:
            return "No results found."
        
        formatted = []
        for i, result in enumerate(results, 1):
            title = result.get("title", "Untitled")
            content = result.get("content", "")
            topic = result.get("topic", "Unknown")
            examples = result.get("examples", [])
            
            result_text = f"{i}. [{topic}] {title}: {content}"
            
            # Add examples if available
            if examples:
                examples_text = ", ".join(examples)
                result_text += f"\n   Examples: {examples_text}"
            
            formatted.append(result_text)
        
        return "\n".join(formatted)

