import { useQuery } from '@tanstack/react-query'
import { agentsAPI } from '../lib/api'
import { Brain, TrendingUp, CheckCircle } from 'lucide-react'

export default function AgentInsights() {
  const { data: decisionsResponse } = useQuery({
    queryKey: ['agent-decisions'],
    queryFn: () => agentsAPI.getRecentDecisions().then(res => res.data),
  })

  const { data: learningResponse } = useQuery({
    queryKey: ['agent-learning'],
    queryFn: () => agentsAPI.getValidatedLearning().then(res => res.data),
  })

  const { data: stats } = useQuery({
    queryKey: ['agent-stats'],
    queryFn: () => agentsAPI.getStatistics().then(res => res.data),
  })

  // Handle both paginated and non-paginated responses
  const decisions = Array.isArray(decisionsResponse) ? decisionsResponse : (decisionsResponse?.results || [])
  const learning = Array.isArray(learningResponse) ? learningResponse : (learningResponse?.results || [])

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">AI Insights</h1>
        <p className="text-gray-600 mt-2">Transparent AI decision-making and learning</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Decisions</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {stats?.total_decisions || 0}
              </p>
            </div>
            <Brain className="w-12 h-12 text-primary-600" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Avg Confidence</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {Math.round((stats?.average_confidence || 0) * 100)}%
              </p>
            </div>
            <TrendingUp className="w-12 h-12 text-blue-600" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Validated Learnings</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {learning?.length || 0}
              </p>
            </div>
            <CheckCircle className="w-12 h-12 text-green-600" />
          </div>
        </div>
      </div>

      {/* Recent Decisions */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Recent AI Decisions</h2>
        
        {decisions.length === 0 ? (
          <p className="text-gray-600 text-center py-8">No decisions yet</p>
        ) : (
          <div className="space-y-4">
            {decisions.slice(0, 10).map((decision: any) => (
              <div key={decision.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-gray-900">{decision.decision_type}</h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {new Date(decision.created_at).toLocaleString()}
                    </p>
                  </div>
                  <span className="text-sm px-3 py-1 bg-green-100 text-green-700 rounded-full">
                    {Math.round(decision.confidence_score * 100)}% confident
                  </span>
                </div>
                
                <p className="text-gray-700 mb-3">{decision.decision}</p>
                
                <details className="text-sm">
                  <summary className="cursor-pointer text-primary-600 font-medium">
                    View Reasoning
                  </summary>
                  <div className="mt-3 pl-4 border-l-2 border-primary-200">
                    <p className="text-gray-700 mb-2"><strong>Rationale:</strong></p>
                    <p className="text-gray-600">{decision.rationale}</p>
                    
                    {decision.reasoning_steps.length > 0 && (
                      <>
                        <p className="text-gray-700 mt-4 mb-2"><strong>Reasoning Steps:</strong></p>
                        <ol className="list-decimal list-inside space-y-1">
                          {decision.reasoning_steps.map((step: string, idx: number) => (
                            <li key={idx} className="text-gray-600">{step}</li>
                          ))}
                        </ol>
                      </>
                    )}
                  </div>
                </details>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Learning Records */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-6">What AI Learned About You</h2>
        
        {learning.length === 0 ? (
          <p className="text-gray-600 text-center py-8">No validated learnings yet</p>
        ) : (
          <div className="space-y-4">
            {learning.map((record: any) => (
              <div key={record.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-semibold text-gray-900">{record.insight_type}</h3>
                  <span className="text-sm px-3 py-1 bg-blue-100 text-blue-700 rounded-full">
                    {Math.round(record.confidence * 100)}% confidence
                  </span>
                </div>
                <p className="text-gray-700">{record.insight_description}</p>
                <div className="mt-3 flex items-center space-x-4 text-sm text-gray-600">
                  <span>Applied {record.applied_to_decisions} times</span>
                  <span>•</span>
                  <span>{Math.round(record.success_rate * 100)}% success rate</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
