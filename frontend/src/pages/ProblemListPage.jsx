import React, { useState, useEffect } from 'react';
import {
  Search,
  Filter,
  Code2,
  Sparkles,
  ArrowRight,
  BookOpen,
  RefreshCw,
  Tag,
  CheckCircle2,
  BrainCircuit,
  Zap,
  Target,
  ChevronLeft,
  ChevronRight,
  Layers
} from 'lucide-react';
import { fetchProblems, fetchTopics, fetchNextRecommendation, generateRecommendation } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function ProblemListPage({ onSelectProblem }) {
  const { user, isAuthenticated } = useAuth();
  const [problems, setProblems] = useState([]);
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Recommendation state
  const [recommendation, setRecommendation] = useState(null);
  const [loadingRec, setLoadingRec] = useState(false);
  const [recError, setRecError] = useState(null);

  // Filter states
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('');
  const [diagnosticOnly, setDiagnosticOnly] = useState(false);
  const [catalogScope, setCatalogScope] = useState('all'); // 'all' | 'curated' | 'diagnostic'

  // Pagination states
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(25);

  const loadRecommendation = async () => {
    if (!isAuthenticated) return;
    setLoadingRec(true);
    setRecError(null);
    try {
      const recData = await fetchNextRecommendation();
      setRecommendation(recData);
    } catch (err) {
      console.warn('Could not load recommendation:', err);
    } finally {
      setLoadingRec(false);
    }
  };

  const handleRefreshRecommendation = async () => {
    if (!isAuthenticated) return;
    setLoadingRec(true);
    try {
      const freshRec = await generateRecommendation();
      setRecommendation(freshRec);
    } catch (err) {
      console.error('Failed to regenerate recommendation:', err);
    } finally {
      setLoadingRec(false);
    }
  };

  useEffect(() => {
    let isMounted = true;
    const loadData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [problemsData, topicsData] = await Promise.all([
          fetchProblems(),
          fetchTopics(),
        ]);
        if (isMounted) {
          setProblems(problemsData);
          setTopics(topicsData);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.response?.data?.detail || err.message || 'Failed to load problem catalog.');
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    loadData();
    if (isAuthenticated) {
      loadRecommendation();
    }
    return () => {
      isMounted = false;
    };
  }, [isAuthenticated]);

  // Reset page when any filter criteria changes
  useEffect(() => {
    setCurrentPage(1);
  }, [searchQuery, selectedTopic, selectedDifficulty, diagnosticOnly, catalogScope, pageSize]);

  const filteredProblems = problems.filter((p) => {
    const matchesSearch =
      p.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.topic?.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesTopic = selectedTopic ? p.topic?.slug === selectedTopic : true;
    const matchesDiff = selectedDifficulty ? p.difficulty?.toLowerCase() === selectedDifficulty.toLowerCase() : true;
    const matchesDiag = diagnosticOnly ? p.is_diagnostic : true;
    const matchesScope =
      catalogScope === 'curated'
        ? p.id <= 40
        : catalogScope === 'diagnostic'
        ? p.is_diagnostic
        : catalogScope === 'multilang'
        ? (p.supported_languages && p.supported_languages.length > 1)
        : true;

    return matchesSearch && matchesTopic && matchesDiff && matchesDiag && matchesScope;
  });

  // Calculate pagination slices
  const totalPages = Math.max(1, Math.ceil(filteredProblems.length / pageSize));
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = Math.min(startIndex + pageSize, filteredProblems.length);
  const paginatedProblems = filteredProblems.slice(startIndex, endIndex);

  const curatedCount = problems.filter((p) => p.id <= 40).length;
  const diagnosticCount = problems.filter((p) => p.is_diagnostic).length;
  const multiLangCount = problems.filter((p) => p.supported_languages && p.supported_languages.length > 1).length;

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

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Header Banner */}
      <div className="card" style={{ padding: '1.5rem', background: 'linear-gradient(135deg, #18181b 0%, #1e1e24 100%)' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <span className="badge badge-blue">
                <Code2 size={13} /> Curated DSA Bank
              </span>
              <span className="badge badge-green">
                {problems.length > 0 ? `${problems.length} Problems` : '889 Problems'}
              </span>
              <span className="badge badge-purple">
                <BrainCircuit size={13} /> AI Recommendation Engine
              </span>
            </div>
            <h1 style={{ fontSize: '1.5rem', fontWeight: 700, margin: 0, color: '#f4f4f5' }}>
              DSA Problem Catalog
            </h1>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '0.35rem', margin: 0 }}>
              Practice curated algorithmic problems across 10 foundational Data Structures and Algorithms domains.
            </p>
          </div>
        </div>
      </div>

      {/* AI Adaptive Recommendation Banner */}
      {isAuthenticated && recommendation?.problem && (
        <div 
          className="card" 
          style={{ 
            padding: '1.25rem 1.5rem', 
            background: 'linear-gradient(135deg, rgba(37, 99, 235, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%)',
            border: '1px solid rgba(99, 102, 241, 0.35)',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.25)'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '1rem', flexWrap: 'wrap' }}>
            <div style={{ flex: 1, minWidth: '280px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <span className="badge badge-purple" style={{ fontSize: '0.75rem', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                  <BrainCircuit size={13} /> Recommended Next Problem (ZPD)
                </span>
                {getDifficultyBadge(recommendation.problem.difficulty)}
                <span className="badge" style={{ background: '#27272a', color: '#a1a1aa' }}>
                  <Tag size={11} style={{ marginRight: 3 }} /> {recommendation.problem.topic_name}
                </span>
              </div>

              <h2 style={{ fontSize: '1.25rem', fontWeight: 700, margin: '0 0 0.5rem', color: '#ffffff' }}>
                {recommendation.problem.id}. {recommendation.problem.title}
              </h2>

              <p style={{ margin: '0 0 0.875rem', fontSize: '0.84rem', color: '#cbd5e1', lineHeight: 1.55 }}>
                {recommendation.explanation_text}
              </p>

              <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                <span>
                  Estimated Success Chance: <strong style={{ color: '#38bdf8' }}>{Math.round(recommendation.predicted_success_prob * 100)}%</strong>
                </span>
                <span>•</span>
                <span>Optimal Zone of Proximal Development Challenge</span>
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', minWidth: '160px' }}>
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => onSelectProblem(recommendation.problem.slug)}
                style={{ justifyContent: 'center', fontWeight: 600, padding: '0.6rem 1.2rem' }}
              >
                <Zap size={16} />
                <span>Solve Problem</span>
                <ArrowRight size={14} />
              </button>

              <button
                type="button"
                className="btn btn-secondary btn-sm"
                onClick={handleRefreshRecommendation}
                disabled={loadingRec}
                style={{ justifyContent: 'center', fontSize: '0.75rem' }}
              >
                <RefreshCw size={12} className={loadingRec ? 'spinning' : ''} />
                <span>{loadingRec ? 'Calculating...' : 'Get Another'}</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Catalog Scope Filter Tabs */}
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        <button
          type="button"
          onClick={() => setCatalogScope('all')}
          style={{
            padding: '0.45rem 0.9rem',
            fontSize: '0.8125rem',
            fontWeight: 600,
            borderRadius: 'var(--radius-sm)',
            border: '1px solid',
            borderColor: catalogScope === 'all' ? 'var(--accent-primary)' : 'var(--border-color)',
            background: catalogScope === 'all' ? 'rgba(59, 130, 246, 0.15)' : '#18181b',
            color: catalogScope === 'all' ? '#60a5fa' : 'var(--text-secondary)',
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.35rem',
          }}
        >
          <Layers size={14} />
          <span>All Problems ({problems.length})</span>
        </button>

        <button
          type="button"
          onClick={() => setCatalogScope('curated')}
          style={{
            padding: '0.45rem 0.9rem',
            fontSize: '0.8125rem',
            fontWeight: 600,
            borderRadius: 'var(--radius-sm)',
            border: '1px solid',
            borderColor: catalogScope === 'curated' ? '#22c55e' : 'var(--border-color)',
            background: catalogScope === 'curated' ? 'rgba(34, 197, 94, 0.15)' : '#18181b',
            color: catalogScope === 'curated' ? '#4ade80' : 'var(--text-secondary)',
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.35rem',
          }}
        >
          <Code2 size={14} />
          <span>Curated Core ({curatedCount || 40})</span>
        </button>

        <button
          type="button"
          onClick={() => setCatalogScope('diagnostic')}
          style={{
            padding: '0.45rem 0.9rem',
            fontSize: '0.8125rem',
            fontWeight: 600,
            borderRadius: 'var(--radius-sm)',
            border: '1px solid',
            borderColor: catalogScope === 'diagnostic' ? '#a855f7' : 'var(--border-color)',
            background: catalogScope === 'diagnostic' ? 'rgba(168, 85, 247, 0.15)' : '#18181b',
            color: catalogScope === 'diagnostic' ? '#c084fc' : 'var(--text-secondary)',
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.35rem',
          }}
        >
          <BrainCircuit size={14} />
          <span>Diagnostic Suite ({diagnosticCount || 7})</span>
        </button>

        <button
          type="button"
          onClick={() => setCatalogScope('multilang')}
          style={{
            padding: '0.45rem 0.9rem',
            fontSize: '0.8125rem',
            fontWeight: 600,
            borderRadius: 'var(--radius-sm)',
            border: '1px solid',
            borderColor: catalogScope === 'multilang' ? '#f59e0b' : 'var(--border-color)',
            background: catalogScope === 'multilang' ? 'rgba(245, 158, 11, 0.15)' : '#18181b',
            color: catalogScope === 'multilang' ? '#fbbf24' : 'var(--text-secondary)',
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.35rem',
          }}
        >
          <Sparkles size={14} />
          <span>Multi-Language ({multiLangCount || 6})</span>
        </button>
      </div>

      {/* Filter Bar */}
      <div className="card" style={{ padding: '1rem' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.75rem', alignItems: 'center' }}>
          {/* Search Box */}
          <div style={{ position: 'relative' }}>
            <Search size={16} style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
            <input
              type="text"
              placeholder="Search by title or topic..."
              className="form-input"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{ paddingLeft: '2.25rem' }}
            />
          </div>

          {/* Topic Dropdown */}
          <select
            className="form-input"
            value={selectedTopic}
            onChange={(e) => setSelectedTopic(e.target.value)}
          >
            <option value="">All Topics (10 Domains)</option>
            {topics.map((t) => (
              <option key={t.slug} value={t.slug}>
                {t.name}
              </option>
            ))}
          </select>

          {/* Difficulty Dropdown */}
          <select
            className="form-input"
            value={selectedDifficulty}
            onChange={(e) => setSelectedDifficulty(e.target.value)}
          >
            <option value="">All Difficulties</option>
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>

          {/* Diagnostic Toggle */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
              <input
                type="checkbox"
                checked={diagnosticOnly}
                onChange={(e) => setDiagnosticOnly(e.target.checked)}
                style={{ width: '16px', height: '16px', accentColor: 'var(--accent-primary)' }}
              />
              <span>Diagnostic Only</span>
            </label>
          </div>
        </div>
      </div>

      {/* Problem Table / Grid */}
      {loading ? (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
          <RefreshCw size={24} className="spinning" style={{ marginRight: '0.5rem' }} />
          <span>Loading curated problem library...</span>
        </div>
      ) : error ? (
        <div className="card" style={{ textAlign: 'center', color: '#f87171' }}>
          <p>{error}</p>
        </div>
      ) : filteredProblems.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
          <BookOpen size={32} style={{ margin: '0 auto 0.75rem', opacity: 0.6 }} />
          <p style={{ margin: 0 }}>No problems match your selected filters.</p>
        </div>
      ) : (
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.875rem' }}>
            <thead>
              <tr style={{ background: '#202024', borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                <th style={{ padding: '0.875rem 1.25rem', width: '60px' }}>#</th>
                <th style={{ padding: '0.875rem 1.25rem' }}>Title</th>
                <th style={{ padding: '0.875rem 1.25rem', width: '180px' }}>Topic</th>
                <th style={{ padding: '0.875rem 1.25rem', width: '120px' }}>Difficulty</th>
                <th style={{ padding: '0.875rem 1.25rem', width: '170px' }}>Languages</th>
                <th style={{ padding: '0.875rem 1.25rem', width: '120px', textAlign: 'right' }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {paginatedProblems.map((p) => (
                <tr
                  key={p.id}
                  style={{
                    borderBottom: '1px solid #27272a',
                    transition: 'background 0.15s ease',
                    cursor: 'pointer',
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.background = '#1e1e23')}
                  onMouseLeave={(e) => (e.currentTarget.style.background = 'transparent')}
                  onClick={() => onSelectProblem(p.slug)}
                >
                  <td style={{ padding: '0.875rem 1.25rem', color: 'var(--text-muted)', fontWeight: 500 }}>
                    {p.id}
                  </td>
                  <td style={{ padding: '0.875rem 1.25rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span style={{ fontWeight: 600, color: '#f4f4f5' }}>{p.title}</span>
                      {p.is_diagnostic && (
                        <span className="badge badge-purple" style={{ fontSize: '0.625rem', padding: '0.1rem 0.4rem' }}>
                          Diagnostic
                        </span>
                      )}
                    </div>
                  </td>
                  <td style={{ padding: '0.875rem 1.25rem' }}>
                    <span style={{ color: 'var(--text-secondary)', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                      <Tag size={12} color="var(--text-muted)" />
                      {p.topic?.name}
                    </span>
                  </td>
                  <td style={{ padding: '0.875rem 1.25rem' }}>
                    {getDifficultyBadge(p.difficulty)}
                  </td>
                  <td style={{ padding: '0.875rem 1.25rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem', flexWrap: 'wrap' }}>
                      {(p.supported_languages || ['python']).map((lang) => {
                        const pill = {
                          python: { label: 'Python', color: '#38bdf8', bg: 'rgba(56, 189, 248, 0.12)' },
                          java: { label: 'Java', color: '#f87171', bg: 'rgba(239, 68, 68, 0.12)' },
                          cpp: { label: 'C++', color: '#60a5fa', bg: 'rgba(59, 130, 246, 0.12)' },
                          javascript: { label: 'JS', color: '#facc15', bg: 'rgba(234, 179, 8, 0.12)' },
                        }[lang] || { label: lang, color: '#a1a1aa', bg: '#27272a' };
                        return (
                          <span
                            key={lang}
                            style={{
                              fontSize: '0.6875rem',
                              padding: '0.12rem 0.38rem',
                              fontWeight: 600,
                              color: pill.color,
                              background: pill.bg,
                              borderRadius: '3px',
                              border: `1px solid ${pill.color}33`,
                            }}
                          >
                            {pill.label}
                          </span>
                        );
                      })}
                    </div>
                  </td>
                  <td style={{ padding: '0.875rem 1.25rem', textAlign: 'right' }}>
                    <button
                      type="button"
                      className="btn btn-secondary btn-sm"
                      onClick={(e) => {
                        e.stopPropagation();
                        onSelectProblem(p.slug);
                      }}
                      style={{ fontSize: '0.75rem', padding: '0.3rem 0.75rem' }}
                    >
                      <span>Solve</span>
                      <ArrowRight size={12} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Pagination Controls */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '0.875rem 1.25rem',
              background: '#18181b',
              borderTop: '1px solid var(--border-color)',
              flexWrap: 'wrap',
              gap: '0.75rem',
              fontSize: '0.8125rem',
              color: 'var(--text-secondary)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <span>
                Showing {filteredProblems.length > 0 ? startIndex + 1 : 0}–{endIndex} of {filteredProblems.length} problems
              </span>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <span>Per page:</span>
                <select
                  className="form-input"
                  value={pageSize}
                  onChange={(e) => setPageSize(Number(e.target.value))}
                  style={{ padding: '0.2rem 0.5rem', fontSize: '0.75rem', width: '70px' }}
                >
                  <option value={25}>25</option>
                  <option value={50}>50</option>
                  <option value={100}>100</option>
                </select>
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
              <button
                type="button"
                className="btn btn-secondary btn-sm"
                onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                disabled={currentPage === 1}
                style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}
              >
                <ChevronLeft size={14} />
                <span>Prev</span>
              </button>

              <span style={{ padding: '0.2rem 0.5rem', fontWeight: 600, color: '#f4f4f5' }}>
                Page {currentPage} of {totalPages}
              </span>

              <button
                type="button"
                className="btn btn-secondary btn-sm"
                onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
                disabled={currentPage === totalPages}
                style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}
              >
                <span>Next</span>
                <ChevronRight size={14} />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
