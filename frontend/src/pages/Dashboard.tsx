import { useQuery } from '@tanstack/react-query'
import { goalsAPI } from '../lib/api'
import { Target, TrendingUp, CheckCircle, AlertCircle } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Dashboard() {
  const { data: goalsResponse, isLoading: goalsLoading } = useQuery({
    queryKey: ['goals'],
    queryFn: () => goalsAPI.list().then(res => res.data),
  })

  const { data: stats } = useQuery({
    queryKey: ['goal-stats'],
    queryFn: () => goalsAPI.getStatistics().then(res => res.data),
  })

  // Handle both paginated and non-paginated responses
  const goals = Array.isArray(goalsResponse) ? goalsResponse : (goalsResponse?.results || [])
  const activeGoals = goals.filter((g: any) => g.status === 'active')
  const needsAttention = activeGoals.filter((g: any) => !g.is_on_track)

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Track your progress and get AI-powered insights</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Goals</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {stats?.total_goals || 0}
              </p>
            </div>
            <Target className="w-12 h-12 text-primary-600" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Active Goals</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {stats?.active_goals || 0}
              </p>
            </div>
            <TrendingUp className="w-12 h-12 text-blue-600" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Completed</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {stats?.completed_goals || 0}
              </p>
            </div>
            <CheckCircle className="w-12 h-12 text-green-600" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Needs Attention</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {needsAttention.length}
              </p>
            </div>
            <AlertCircle className="w-12 h-12 text-orange-600" />
          </div>
        </div>
      </div>

      {/* Active Goals */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900">Active Goals</h2>
          <Link to="/goals" className="text-primary-600 hover:text-primary-700 font-medium">
            View All
          </Link>
        </div>

        {goalsLoading ? (
          <p className="text-gray-600">Loading goals...</p>
        ) : activeGoals.length === 0 ? (
          <div className="text-center py-12">
            <Target className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 mb-4">No active goals yet</p>
            <Link to="/goals" className="btn btn-primary">
              Create Your First Goal
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {activeGoals.slice(0, 5).map((goal: any) => (
              <Link
                key={goal.id}
                to={`/goals/${goal.id}`}
                className="block p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900">{goal.title}</h3>
                    <p className="text-sm text-gray-600 mt-1">{goal.description}</p>
                    <div className="flex items-center space-x-4 mt-3">
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        goal.priority === 'high' || goal.priority === 'critical'
                          ? 'bg-red-100 text-red-700'
                          : goal.priority === 'medium'
                          ? 'bg-yellow-100 text-yellow-700'
                          : 'bg-gray-100 text-gray-700'
                      }`}>
                        {goal.priority}
                      </span>
                      <span className="text-xs text-gray-600">
                        Target: {new Date(goal.target_date).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                  <div className="ml-6 text-right">
                    <p className="text-2xl font-bold text-primary-600">
                      {goal.progress_percentage}%
                    </p>
                    <p className="text-xs text-gray-600 mt-1">Progress</p>
                  </div>
                </div>
                
                {/* Progress bar */}
                <div className="mt-4 bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-primary-600 h-2 rounded-full transition-all"
                    style={{ width: `${goal.progress_percentage}%` }}
                  />
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link to="/goals" className="card hover:shadow-md transition-shadow">
          <Target className="w-8 h-8 text-primary-600 mb-4" />
          <h3 className="font-semibold text-gray-900 mb-2">Create Goal</h3>
          <p className="text-sm text-gray-600">Set a new goal and let AI guide you</p>
        </Link>

        <Link to="/coaching" className="card hover:shadow-md transition-shadow">
          <TrendingUp className="w-8 h-8 text-blue-600 mb-4" />
          <h3 className="font-semibold text-gray-900 mb-2">Start Coaching</h3>
          <p className="text-sm text-gray-600">Chat with your AI coach</p>
        </Link>

        <Link to="/insights" className="card hover:shadow-md transition-shadow">
          <CheckCircle className="w-8 h-8 text-green-600 mb-4" />
          <h3 className="font-semibold text-gray-900 mb-2">View Insights</h3>
          <p className="text-sm text-gray-600">See what AI learned about you</p>
        </Link>
      </div>
    </div>
  )
}
