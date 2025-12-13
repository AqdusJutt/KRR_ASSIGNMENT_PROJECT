import { useState, useRef, useEffect } from 'react'
import axios from 'axios'

interface AgentResult {
  agent: string
  confidence: number
  result: string
}

interface QueryResponse {
  task_id: string
  user_query: string
  task_plan: {
    complexity: string
    requires_research: boolean
    requires_analysis: boolean
    requires_memory: boolean
    subtasks: string[]
  }
  agent_results: AgentResult[]
  final_answer: string
  memory_context_used: boolean
  overall_confidence: number
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState<QueryResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [history, setHistory] = useState<Array<{ query: string; response: QueryResponse }>>([])
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [history, response])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim() || loading) return

    setLoading(true)
    setError(null)
    const currentQuery = query
    setQuery('')

    try {
      const { data } = await axios.post<QueryResponse>(`${API_BASE_URL}/query`, {
        query: currentQuery,
      })

      setResponse(data)
      setHistory([...history, { query: currentQuery, response: data }])
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to process query. Please check if the backend is running.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const getAgentColor = (agentName: string) => {
    const colors: Record<string, string> = {
      CoordinatorAgent: 'bg-purple-100 text-purple-800 border-purple-300',
      ResearchAgent: 'bg-blue-100 text-blue-800 border-blue-300',
      AnalysisAgent: 'bg-green-100 text-green-800 border-green-300',
      MemoryAgent: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    }
    return colors[agentName] || 'bg-gray-100 text-gray-800 border-gray-300'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Multi-Agent Chat System
          </h1>
          <p className="text-gray-600">
            Knowledge Representation and Reasoning - Group Assignment 03
          </p>
          <div className="mt-4 flex justify-center gap-4 text-sm">
            <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full">
              ✓ Coordinator Agent
            </span>
            <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full">
              ✓ Research Agent
            </span>
            <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full">
              ✓ Analysis Agent
            </span>
            <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full">
              ✓ Memory Agent
            </span>
          </div>
        </div>

        {/* Chat Interface */}
        <div className="bg-white rounded-lg shadow-xl overflow-hidden mb-6">
          {/* Messages Area */}
          <div className="h-96 overflow-y-auto p-6 space-y-4 scrollbar-hide">
            {history.length === 0 && !response && (
              <div className="text-center text-gray-500 py-12">
                <p className="text-lg mb-2">Welcome! 👋</p>
                <p>Ask me anything about machine learning, neural networks, or AI!</p>
                <div className="mt-6 space-y-2 text-sm text-left max-w-md mx-auto">
                  <p className="font-semibold">Example queries:</p>
                  <ul className="list-disc list-inside space-y-1 text-gray-600">
                    <li>What are the main types of neural networks?</li>
                    <li>Compare Adam optimizer vs SGD</li>
                    <li>What did we discuss earlier?</li>
                  </ul>
                </div>
              </div>
            )}

            {history.map((item, idx) => (
              <div key={idx} className="space-y-3">
                {/* User Query */}
                <div className="flex justify-end">
                  <div className="bg-primary-500 text-white rounded-lg px-4 py-2 max-w-2xl">
                    <p className="font-medium">You:</p>
                    <p>{item.query}</p>
                  </div>
                </div>

                {/* System Response */}
                <div className="space-y-2">
                  {/* Task Plan */}
                  <div className="bg-gray-50 rounded-lg p-3 max-w-2xl">
                    <p className="text-xs font-semibold text-gray-600 mb-1">Task Plan:</p>
                    <div className="flex gap-2 flex-wrap">
                      <span className={`text-xs px-2 py-1 rounded ${item.response.task_plan.requires_research ? 'bg-blue-200' : 'bg-gray-200'}`}>
                        Research: {item.response.task_plan.requires_research ? '✓' : '✗'}
                      </span>
                      <span className={`text-xs px-2 py-1 rounded ${item.response.task_plan.requires_analysis ? 'bg-green-200' : 'bg-gray-200'}`}>
                        Analysis: {item.response.task_plan.requires_analysis ? '✓' : '✗'}
                      </span>
                      <span className={`text-xs px-2 py-1 rounded ${item.response.task_plan.requires_memory ? 'bg-yellow-200' : 'bg-gray-200'}`}>
                        Memory: {item.response.task_plan.requires_memory ? '✓' : '✗'}
                      </span>
                      <span className="text-xs px-2 py-1 rounded bg-purple-200">
                        Complexity: {item.response.task_plan.complexity}
                      </span>
                    </div>
                  </div>

                  {/* Agent Results */}
                  {item.response.agent_results.map((agentResult, agentIdx) => (
                    <div key={agentIdx} className={`rounded-lg p-3 max-w-2xl border ${getAgentColor(agentResult.agent)}`}>
                      <div className="flex justify-between items-center mb-1">
                        <p className="font-semibold text-sm">{agentResult.agent}</p>
                        <span className="text-xs">Confidence: {(agentResult.confidence * 100).toFixed(0)}%</span>
                      </div>
                      <p className="text-sm whitespace-pre-wrap">{agentResult.result}</p>
                    </div>
                  ))}

                  {/* Final Answer */}
                  <div className="bg-primary-50 border-l-4 border-primary-500 rounded p-3 max-w-2xl">
                    <p className="font-semibold text-sm mb-1">Final Answer:</p>
                    <p className="text-sm whitespace-pre-wrap">{item.response.final_answer}</p>
                    <div className="mt-2 flex justify-between items-center text-xs text-gray-600">
                      <span>Overall Confidence: {(item.response.overall_confidence * 100).toFixed(0)}%</span>
                      {item.response.memory_context_used && (
                        <span className="bg-yellow-200 px-2 py-1 rounded">Memory Used</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {/* Current Response (if any) */}
            {response && !history.some(h => h.response.task_id === response.task_id) && (
              <div className="space-y-2">
                <div className="bg-primary-50 border-l-4 border-primary-500 rounded p-3 max-w-2xl">
                  <p className="font-semibold text-sm mb-1">Final Answer:</p>
                  <p className="text-sm whitespace-pre-wrap">{response.final_answer}</p>
                </div>
              </div>
            )}

            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-lg px-4 py-2">
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-500"></div>
                    <span className="text-sm text-gray-600">Processing...</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t p-4 bg-gray-50">
            {error && (
              <div className="mb-3 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}
            <form onSubmit={handleSubmit} className="flex gap-2">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask a question..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !query.trim()}
                className="px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? 'Sending...' : 'Send'}
              </button>
            </form>
          </div>
        </div>

        {/* System Info */}
        <div className="bg-white rounded-lg shadow-lg p-4">
          <h2 className="font-semibold mb-2">System Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <p className="font-medium text-gray-700">API Endpoint:</p>
              <p className="text-gray-600">{API_BASE_URL}</p>
            </div>
            <div>
              <p className="font-medium text-gray-700">Status:</p>
              <p className="text-green-600">● Operational</p>
            </div>
            <div>
              <p className="font-medium text-gray-700">Conversations:</p>
              <p className="text-gray-600">{history.length}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

