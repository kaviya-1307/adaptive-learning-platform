import React, { useState, useEffect } from 'react';
import {
  BrainCircuit,
  TrendingUp,
  CheckCircle2,
  Target,
  Zap,
  RefreshCw,
  Award,
  BookOpen,
  Clock,
  ArrowRight,
  ShieldCheck,
  AlertCircle,
  Sparkles,
  BarChart3,
  Flame,
  Activity,
  Tag,
  Code2,
  XCircle,
  Map,
  Layers
} from 'lucide-react';
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  Tooltip as RechartsTooltip
} from 'recharts';
import {
  fetchDashboardSummary,
  recalculateKnowledgeState,
  generateRecommendation
} from '../services/api';
import { useAuth } from '../context/AuthContext';
import AdaptiveRoadmap from '../components/AdaptiveRoadmap';

export default function DashboardPage({ onSelectProblem, onNavigate }) {
  const { user, isAuthenticated } = useAuth();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [recalculating, setRecalculating] = useState(false);
  const [refreshingRec, setRefreshingRec] = useState(false);
  const [feedbackMessage, setFeedbackMessage] = useState(null);
  const [activeCurriculumTab, setActiveCurriculumTab] = useState('roadmap'); // 'roadmap' | 'radar' | 'both'

  const loadDashboard = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchDashboardSummary();
      setDashboardData(data);
    } catch (err) {
      console.error('Failed to load dashboard summary:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to load learner dashboard.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      loadDashboard();
    }
  }, [isAuthenticated]);

  const handleRecalculateState = async () => {
    setRecalculating(true);
    setFeedbackMessage(null);
    try {
      const result = await recalculateKnowledgeState();
      setFeedbackMessage({
        type: 'success',
        text: `Knowledge state successfully recalculated across ${result.interactions_replayed} historical interactions!`
      });
      // Refresh dashboard data
      const refreshed = await fetchDashboardSummary();
      setDashboardData(refreshed);
    } catch (err) {
      console.error('Failed to recalculate knowledge state:', err);
      setFeedbackMessage({
        type: 'error',
        text: err.response?.data?.detail || 'Failed to recalculate knowledge state.'
      });
    } finally {
      setRecalculating(false);
    }
  };

  const handleRefreshRecommendation = async () => {
    setRefreshingRec(true);
    try {
      await generateRecommendation();
      const refreshed = await fetchDashboardSummary();
      setDashboardData(refreshed);
      setFeedbackMessage({
        type: 'success',
        text: 'Generated fresh active recommendation based on your latest mastery profile!'
      });
    } catch (err) {
      console.error('Failed to generate recommendation:', err);
    } finally {
      setRefreshingRec(false);
    }
  };

  const getDifficultyBadge = (diff) => {
    switch (diff?.toLowerCase()) {
      case 'easy':
        return <span className="badge badge-green">Easy</span>;
      case 'medium':
        return <span className="badge badge-blue">Medium</span>;
      case 'hard':
        return <span className="badge badge-red">Hard</span>;
      default:
        return <span className="badge badge-blue">{diff}</span>;
    }
  };

  const getMasteryTierBadge = (level) => {
    switch (level?.toLowerCase()) {
      case 'master':
        return <span className="badge badge-purple" style={{ fontWeight: 600 }}>Master</span>;
      case 'proficient':
        return <span className="badge badge-green" style={{ fontWeight: 600 }}>Proficient</span>;
      case 'developing':
        return <span className="badge badge-blue" style={{ fontWeight: 600 }}>Developing</span>;
      default:
        return <span className="badge badge-yellow" style={{ fontWeight: 600 }}>Novice</span>;
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'Accepted':
        return (
          <span className="badge badge-green" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
            <CheckCircle2 size={12} /> Accepted
          </span>
        );
      case 'Wrong Answer':
        return (
          <span className="badge badge-red" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
            <XCircle size={12} /> Wrong Answer
          </span>
        );
      case 'Time Limit Exceeded':
        return (
          <span className="badge badge-yellow" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
            <Clock size={12} /> TLE
          </span>
        );
      default:
        return (
          <span className="badge badge-red" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
            <AlertCircle size={12} /> {status}
          </span>
        );
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '5rem 0', color: 'var(--text-secondary)' }}>
        <RefreshCw size={36} className="spinning" style={{ marginBottom: '1rem', color: 'var(--accent-primary)' }} />
        <h3 style={{ margin: 0, color: '#f4f4f5' }}>Loading Personalized Dashboard...</h3>
        <p style={{ fontSize: '0.875rem', marginTop: '0.5rem', color: 'var(--text-muted)' }}>
          Aggregating Adaptive Knowledge State, Submission History, and Adaptive Recommendations.
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem', maxWidth: '600px', margin: '2rem auto' }}>
        <AlertCircle size={40} color="#ef4444" style={{ margin: '0 auto 1rem' }} />
        <h3 style={{ margin: '0 0 0.5rem', color: '#f4f4f5' }}>Unable to Load Dashboard</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '1.5rem' }}>{error}</p>
        <button type="button" className="btn btn-primary" onClick={loadDashboard}>
          <RefreshCw size={14} /> Retry Loading
        </button>
      </div>
    );
  }

  const {
    user: userInfo,
    learning_state,
    topic_mastery,
    problem_stats,
    active_recommendation,
    recommendation_history,
    recent_submissions
  } = dashboardData || {};

  const totalCatalogCount = (problem_stats?.difficulty_breakdown || []).reduce(
    (sum, d) => sum + (d.total_count || 0),
    0
  ) || 889;

  // Radar chart data preparation
  const radarChartData = (topic_mastery || []).map((t) => ({
    topic: t.topic_name.length > 12 ? t.topic_name.substring(0, 10) + '..' : t.topic_name,
    mastery: t.mastery_percentage,
    confidence: Math.round(t.confidence_score * 100),
    fullTopic: t.topic_name,
  }));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* 1. Header Banner */}
      <div
        className="card"
        style={{
          padding: '1.75rem 2rem',
          background: 'linear-gradient(135deg, #18181b 0%, #1e1e24 50%, #27272a 100%)',
          border: '1px solid rgba(99, 102, 241, 0.25)',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1.25rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <span className="badge badge-purple" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                <BrainCircuit size={13} /> Personalized Learning Analytics
              </span>
              {userInfo?.learning_goal && (
                <span className="badge badge-blue">
                  Goal: {userInfo.learning_goal.replace('_', ' ').toUpperCase()}
                </span>
              )}
              {userInfo?.experience_level && (
                <span className="badge badge-green">
                  Tier: {userInfo.experience_level.toUpperCase()}
                </span>
              )}
              {(userInfo?.diagnostic_completed || user?.diagnostic_completed) && (
                <span
                  className="badge badge-purple"
                  style={{ cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}
                  onClick={() => onNavigate && onNavigate('diagnostic')}
                  title="View Diagnostic Score Breakdown"
                >
                  <CheckCircle2 size={12} color="#10b981" /> Diagnostic: {(userInfo?.diagnostic_score ?? user?.diagnostic_score) ?? 0}/{(userInfo?.diagnostic_total ?? user?.diagnostic_total) ?? 7}
                </span>
              )}
            </div>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800, margin: '0 0 0.4rem', color: '#ffffff', letterSpacing: '-0.02em' }}>
              Welcome back, {userInfo?.name || 'Learner'} 👋
            </h1>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', margin: 0 }}>
              Your real-time concept mastery profile and adaptive problem recommendations across DSA domains.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={handleRecalculateState}
              disabled={recalculating}
              style={{ fontWeight: 600, padding: '0.55rem 1rem' }}
              title="Replays all historical submissions through the Bayesian knowledge state engine"
            >
              <RefreshCw size={14} className={recalculating ? 'spinning' : ''} />
              <span>{recalculating ? 'Recalculating...' : 'Recalculate Knowledge State'}</span>
            </button>
          </div>
        </div>

        {/* Feedback Alert Toast */}
        {feedbackMessage && (
          <div
            style={{
              marginTop: '1rem',
              padding: '0.75rem 1rem',
              borderRadius: '8px',
              fontSize: '0.85rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              background: feedbackMessage.type === 'success' ? 'rgba(34, 197, 94, 0.15)' : 'rgba(239, 68, 68, 0.15)',
              border: `1px solid ${feedbackMessage.type === 'success' ? '#22c55e' : '#ef4444'}`,
              color: feedbackMessage.type === 'success' ? '#86efac' : '#fca5a5'
            }}
          >
            <span>{feedbackMessage.text}</span>
            <button
              type="button"
              onClick={() => setFeedbackMessage(null)}
              style={{ background: 'transparent', border: 'none', color: 'inherit', cursor: 'pointer', fontWeight: 700 }}
            >
              ×
            </button>
          </div>
        )}
      </div>

      {/* 2. Key Metrics Scorecards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
        {/* Overall Mastery Card */}
        <div className="card" style={{ padding: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Overall Mastery
            </span>
            <div style={{ width: 28, height: 28, borderRadius: 6, background: 'rgba(99, 102, 241, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <TrendingUp size={16} color="#818cf8" />
            </div>
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f4f4f5' }}>
            {Math.round((learning_state?.overall_mastery || 0) * 100)}%
          </div>
          <div style={{ width: '100%', height: '6px', background: '#27272a', borderRadius: '3px', marginTop: '0.75rem', overflow: 'hidden' }}>
            <div
              style={{
                width: `${Math.round((learning_state?.overall_mastery || 0) * 100)}%`,
                height: '100%',
                background: 'linear-gradient(90deg, #6366f1, #8b5cf6)',
                borderRadius: '3px',
                transition: 'width 0.5s ease'
              }}
            />
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: '0.5rem 0 0' }}>
            Average across 10 DSA domains
          </p>
        </div>

        {/* Model Confidence Card */}
        <div className="card" style={{ padding: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Model Confidence
            </span>
            <div style={{ width: 28, height: 28, borderRadius: 6, background: 'rgba(56, 189, 248, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <ShieldCheck size={16} color="#38bdf8" />
            </div>
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f4f4f5' }}>
            {Math.round((learning_state?.overall_confidence || 0) * 100)}%
          </div>
          <div style={{ width: '100%', height: '6px', background: '#27272a', borderRadius: '3px', marginTop: '0.75rem', overflow: 'hidden' }}>
            <div
              style={{
                width: `${Math.round((learning_state?.overall_confidence || 0) * 100)}%`,
                height: '100%',
                background: 'linear-gradient(90deg, #0ea5e9, #38bdf8)',
                borderRadius: '3px',
                transition: 'width 0.5s ease'
              }}
            />
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: '0.5rem 0 0' }}>
            Knowledge tracing calibration certainty
          </p>
        </div>

        {/* Problems Solved Card */}
        <div className="card" style={{ padding: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Problems Solved
            </span>
            <div style={{ width: 28, height: 28, borderRadius: 6, background: 'rgba(34, 197, 94, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Award size={16} color="#22c55e" />
            </div>
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f4f4f5' }}>
            {problem_stats?.total_solved || 0}{' '}
            <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: 500 }}>/ {totalCatalogCount}</span>
          </div>
          <div style={{ width: '100%', height: '6px', background: '#27272a', borderRadius: '3px', marginTop: '0.75rem', overflow: 'hidden' }}>
            <div
              style={{
                width: `${Math.min(100, Math.round(((problem_stats?.total_solved || 0) / totalCatalogCount) * 100))}%`,
                height: '100%',
                background: 'linear-gradient(90deg, #10b981, #22c55e)',
                borderRadius: '3px',
                transition: 'width 0.5s ease'
              }}
            />
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: '0.5rem 0 0' }}>
            Unique problems completed
          </p>
        </div>

        {/* Acceptance Rate Card */}
        <div className="card" style={{ padding: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Acceptance Rate
            </span>
            <div style={{ width: 28, height: 28, borderRadius: 6, background: 'rgba(234, 179, 8, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Flame size={16} color="#eab308" />
            </div>
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f4f4f5' }}>
            {problem_stats?.acceptance_rate || 0}%
          </div>
          <div style={{ width: '100%', height: '6px', background: '#27272a', borderRadius: '3px', marginTop: '0.75rem', overflow: 'hidden' }}>
            <div
              style={{
                width: `${problem_stats?.acceptance_rate || 0}%`,
                height: '100%',
                background: 'linear-gradient(90deg, #f59e0b, #eab308)',
                borderRadius: '3px',
                transition: 'width 0.5s ease'
              }}
            />
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: '0.5rem 0 0' }}>
            {problem_stats?.accepted_submissions || 0} accepted of {problem_stats?.total_submissions || 0} total
          </p>
        </div>
      </div>

      {/* 3. Active Recommendation Spotlight (M6) */}
      <div
        className="card"
        style={{
          padding: '1.5rem',
          background: 'linear-gradient(135deg, rgba(37, 99, 235, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%)',
          border: '1px solid rgba(99, 102, 241, 0.35)',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.25)'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span className="badge badge-purple" style={{ fontSize: '0.75rem', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
              <BrainCircuit size={13} /> Your Next Recommended Problem
            </span>
            <span className="badge" style={{ background: '#27272a', color: '#cbd5e1' }}>
              Zone of Proximal Development (ZPD)
            </span>
          </div>
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={handleRefreshRecommendation}
            disabled={refreshingRec}
            style={{ fontSize: '0.75rem' }}
          >
            <RefreshCw size={12} className={refreshingRec ? 'spinning' : ''} />
            <span>{refreshingRec ? 'Regenerating...' : 'Get Another Recommendation'}</span>
          </button>
        </div>

        {active_recommendation ? (
          <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '1.5rem', flexWrap: 'wrap' }}>
            <div style={{ flex: 1, minWidth: '280px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <h2 style={{ fontSize: '1.35rem', fontWeight: 700, margin: 0, color: '#ffffff' }}>
                  {active_recommendation.problem_id}. {active_recommendation.problem_title}
                </h2>
                {getDifficultyBadge(active_recommendation.difficulty)}
                <span className="badge" style={{ background: '#27272a', color: '#a1a1aa' }}>
                  <Tag size={11} style={{ marginRight: 3 }} /> {active_recommendation.topic_name}
                </span>
              </div>

              <p style={{ fontSize: '0.875rem', color: '#cbd5e1', lineHeight: 1.6, margin: '0 0 1rem' }}>
                {active_recommendation.explanation_text}
              </p>

              <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                <span>
                  Estimated Success Chance:{' '}
                  <strong style={{ color: '#38bdf8' }}>
                    {Math.round(active_recommendation.predicted_success_prob * 100)}%
                  </strong>
                </span>
                <span>•</span>
                <span>Target Challenge: Optimal Learning Zone</span>
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center' }}>
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => onSelectProblem(active_recommendation.problem_slug)}
                style={{ padding: '0.75rem 1.5rem', fontWeight: 700, fontSize: '0.95rem' }}
              >
                <Zap size={16} />
                <span>Solve Problem</span>
                <ArrowRight size={16} />
              </button>
            </div>
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '1.5rem 0', color: 'var(--text-muted)' }}>
            <p style={{ margin: '0 0 0.75rem' }}>No active recommendation available yet.</p>
            <button
              type="button"
              className="btn btn-primary btn-sm"
              onClick={handleRefreshRecommendation}
              disabled={refreshingRec}
            >
              <Zap size={14} /> Generate Recommendation
            </button>
          </div>
        )}
      </div>

      {/* 4. Curriculum Progression & Mastery Section */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {/* Curriculum View Selector Tabs */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid #27272a', paddingBottom: '0.75rem', flexWrap: 'wrap', gap: '0.75rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button
              type="button"
              className={`btn btn-sm ${activeCurriculumTab === 'roadmap' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveCurriculumTab('roadmap')}
              style={{ fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '0.4rem', padding: '0.45rem 0.9rem' }}
            >
              <Map size={14} /> Adaptive Roadmap (4 Stages &amp; 37 Concepts)
            </button>
            <button
              type="button"
              className={`btn btn-sm ${activeCurriculumTab === 'radar' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveCurriculumTab('radar')}
              style={{ fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '0.4rem', padding: '0.45rem 0.9rem' }}
            >
              <BarChart3 size={14} /> 10-Topic Mastery Radar
            </button>
            <button
              type="button"
              className={`btn btn-sm ${activeCurriculumTab === 'both' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setActiveCurriculumTab('both')}
              style={{ fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '0.4rem', padding: '0.45rem 0.9rem' }}
            >
              <Layers size={14} /> View Both
            </button>
          </div>

          <span className="badge badge-purple" style={{ fontSize: '0.7rem' }}>
            Phase 2: Adaptive Mastery Engine
          </span>
        </div>

        {/* View Option 1: Adaptive Learning Roadmap */}
        {(activeCurriculumTab === 'roadmap' || activeCurriculumTab === 'both') && (
          <AdaptiveRoadmap onSelectProblem={onSelectProblem} onNavigate={onNavigate} />
        )}

        {/* View Option 2: 10-Topic Radar & Breakdown */}
        {(activeCurriculumTab === 'radar' || activeCurriculumTab === 'both') && (
          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(300px, 1fr) minmax(360px, 1.4fr)', gap: '1.25rem', alignItems: 'start' }}>
            {/* Left Column: Radar Chart */}
            <div className="card" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <BarChart3 size={18} color="#818cf8" />
                  <h2 style={{ fontSize: '1.1rem', fontWeight: 700, margin: 0, color: '#f4f4f5' }}>
                    10-Topic Mastery Radar
                  </h2>
                </div>
                <span className="badge badge-purple" style={{ fontSize: '0.7rem' }}>
                  Adaptive Knowledge State
                </span>
              </div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: '0 0 1rem' }}>
                Multi-dimensional knowledge state representation across all 10 core algorithmic domains.
              </p>

              <div style={{ width: '100%', height: 320, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={radarChartData} margin={{ top: 10, right: 20, bottom: 10, left: 20 }}>
                    <PolarGrid stroke="#3f3f46" strokeDasharray="3 3" />
                    <PolarAngleAxis dataKey="topic" stroke="#a1a1aa" tick={{ fill: '#d4d4d8', fontSize: 11 }} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#52525b" tick={{ fill: '#71717a', fontSize: 9 }} />
                    <Radar
                      name="Topic Mastery (%)"
                      dataKey="mastery"
                      stroke="#818cf8"
                      fill="#6366f1"
                      fillOpacity={0.45}
                    />
                    <RechartsTooltip
                      contentStyle={{ background: '#18181b', borderColor: '#3f3f46', borderRadius: '8px', fontSize: '0.8rem', color: '#f4f4f5' }}
                      formatter={(val, name, props) => [`${val}%`, `${props.payload.fullTopic} Mastery`]}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Right Column: 10-Topic Detailed Grid */}
            <div className="card" style={{ padding: '1.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <BookOpen size={18} color="#38bdf8" />
                  <h2 style={{ fontSize: '1.1rem', fontWeight: 700, margin: 0, color: '#f4f4f5' }}>
                    Topic Mastery Breakdown
                  </h2>
                </div>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  10 DSA Domains
                </span>
              </div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: '0 0 1rem' }}>
                Dynamic proficiencies updated in real time with each code submission.
              </p>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '0.75rem' }}>
                {(topic_mastery || []).map((t) => (
                  <div
                    key={t.topic_id}
                    style={{
                      background: '#18181b',
                      border: '1px solid #27272a',
                      borderRadius: '8px',
                      padding: '0.75rem',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '0.4rem',
                      transition: 'border-color 0.15s ease'
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <span style={{ fontWeight: 600, fontSize: '0.82rem', color: '#f4f4f5' }}>{t.topic_name}</span>
                      {getMasteryTierBadge(t.mastery_level)}
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      <span>Mastery: <strong style={{ color: '#e4e4e7' }}>{t.mastery_percentage}%</strong></span>
                      <span>Conf: {Math.round(t.confidence_score * 100)}%</span>
                    </div>

                    {/* Progress bar */}
                    <div style={{ width: '100%', height: '5px', background: '#27272a', borderRadius: '3px', overflow: 'hidden' }}>
                      <div
                        style={{
                          width: `${t.mastery_percentage}%`,
                          height: '100%',
                          background:
                            t.mastery_percentage >= 75
                              ? 'linear-gradient(90deg, #10b981, #22c55e)'
                              : t.mastery_percentage >= 40
                              ? 'linear-gradient(90deg, #3b82f6, #60a5fa)'
                              : 'linear-gradient(90deg, #f59e0b, #eab308)',
                          borderRadius: '3px',
                          transition: 'width 0.4s ease'
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 5. Problem Solving Difficulty Distribution */}
      <div className="card" style={{ padding: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Activity size={18} color="#22c55e" />
            <h2 style={{ fontSize: '1.1rem', fontWeight: 700, margin: 0, color: '#f4f4f5' }}>
              Difficulty Distribution &amp; Catalog Coverage
            </h2>
          </div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            {totalCatalogCount} Problems Across 10 Topics
          </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
          {(problem_stats?.difficulty_breakdown || []).map((diffItem) => {
            const isEasy = diffItem.difficulty.toLowerCase() === 'easy';
            const isMedium = diffItem.difficulty.toLowerCase() === 'medium';
            const barColor = isEasy ? '#22c55e' : isMedium ? '#3b82f6' : '#ef4444';

            return (
              <div
                key={diffItem.difficulty}
                style={{
                  background: '#18181b',
                  border: '1px solid #27272a',
                  borderRadius: '10px',
                  padding: '1rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.5rem'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                    {getDifficultyBadge(diffItem.difficulty)}
                    <span style={{ fontWeight: 600, fontSize: '0.85rem', color: '#f4f4f5' }}>
                      {diffItem.difficulty} Problems
                    </span>
                  </div>
                  <span style={{ fontWeight: 700, fontSize: '0.9rem', color: '#f4f4f5' }}>
                    {diffItem.solved_count}{' '}
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>/ {diffItem.total_count}</span>
                  </span>
                </div>

                <div style={{ width: '100%', height: '6px', background: '#27272a', borderRadius: '3px', overflow: 'hidden' }}>
                  <div
                    style={{
                      width: `${diffItem.percentage}%`,
                      height: '100%',
                      background: barColor,
                      borderRadius: '3px',
                      transition: 'width 0.4s ease'
                    }}
                  />
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  <span>Completed: {diffItem.percentage}%</span>
                  <span>{diffItem.total_count - diffItem.solved_count} remaining</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 6. Dual Feeds: Recommendation History & Recent Submissions */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '1.25rem' }}>
        {/* Recommendation History */}
        <div className="card" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Sparkles size={18} color="#a855f7" />
              <h2 style={{ fontSize: '1.1rem', fontWeight: 700, margin: 0, color: '#f4f4f5' }}>
                Recommendation History
              </h2>
            </div>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Latest 5</span>
          </div>

          {(recommendation_history || []).length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem 0', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
              No recommendation history recorded yet.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {(recommendation_history || []).map((rec) => (
                <div
                  key={rec.id}
                  style={{
                    background: '#18181b',
                    border: '1px solid #27272a',
                    borderRadius: '8px',
                    padding: '0.75rem 1rem',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '0.35rem'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.4rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                      <span style={{ fontWeight: 600, fontSize: '0.85rem', color: '#ffffff' }}>
                        {rec.problem_title}
                      </span>
                      {getDifficultyBadge(rec.difficulty)}
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                      {rec.is_active ? (
                        <span className="badge badge-purple" style={{ fontSize: '0.65rem' }}>Active</span>
                      ) : (
                        <span className="badge" style={{ background: '#27272a', color: '#71717a', fontSize: '0.65rem' }}>Archived</span>
                      )}
                    </div>
                  </div>

                  <p style={{ margin: 0, fontSize: '0.75rem', color: '#a1a1aa', lineHeight: 1.4 }}>
                    {rec.explanation_text.length > 130
                      ? rec.explanation_text.substring(0, 130) + '...'
                      : rec.explanation_text}
                  </p>

                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                    <span>Topic: {rec.topic_name}</span>
                    <span>Success Chance: {Math.round(rec.predicted_success_prob * 100)}%</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Submissions Feed */}
        <div className="card" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Code2 size={18} color="#22c55e" />
              <h2 style={{ fontSize: '1.1rem', fontWeight: 700, margin: 0, color: '#f4f4f5' }}>
                Recent Submissions
              </h2>
            </div>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Latest 5</span>
          </div>

          {(recent_submissions || []).length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem 0', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
              No submissions recorded yet. Pick a problem to start coding!
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {(recent_submissions || []).map((sub) => (
                <div
                  key={sub.submission_id}
                  style={{
                    background: '#18181b',
                    border: '1px solid #27272a',
                    borderRadius: '8px',
                    padding: '0.75rem 1rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    flexWrap: 'wrap',
                    gap: '0.5rem'
                  }}
                >
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.2rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                      <span style={{ fontWeight: 600, fontSize: '0.85rem', color: '#ffffff' }}>
                        {sub.problem_title}
                      </span>
                      {getDifficultyBadge(sub.difficulty)}
                    </div>
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                      {sub.topic_name} • {sub.execution_time_ms} ms
                    </span>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <span style={{ fontSize: '0.75rem', color: '#a1a1aa' }}>
                      {sub.passed_test_cases}/{sub.total_test_cases} Tests
                    </span>
                    {getStatusBadge(sub.status)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
