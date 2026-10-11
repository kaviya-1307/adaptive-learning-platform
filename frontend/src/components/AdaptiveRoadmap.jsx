import React, { useState, useEffect } from 'react';
import {
  Map,
  CheckCircle2,
  Lock,
  Unlock,
  Play,
  Zap,
  Sparkles,
  AlertTriangle,
  RefreshCw,
  ArrowRight,
  BookOpen,
  Award,
  Flame,
  HelpCircle,
  Clock,
  Layers,
  ChevronRight,
  ChevronDown,
  Info
} from 'lucide-react';
import { fetchRoadmap, fetchProblems } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function AdaptiveRoadmap({ onSelectProblem, onNavigate }) {
  const { isAuthenticated } = useAuth();
  const [roadmap, setRoadmap] = useState(null);
  const [problemsMap, setProblemsMap] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedStageId, setSelectedStageId] = useState(null);
  const [expandedConcepts, setExpandedConcepts] = useState({});

  const loadRoadmapData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [roadmapData, problemsData] = await Promise.all([
        fetchRoadmap(),
        fetchProblems().catch(() => [])
      ]);

      setRoadmap(roadmapData);

      // Map problem ID -> problem object
      const pMap = {};
      if (Array.isArray(problemsData)) {
        problemsData.forEach((p) => {
          pMap[p.id] = p;
        });
      }
      setProblemsMap(pMap);

      // Default selected stage to current active stage or first available
      if (roadmapData?.stages?.length > 0) {
        const activeStage = roadmapData.stages.find(
          (s) => s.stage_name.toLowerCase() === (roadmapData.current_stage || '').toLowerCase()
        ) || roadmapData.stages.find((s) => s.status === 'in_progress' || s.status === 'available') || roadmapData.stages[0];

        setSelectedStageId(activeStage.stage_id);
      }
    } catch (err) {
      console.error('Failed to load adaptive roadmap:', err);
      if (err.response && err.response.status === 401) {
        setError('unauthorized');
      } else {
        setError(err.response?.data?.detail || err.message || 'Failed to load adaptive roadmap.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      loadRoadmapData();
    } else {
      setLoading(false);
      setError('unauthorized');
    }
  }, [isAuthenticated]);

  const toggleConceptExpand = (conceptKey) => {
    setExpandedConcepts((prev) => ({
      ...prev,
      [conceptKey]: !prev[conceptKey]
    }));
  };

  const getStageStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return (
          <span className="badge badge-green" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
            <CheckCircle2 size={12} /> Completed
          </span>
        );
      case 'in_progress':
        return (
          <span className="badge badge-blue" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
            <Play size={12} /> In Progress
          </span>
        );
      case 'available':
        return (
          <span className="badge badge-purple" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
            <Unlock size={12} /> Available
          </span>
        );
      case 'locked':
      default:
        return (
          <span className="badge" style={{ background: '#27272a', color: '#71717a', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
            <Lock size={12} /> Locked
          </span>
        );
    }
  };

  const getConceptStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return (
          <span className="badge badge-green" style={{ fontSize: '0.7rem' }}>
            <CheckCircle2 size={10} style={{ marginRight: 2 }} /> Mastered
          </span>
        );
      case 'in_progress':
        return (
          <span className="badge badge-blue" style={{ fontSize: '0.7rem' }}>
            <Play size={10} style={{ marginRight: 2 }} /> In Progress
          </span>
        );
      case 'available':
        return (
          <span className="badge badge-purple" style={{ fontSize: '0.7rem' }}>
            Ready
          </span>
        );
      case 'locked':
      default:
        return (
          <span className="badge" style={{ background: '#27272a', color: '#71717a', fontSize: '0.7rem' }}>
            Locked
          </span>
        );
    }
  };

  const getWeaknessBadge = (level) => {
    switch (level) {
      case 'Very High':
        return <span className="badge badge-red" style={{ fontSize: '0.65rem' }}>Very High Gap</span>;
      case 'High':
        return <span className="badge badge-yellow" style={{ fontSize: '0.65rem', background: 'rgba(239, 68, 68, 0.15)', color: '#f87171' }}>High Gap</span>;
      case 'Moderate':
        return <span className="badge badge-yellow" style={{ fontSize: '0.65rem' }}>Moderate</span>;
      case 'Low':
        return <span className="badge badge-blue" style={{ fontSize: '0.65rem' }}>Low Gap</span>;
      case 'Very Low':
        return <span className="badge badge-green" style={{ fontSize: '0.65rem' }}>Strong</span>;
      default:
        return null;
    }
  };

  const getDifficultyBadge = (diff) => {
    switch (diff?.toLowerCase()) {
      case 'easy':
        return <span className="badge badge-green" style={{ fontSize: '0.7rem' }}>Easy</span>;
      case 'medium':
        return <span className="badge badge-blue" style={{ fontSize: '0.7rem' }}>Medium</span>;
      case 'hard':
        return <span className="badge badge-red" style={{ fontSize: '0.7rem' }}>Hard</span>;
      default:
        return <span className="badge badge-blue" style={{ fontSize: '0.7rem' }}>{diff || 'Easy'}</span>;
    }
  };

  // 1. Loading State
  if (loading) {
    return (
      <div className="card" style={{ padding: '3.5rem 2rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
        <RefreshCw size={36} className="spinning" style={{ margin: '0 auto 1rem', color: 'var(--accent-primary)' }} />
        <h3 style={{ margin: '0 0 0.5rem', color: '#f4f4f5' }}>Synthesizing Adaptive Roadmap...</h3>
        <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', maxWidth: '480px', margin: '0 auto' }}>
          Calibrating 4-stage progression across 37 learning concepts, prerequisite gates, and personalized problem recommendations.
        </p>
      </div>
    );
  }

  // 2. Unauthenticated 401 State
  if (error === 'unauthorized') {
    return (
      <div className="card" style={{ padding: '3rem 2rem', textAlign: 'center', maxWidth: '600px', margin: '2rem auto' }}>
        <Lock size={42} color="#a855f7" style={{ margin: '0 auto 1rem' }} />
        <h3 style={{ margin: '0 0 0.5rem', color: '#f4f4f5' }}>Personalized Roadmap Locked</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1.5rem', lineHeight: 1.6 }}>
          Sign in or register to access your dynamic 4-stage learning path, concept mastery tracking, and prerequisite-aware problem recommendations.
        </p>
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => onNavigate && onNavigate('login')}
        >
          Sign In to Unlock
        </button>
      </div>
    );
  }

  // 3. API Error State
  if (error) {
    return (
      <div className="card" style={{ padding: '2.5rem 2rem', textAlign: 'center', maxWidth: '600px', margin: '2rem auto', border: '1px solid rgba(239, 68, 68, 0.4)' }}>
        <AlertTriangle size={36} color="#ef4444" style={{ margin: '0 auto 1rem' }} />
        <h3 style={{ margin: '0 0 0.5rem', color: '#f4f4f5' }}>Unable to Load Roadmap</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '1.5rem' }}>{error}</p>
        <button type="button" className="btn btn-primary" onClick={loadRoadmapData}>
          <RefreshCw size={14} style={{ marginRight: '0.4rem' }} /> Retry Loading
        </button>
      </div>
    );
  }

  // 4. Empty State
  if (!roadmap || !roadmap.stages || roadmap.stages.length === 0) {
    return (
      <div className="card" style={{ padding: '3rem 2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
        <Map size={36} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
        <h3 style={{ margin: '0 0 0.5rem', color: '#f4f4f5' }}>No Roadmap Stages Available</h3>
        <p style={{ fontSize: '0.875rem' }}>Complete onboarding or diagnostic assessment to initialize your roadmap.</p>
      </div>
    );
  }

  const stages = roadmap.stages;
  const currentStageName = roadmap.current_stage || 'Foundations';
  const selectedStage = stages.find((s) => s.stage_id === selectedStageId) || stages[0];

  // Resolve recommended problems for selected stage
  const stageRecommendedProblems = (selectedStage.recommended_problem_ids || [])
    .map((pid) => problemsMap[pid])
    .filter(Boolean);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Roadmap Header & Overall Progress Banner */}
      <div
        className="card"
        style={{
          padding: '1.75rem 2rem',
          background: 'linear-gradient(135deg, #18181b 0%, #1f1d2b 50%, #262338 100%)',
          border: '1px solid rgba(168, 85, 247, 0.3)',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.35)'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem' }}>
              <span className="badge badge-purple" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                <Map size={13} /> Adaptive Learning Roadmap
              </span>
              <span className="badge badge-blue">
                Active Stage: {currentStageName}
              </span>
              <span className="badge badge-green">
                {roadmap.completed_stages} / {roadmap.total_stages} Stages Completed
              </span>
            </div>
            <h2 style={{ fontSize: '1.65rem', fontWeight: 800, margin: '0 0 0.4rem', color: '#ffffff', letterSpacing: '-0.02em' }}>
              Your Personalized DSA Progression Pathway
            </h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', margin: 0, maxWidth: '720px', lineHeight: 1.5 }}>
              4 prerequisite-governed stages spanning 37 algorithmic learning concepts. Complete concepts with mastery &ge; 70% to unlock downstream stages and solve tailored practice problems.
            </p>
          </div>

          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={loadRoadmapData}
            title="Refresh roadmap with latest submission & diagnostic evidence"
          >
            <RefreshCw size={13} style={{ marginRight: '0.4rem' }} />
            <span>Sync Roadmap</span>
          </button>
        </div>

        {/* Overall Roadmap Progress Bar */}
        <div style={{ marginTop: '1.25rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.8rem', marginBottom: '0.4rem' }}>
            <span style={{ color: 'var(--text-secondary)', fontWeight: 600 }}>Overall Curriculum Completion</span>
            <span style={{ color: '#c084fc', fontWeight: 700 }}>{roadmap.overall_progress_percent}%</span>
          </div>
          <div style={{ width: '100%', height: '8px', background: '#27272a', borderRadius: '4px', overflow: 'hidden' }}>
            <div
              style={{
                width: `${roadmap.overall_progress_percent}%`,
                height: '100%',
                background: 'linear-gradient(90deg, #a855f7, #6366f1)',
                borderRadius: '4px',
                transition: 'width 0.5s ease'
              }}
            />
          </div>
        </div>
      </div>

      {/* 4 Stage Stepper / Selector Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
        {stages.map((stage, idx) => {
          const isSelected = stage.stage_id === selectedStageId;
          const isCurrentActive = stage.stage_name.toLowerCase() === currentStageName.toLowerCase();
          const isLocked = stage.status === 'locked';

          return (
            <div
              key={stage.stage_id}
              onClick={() => setSelectedStageId(stage.stage_id)}
              className="card"
              style={{
                padding: '1.25rem',
                cursor: 'pointer',
                background: isSelected
                  ? 'linear-gradient(135deg, rgba(99, 102, 241, 0.18) 0%, rgba(168, 85, 247, 0.12) 100%)'
                  : '#18181b',
                border: isSelected
                  ? '1px solid #a855f7'
                  : isCurrentActive
                  ? '1px solid rgba(59, 130, 246, 0.5)'
                  : '1px solid #27272a',
                boxShadow: isSelected ? '0 4px 20px rgba(168, 85, 247, 0.2)' : 'none',
                transition: 'all 0.2s ease',
                position: 'relative',
                overflow: 'hidden'
              }}
            >
              {/* Active Stage Indicator Glow */}
              {isCurrentActive && (
                <div
                  style={{
                    position: 'absolute',
                    top: 0,
                    right: 0,
                    background: 'linear-gradient(135deg, #3b82f6, #6366f1)',
                    color: '#ffffff',
                    fontSize: '0.62rem',
                    fontWeight: 700,
                    padding: '0.2rem 0.6rem',
                    borderBottomLeftRadius: '6px',
                    letterSpacing: '0.05em'
                  }}
                >
                  CURRENT FOCUS
                </div>
              )}

              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                  Stage {stage.order_index} of {stages.length}
                </span>
                {getStageStatusBadge(stage.status)}
              </div>

              <h3 style={{ fontSize: '1.05rem', fontWeight: 700, margin: '0 0 0.35rem', color: isLocked ? '#a1a1aa' : '#ffffff' }}>
                {stage.stage_name}
              </h3>

              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '0.4rem' }}>
                <span>{stage.completed_concepts} / {stage.total_concepts} Concepts</span>
                <span style={{ fontWeight: 600, color: '#e4e4e7' }}>{stage.progress_percent}%</span>
              </div>

              {/* Progress Bar */}
              <div style={{ width: '100%', height: '5px', background: '#27272a', borderRadius: '3px', overflow: 'hidden' }}>
                <div
                  style={{
                    width: `${stage.progress_percent}%`,
                    height: '100%',
                    background:
                      stage.status === 'completed'
                        ? '#22c55e'
                        : isLocked
                        ? '#52525b'
                        : 'linear-gradient(90deg, #6366f1, #a855f7)',
                    borderRadius: '3px',
                    transition: 'width 0.4s ease'
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Selected Stage Detail View */}
      {selectedStage && (
        <div
          className="card"
          style={{
            padding: '1.75rem',
            background: '#18181b',
            border: '1px solid #27272a',
            display: 'flex',
            flexDirection: 'column',
            gap: '1.5rem'
          }}
        >
          {/* Stage Banner Header */}
          <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem', borderBottom: '1px solid #27272a', paddingBottom: '1.25rem' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem' }}>
                <span className="badge" style={{ background: '#27272a', color: '#cbd5e1' }}>
                  Stage {selectedStage.order_index} of {stages.length}
                </span>
                {getStageStatusBadge(selectedStage.status)}
                {selectedStage.prerequisites && selectedStage.prerequisites.length > 0 && (
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    Requires: {selectedStage.prerequisites.join(', ')}
                  </span>
                )}
              </div>
              <h3 style={{ fontSize: '1.4rem', fontWeight: 800, margin: '0 0 0.35rem', color: '#ffffff' }}>
                {selectedStage.stage_name}
              </h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', margin: 0 }}>
                {selectedStage.description}
              </p>
            </div>

            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#f4f4f5' }}>
                {selectedStage.progress_percent}%
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                {selectedStage.completed_concepts} of {selectedStage.total_concepts} Concepts Completed
              </div>
            </div>
          </div>

          {/* Recommended Problems for Selected Stage */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Zap size={16} color="#eab308" />
                <h4 style={{ margin: 0, fontSize: '1rem', fontWeight: 700, color: '#f4f4f5' }}>
                  Recommended Practice for {selectedStage.stage_name}
                </h4>
              </div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                Ranked by 0.60*Concept Gap + 0.40*Difficulty Fit
              </span>
            </div>

            {stageRecommendedProblems.length > 0 ? (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '0.75rem' }}>
                {stageRecommendedProblems.map((p) => (
                  <div
                    key={p.id}
                    style={{
                      background: '#121214',
                      border: '1px solid #27272a',
                      borderRadius: '8px',
                      padding: '0.85rem 1rem',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      gap: '0.75rem',
                      transition: 'border-color 0.15s ease'
                    }}
                  >
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', flexWrap: 'wrap' }}>
                        <span style={{ fontWeight: 600, fontSize: '0.85rem', color: '#ffffff' }}>
                          {p.title}
                        </span>
                        {getDifficultyBadge(p.difficulty)}
                      </div>
                      <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                        {p.topic?.name || 'DSA'} • Numerical Rating: {p.difficulty_rating || 1000}
                      </span>
                    </div>

                    <button
                      type="button"
                      className="btn btn-primary btn-sm"
                      onClick={() => onSelectProblem && onSelectProblem(p.slug)}
                      style={{ padding: '0.45rem 0.85rem', fontSize: '0.78rem', whiteSpace: 'nowrap' }}
                    >
                      <span>Solve</span>
                      <ArrowRight size={13} />
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <div
                style={{
                  background: '#121214',
                  border: '1px dashed #27272a',
                  borderRadius: '8px',
                  padding: '1.25rem',
                  textAlign: 'center',
                  color: 'var(--text-muted)',
                  fontSize: '0.82rem'
                }}
              >
                {selectedStage.status === 'completed'
                  ? '🎉 All core learning objectives in this stage completed! Move ahead to the next stage.'
                  : selectedStage.status === 'locked'
                  ? 'Complete prerequisite stages to unlock problem recommendations for this tier.'
                  : 'Practice current unattempted problems in the Problems tab to advance this stage.'}
              </div>
            )}
          </div>

          {/* Concepts Grid for Selected Stage */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Layers size={16} color="#38bdf8" />
                <h4 style={{ margin: 0, fontSize: '1rem', fontWeight: 700, color: '#f4f4f5' }}>
                  Stage Learning Concepts ({selectedStage.concepts.length})
                </h4>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
                  <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#ef4444' }} /> Confirmed Gap
                </span>
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
                  <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#71717a' }} /> Untested Prior
                </span>
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
                  <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#22c55e' }} /> Mastered
                </span>
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '0.75rem' }}>
              {selectedStage.concepts.map((conceptItem) => {
                const masteryPct = Math.round(conceptItem.mastery_score * 100);
                const weaknessPct = Math.round(conceptItem.weakness_score * 100);
                const isConfirmedWeakness = conceptItem.is_confirmed_weakness;
                const isUntested = conceptItem.interactions === 0;
                const isMastered = conceptItem.status === 'completed';

                return (
                  <div
                    key={conceptItem.concept}
                    style={{
                      background: isConfirmedWeakness
                        ? 'rgba(239, 68, 68, 0.05)'
                        : isMastered
                        ? 'rgba(34, 197, 94, 0.04)'
                        : '#141416',
                      border: isConfirmedWeakness
                        ? '1px solid rgba(239, 68, 68, 0.35)'
                        : isMastered
                        ? '1px solid rgba(34, 197, 94, 0.3)'
                        : '1px solid #27272a',
                      borderRadius: '8px',
                      padding: '0.85rem 1rem',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '0.45rem',
                      transition: 'border-color 0.15s ease'
                    }}
                  >
                    {/* Header Row */}
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                        <span style={{ fontWeight: 700, fontSize: '0.85rem', color: '#f4f4f5', textTransform: 'capitalize' }}>
                          {conceptItem.concept}
                        </span>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                        {isConfirmedWeakness && (
                          <span
                            className="badge badge-red"
                            style={{ fontSize: '0.62rem', padding: '0.15rem 0.45rem' }}
                            title="Empirically confirmed knowledge gap from diagnostic or practice failure"
                          >
                            ⚠ Gap #{conceptItem.priority}
                          </span>
                        )}
                        {isUntested && (
                          <span
                            className="badge"
                            style={{ background: '#27272a', color: '#94a3b8', fontSize: '0.62rem', padding: '0.15rem 0.45rem' }}
                            title="Neutral Bayesian prior (mastery=0.50). No diagnostic or practice attempts yet."
                          >
                            Untested Prior
                          </span>
                        )}
                        {getConceptStatusBadge(conceptItem.status)}
                      </div>
                    </div>

                    {/* Progress Bar */}
                    <div style={{ width: '100%', height: '5px', background: '#27272a', borderRadius: '3px', overflow: 'hidden' }}>
                      <div
                        style={{
                          width: `${masteryPct}%`,
                          height: '100%',
                          background:
                            isMastered
                              ? 'linear-gradient(90deg, #10b981, #22c55e)'
                              : isConfirmedWeakness
                              ? 'linear-gradient(90deg, #ef4444, #f97316)'
                              : isUntested
                              ? '#52525b'
                              : 'linear-gradient(90deg, #3b82f6, #60a5fa)',
                          borderRadius: '3px',
                          transition: 'width 0.4s ease'
                        }}
                      />
                    </div>

                    {/* Metrics Row */}
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                      <span>
                        Mastery: <strong style={{ color: isConfirmedWeakness ? '#fca5a5' : '#e4e4e7' }}>{masteryPct}%</strong>
                      </span>
                      <span>
                        Weakness: <strong style={{ color: isConfirmedWeakness ? '#ef4444' : '#a1a1aa' }}>{weaknessPct}%</strong>
                      </span>
                      <span>
                        Evidence: {conceptItem.solved_count}/{conceptItem.interactions} Solved
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
