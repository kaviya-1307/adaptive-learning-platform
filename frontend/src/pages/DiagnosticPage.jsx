import React, { useState, useEffect } from 'react';
import {
  BrainCircuit,
  CheckCircle2,
  XCircle,
  Clock,
  Play,
  ArrowRight,
  ArrowLeft,
  Award,
  AlertCircle,
  RefreshCw,
  BookOpen,
  Sparkles,
  Zap,
  Tag,
  Code2,
  Check
} from 'lucide-react';
import {
  fetchDiagnosticProblems,
  fetchDiagnosticHistory,
  fetchDiagnosticScore,
  submitDiagnosticAttempt,
  completeDiagnostic,
  runCode,
  fetchNextRecommendation
} from '../services/api';
import CodeEditor from '../components/CodeEditor';
import TestCasePanel from '../components/TestCasePanel';
import { useAuth } from '../context/AuthContext';

export default function DiagnosticPage({ onSelectProblem, onNavigate }) {
  const { user, isAuthenticated, refreshUser } = useAuth();
  const [problems, setProblems] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Per-problem user code, languages, and attempts state
  const [userCodes, setUserCodes] = useState({});
  const [selectedLanguages, setSelectedLanguages] = useState({});
  const [attempts, setAttempts] = useState({});
  const [evalResults, setEvalResults] = useState({});
  const [running, setRunning] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [completing, setCompleting] = useState(false);
  const [completedSummary, setCompletedSummary] = useState(null);
  const [recommendedProblem, setRecommendedProblem] = useState(null);

  // Time tracker
  const [timeSpent, setTimeSpent] = useState(0);

  const getDiagStarterCode = (prob, lang) => {
    if (!prob) return '';
    switch (lang) {
      case 'java':
        return prob.starter_code_java || '';
      case 'cpp':
        return prob.starter_code_cpp || '';
      case 'javascript':
        return prob.starter_code_javascript || '';
      case 'python':
      default:
        return prob.starter_code_python || '';
    }
  };

  useEffect(() => {
    let timerId;
    if (!completedSummary) {
      timerId = setInterval(() => {
        setTimeSpent((t) => t + 1);
      }, 1000);
    }
    return () => clearInterval(timerId);
  }, [completedSummary]);

  useEffect(() => {
    let isMounted = true;

    // If user has already completed diagnostic, fetch authoritative score from backend
    if (user?.diagnostic_completed) {
      setLoading(true);
      Promise.all([
        fetchDiagnosticScore().catch(() => ({
          diagnostic_completed: true,
          diagnostic_score: user.diagnostic_score !== null && user.diagnostic_score !== undefined ? user.diagnostic_score : 0,
          diagnostic_total: user.diagnostic_total || 7,
          score_percent: user.diagnostic_total ? Math.round(((user.diagnostic_score || 0) / user.diagnostic_total) * 100) : 0,
          knowledge_states_initialized: 10,
          diagnostic_completed_at: user.diagnostic_completed_at,
          attempts: []
        })),
        fetchNextRecommendation().catch(() => null)
      ]).then(([scoreData, rec]) => {
        if (!isMounted) return;
        const total = scoreData.diagnostic_total || user.diagnostic_total || 7;
        const solved = scoreData.diagnostic_score !== undefined ? scoreData.diagnostic_score : (user.diagnostic_score || 0);
        setCompletedSummary({
          total_problems: total,
          solved_count: solved,
          score_percent: scoreData.score_percent !== undefined ? scoreData.score_percent : (total > 0 ? Math.round((solved / total) * 100) : 0),
          knowledge_states_initialized: scoreData.knowledge_states_initialized || 10,
          diagnostic_completed_at: scoreData.diagnostic_completed_at || user.diagnostic_completed_at,
          attempts: scoreData.attempts || []
        });
        if (rec) setRecommendedProblem(rec);
        setLoading(false);
      });
      return;
    }

    const loadProblems = async () => {
      setLoading(true);
      setError(null);
      try {
        const [diagProblems, history] = await Promise.all([
          fetchDiagnosticProblems(),
          fetchDiagnosticHistory().catch(() => [])
        ]);
        if (isMounted) {
          setProblems(diagProblems);
          // Initialize starter codes and existing attempts
          const initialCodes = {};
          diagProblems.forEach((p) => {
            initialCodes[`${p.id}_python`] = p.starter_code_python || '# Write your solution here\n';
            if (p.starter_code_java) initialCodes[`${p.id}_java`] = p.starter_code_java;
            if (p.starter_code_cpp) initialCodes[`${p.id}_cpp`] = p.starter_code_cpp;
            if (p.starter_code_javascript) initialCodes[`${p.id}_javascript`] = p.starter_code_javascript;
          });
          if (history && history.length > 0) {
            const initialAttempts = {};
            const initialLangs = {};
            history.forEach((att) => {
              const attLang = att.language || 'python';
              initialAttempts[att.problem_id] = {
                is_solved: att.is_solved,
                time_spent_seconds: att.time_spent_seconds,
                code_submitted: att.code_submitted,
                language: attLang
              };
              if (att.code_submitted) {
                initialCodes[`${att.problem_id}_${attLang}`] = att.code_submitted;
              }
              initialLangs[att.problem_id] = attLang;
            });
            setAttempts(initialAttempts);
            setSelectedLanguages(initialLangs);
          }
          setUserCodes(initialCodes);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.response?.data?.detail || err.message || 'Failed to load diagnostic problems.');
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    if (isAuthenticated) {
      loadProblems();
    }
    return () => {
      isMounted = false;
    };
  }, [isAuthenticated]);

  const currentProblem = problems[currentIndex] || null;
  const activeLang = (currentProblem ? selectedLanguages[currentProblem.id] : null) || (currentProblem?.supported_languages?.[0] || 'python');
  const currentCodeKey = currentProblem ? `${currentProblem.id}_${activeLang}` : '';
  const currentCode = currentProblem
    ? (userCodes[currentCodeKey] !== undefined
        ? userCodes[currentCodeKey]
        : getDiagStarterCode(currentProblem, activeLang))
    : '';
  const currentAttempt = currentProblem ? attempts[currentProblem.id] : null;
  const currentEvalResult = currentProblem ? evalResults[currentProblem.id] : null;

  const handleCodeChange = (newCode) => {
    if (!currentProblem) return;
    const val = newCode !== undefined ? newCode : '';
    setUserCodes((prev) => ({
      ...prev,
      [`${currentProblem.id}_${activeLang}`]: val
    }));
  };

  const handleLanguageChange = (newLang) => {
    if (!currentProblem) return;
    setSelectedLanguages((prev) => ({
      ...prev,
      [currentProblem.id]: newLang
    }));
  };

  const handleResetCode = () => {
    if (!currentProblem) return;
    const starter = getDiagStarterCode(currentProblem, activeLang);
    setUserCodes((prev) => ({
      ...prev,
      [`${currentProblem.id}_${activeLang}`]: starter
    }));
  };

  const handleRunCode = async () => {
    if (!currentProblem) return;
    setRunning(true);
    try {
      const result = await runCode({
        problem_id: currentProblem.id,
        code: currentCode,
        language: activeLang
      });
      setEvalResults((prev) => ({
        ...prev,
        [currentProblem.id]: result
      }));
    } catch (err) {
      console.error('Run diagnostic code failed:', err);
    } finally {
      setRunning(false);
    }
  };

  const handleSubmitCode = async () => {
    if (!currentProblem) return;
    setSubmitting(true);
    try {
      const response = await submitDiagnosticAttempt({
        problem_id: currentProblem.id,
        time_spent_seconds: timeSpent,
        code_submitted: currentCode,
        language: activeLang
      });

      setEvalResults((prev) => ({
        ...prev,
        [currentProblem.id]: {
          status: response.status || (response.is_solved ? 'Accepted' : 'Wrong Answer'),
          passed_test_cases: response.passed_test_cases ?? (response.is_solved ? 1 : 0),
          total_test_cases: response.total_test_cases ?? 1,
          compile_error: response.compile_error,
          runtime_error: response.runtime_error,
        }
      }));

      setAttempts((prev) => ({
        ...prev,
        [currentProblem.id]: response
      }));
    } catch (err) {
      console.error('Submit diagnostic attempt failed:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleCompleteAssessment = async () => {
    setCompleting(true);
    try {
      const summary = await completeDiagnostic();
      setCompletedSummary(summary);
      if (refreshUser) {
        await refreshUser();
      }

      // Fetch active recommendation after diagnostic calibration
      try {
        const nextRec = await fetchNextRecommendation();
        setRecommendedProblem(nextRec);
      } catch (recErr) {
        console.warn('Could not fetch recommendation:', recErr);
      }
    } catch (err) {
      console.error('Complete diagnostic failed:', err);
      setError(err.response?.data?.detail || 'Failed to complete diagnostic assessment.');
    } finally {
      setCompleting(false);
    }
  };

  const formatTimer = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
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

  if (!isAuthenticated) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem', maxWidth: '540px', margin: '3rem auto' }}>
        <BrainCircuit size={44} color="var(--accent-primary)" style={{ margin: '0 auto 1rem' }} />
        <h2 style={{ fontSize: '1.4rem', fontWeight: 700, margin: '0 0 0.5rem', color: '#f4f4f5' }}>
          Diagnostic Assessment Requires Login
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '1.5rem' }}>
          Sign in or create an account to calibrate your baseline knowledge state across 10 DSA topics.
        </p>
        <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center' }}>
          <button type="button" className="btn btn-primary" onClick={() => onNavigate('login')}>
            Sign In
          </button>
          <button type="button" className="btn btn-secondary" onClick={() => onNavigate('register')}>
            Register
          </button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '5rem 0', color: 'var(--text-secondary)' }}>
        <RefreshCw size={36} className="spinning" style={{ marginBottom: '1rem', color: 'var(--accent-primary)' }} />
        <h3 style={{ margin: 0, color: '#f4f4f5' }}>Loading Diagnostic Assessment Suite...</h3>
        <p style={{ fontSize: '0.875rem', marginTop: '0.5rem', color: 'var(--text-muted)' }}>
          Preparing multi-topic baseline calibration problems.
        </p>
      </div>
    );
  }

  if (error && !completedSummary) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem', maxWidth: '560px', margin: '2rem auto' }}>
        <AlertCircle size={40} color="#ef4444" style={{ margin: '0 auto 1rem' }} />
        <h3 style={{ margin: '0 0 0.5rem', color: '#f4f4f5' }}>Diagnostic Suite Notice</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '1.5rem' }}>{error}</p>
        <button type="button" className="btn btn-primary" onClick={() => onNavigate('problems')}>
          Explore Problem Catalog
        </button>
      </div>
    );
  }

  // -------------------------------------------------------------
  // COMPLETED SUMMARY VIEW
  // -------------------------------------------------------------
  if (completedSummary) {
    return (
      <div style={{ maxWidth: '840px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div
          className="card"
          style={{
            padding: '2.5rem',
            textAlign: 'center',
            background: 'linear-gradient(135deg, #18181b 0%, #1e1e24 50%, #27272a 100%)',
            border: '1px solid rgba(34, 197, 94, 0.35)',
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)'
          }}
        >
          <div style={{ width: 64, height: 64, borderRadius: '50%', background: 'rgba(34, 197, 94, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.25rem', color: '#22c55e' }}>
            <Award size={36} />
          </div>

          <span className="badge badge-green" style={{ marginBottom: '0.75rem' }}>
            Assessment Calibrated
          </span>

          <h1 style={{ fontSize: '1.85rem', fontWeight: 800, margin: '0 0 0.5rem', color: '#ffffff' }}>
            Diagnostic Assessment Completed!
          </h1>
          {completedSummary.diagnostic_completed_at && (
            <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', margin: '0 0 0.75rem' }}>
              Completed on {new Date(completedSummary.diagnostic_completed_at).toLocaleString()}
            </p>
          )}
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem', maxWidth: '540px', margin: '0 auto 1.75rem', lineHeight: 1.6 }}>
            Your baseline knowledge profile has been calibrated across all 10 DSA topics. The AI recommendation engine is now tuned to your Zone of Proximal Development.
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
            <div style={{ background: '#18181b', border: '1px solid #27272a', borderRadius: '10px', padding: '1rem' }}>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Score</span>
              <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#38bdf8', marginTop: '0.2rem' }}>
                {completedSummary.score_percent}%
              </div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                {completedSummary.solved_count} of {completedSummary.total_problems} Solved
              </span>
            </div>

            <div style={{ background: '#18181b', border: '1px solid #27272a', borderRadius: '10px', padding: '1rem' }}>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Topics Calibrated</span>
              <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#22c55e', marginTop: '0.2rem' }}>
                {completedSummary.knowledge_states_initialized || 10}
              </div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                10 Core DSA Domains
              </span>
            </div>

            <div style={{ background: '#18181b', border: '1px solid #27272a', borderRadius: '10px', padding: '1rem' }}>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Total Duration</span>
              <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#eab308', marginTop: '0.2rem' }}>
                {formatTimer(timeSpent)}
              </div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                Assessment Time
              </span>
            </div>
          </div>

          {/* Next Recommended Problem Callout */}
          {recommendedProblem?.problem && (
            <div
              style={{
                textAlign: 'left',
                background: 'linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%)',
                border: '1px solid rgba(99, 102, 241, 0.4)',
                borderRadius: '12px',
                padding: '1.25rem 1.5rem',
                marginBottom: '2rem'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <span className="badge badge-purple" style={{ fontSize: '0.75rem', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                  <BrainCircuit size={13} /> Your First Recommended Problem
                </span>
                {getDifficultyBadge(recommendedProblem.problem.difficulty)}
                <span className="badge" style={{ background: '#27272a', color: '#a1a1aa' }}>
                  {recommendedProblem.problem.topic_name}
                </span>
              </div>

              <h3 style={{ fontSize: '1.2rem', fontWeight: 700, margin: '0 0 0.4rem', color: '#ffffff' }}>
                {recommendedProblem.problem.id}. {recommendedProblem.problem.title}
              </h3>
              <p style={{ fontSize: '0.84rem', color: '#cbd5e1', lineHeight: 1.5, margin: '0 0 1rem' }}>
                {recommendedProblem.explanation_text}
              </p>

              <button
                type="button"
                className="btn btn-primary"
                onClick={() => onSelectProblem(recommendedProblem.problem.slug)}
                style={{ fontWeight: 600, padding: '0.65rem 1.25rem' }}
              >
                <Zap size={16} />
                <span>Start Recommended Problem</span>
                <ArrowRight size={14} />
              </button>
            </div>
          )}

          <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center', flexWrap: 'wrap' }}>
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => onNavigate('dashboard')}
              style={{ minWidth: 200, padding: '0.75rem 1.5rem' }}
            >
              <Award size={18} />
              <span>Go to Learner Dashboard</span>
              <ArrowRight size={16} />
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => onNavigate('problems')}
              style={{ minWidth: 200, padding: '0.75rem 1.5rem' }}
            >
              <BookOpen size={18} />
              <span>Browse 889 Problems</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  // -------------------------------------------------------------
  // ACTIVE DIAGNOSTIC ASSESSMENT WORKSPACE
  // -------------------------------------------------------------
  const solvedAttemptsCount = Object.values(attempts).filter((a) => a.is_solved).length;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Header Banner */}
      <div
        className="card"
        style={{
          padding: '1.25rem 1.5rem',
          background: 'linear-gradient(135deg, #18181b 0%, #1e1e24 100%)',
          border: '1px solid var(--border-color)'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
              <span className="badge badge-purple" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}>
                <BrainCircuit size={13} /> Diagnostic Assessment
              </span>
              <span className="badge badge-blue">
                Problem {currentIndex + 1} of {problems.length}
              </span>
            </div>
            <h1 style={{ fontSize: '1.35rem', fontWeight: 700, margin: 0, color: '#f4f4f5' }}>
              Baseline Knowledge Calibration
            </h1>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              <Clock size={16} color="#eab308" />
              <span style={{ fontWeight: 600, color: '#f4f4f5', fontFamily: 'monospace' }}>
                {formatTimer(timeSpent)}
              </span>
            </div>

            <button
              type="button"
              className="btn btn-primary btn-sm"
              onClick={handleCompleteAssessment}
              disabled={completing}
              style={{ fontWeight: 600 }}
            >
              <Check size={14} />
              <span>{completing ? 'Finalizing...' : 'Complete Assessment'}</span>
            </button>
          </div>
        </div>

        {/* Progress Bar & Question Stepper */}
        <div style={{ marginTop: '1rem' }}>
          <div style={{ display: 'flex', gap: '0.4rem', marginBottom: '0.5rem' }}>
            {problems.map((p, idx) => {
              const isCurrent = idx === currentIndex;
              const isAttempted = attempts[p.id];
              const isSolved = isAttempted?.is_solved;

              return (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => setCurrentIndex(idx)}
                  style={{
                    flex: 1,
                    padding: '0.45rem 0.25rem',
                    background: isCurrent
                      ? 'var(--accent-primary)'
                      : isSolved
                      ? '#22c55e'
                      : isAttempted
                      ? '#ef4444'
                      : '#27272a',
                    border: 'none',
                    borderRadius: '4px',
                    color: isCurrent || isSolved || isAttempted ? '#ffffff' : '#a1a1aa',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                    transition: 'all 0.15s ease'
                  }}
                  title={`Problem ${idx + 1}: ${p.title} (${p.topic?.name || ''})`}
                >
                  Q{idx + 1}
                </button>
              );
            })}
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            <span>Solved: {solvedAttemptsCount} / {problems.length}</span>
            <span>Click any question to jump</span>
          </div>
        </div>
      </div>

      {/* Main Split Layout: Description on Left, Editor on Right */}
      {currentProblem && (
        <div style={{ display: 'grid', gridTemplateColumns: 'minmax(320px, 1fr) minmax(400px, 1.4fr)', gap: '1.25rem', alignItems: 'start' }}>
          {/* Left Column: Problem Details */}
          <div className="card" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span style={{ fontSize: '1.15rem', fontWeight: 700, color: '#f4f4f5' }}>
                  {currentIndex + 1}. {currentProblem.title}
                </span>
              </div>
              <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
                {getDifficultyBadge(currentProblem.difficulty)}
                <span className="badge" style={{ background: '#27272a', color: '#a1a1aa' }}>
                  <Tag size={11} style={{ marginRight: 3 }} />
                  {currentProblem.topic?.name}
                </span>
              </div>
            </div>

            {/* Description */}
            <div
              style={{
                fontSize: '0.875rem',
                color: '#e4e4e7',
                lineHeight: 1.6,
                background: '#18181b',
                padding: '1rem',
                borderRadius: '8px',
                border: '1px solid #27272a',
                whiteSpace: 'pre-wrap'
              }}
            >
              {currentProblem.description_markdown || 'No description available for this problem.'}
            </div>

            {/* Status indicator */}
            {currentAttempt && (
              <div
                style={{
                  padding: '0.6rem 0.8rem',
                  borderRadius: '6px',
                  fontSize: '0.8rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                  background: currentAttempt.is_solved ? 'rgba(34, 197, 94, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                  border: `1px solid ${currentAttempt.is_solved ? '#22c55e' : '#ef4444'}`,
                  color: currentAttempt.is_solved ? '#86efac' : '#fca5a5'
                }}
              >
                {currentAttempt.is_solved ? <CheckCircle2 size={14} /> : <XCircle size={14} />}
                <span>
                  {currentAttempt.is_solved
                    ? 'Attempt recorded as Solved!'
                    : 'Attempt submitted. Feel free to refine your code or proceed.'}
                </span>
              </div>
            )}

            {/* Navigation buttons */}
            <div style={{ display: 'flex', justifyContent: 'space-between', gap: '0.5rem', marginTop: 'auto', paddingTop: '1rem' }}>
              <button
                type="button"
                className="btn btn-secondary btn-sm"
                onClick={() => setCurrentIndex(Math.max(0, currentIndex - 1))}
                disabled={currentIndex === 0}
              >
                <ArrowLeft size={14} />
                <span>Previous</span>
              </button>

              <button
                type="button"
                className="btn btn-secondary btn-sm"
                onClick={() => setCurrentIndex(Math.min(problems.length - 1, currentIndex + 1))}
                disabled={currentIndex === problems.length - 1}
              >
                <span>Next</span>
                <ArrowRight size={14} />
              </button>
            </div>
          </div>

          {/* Right Column: Code Editor & Test Runner */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
              <div
                style={{
                  padding: '0.75rem 1rem',
                  background: '#202024',
                  borderBottom: '1px solid var(--border-color)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem', color: '#a1a1aa' }}>
                  <Code2 size={14} />
                  <span>{(currentProblem?.supported_languages && currentProblem.supported_languages.length > 1) ? 'Multi-Language Solution' : 'Solution Editor'}</span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <button
                    type="button"
                    className="btn btn-secondary btn-sm"
                    onClick={handleRunCode}
                    disabled={running || submitting}
                    style={{ padding: '0.35rem 0.85rem', fontSize: '0.8rem' }}
                    id="diag-run-code-btn"
                  >
                    <Play size={13} className={running ? 'spinning' : ''} />
                    <span>{running ? 'Running Tests...' : 'Run & Test Code'}</span>
                  </button>

                  <button
                    type="button"
                    className="btn btn-primary btn-sm"
                    onClick={handleSubmitCode}
                    disabled={running || submitting}
                    style={{ padding: '0.35rem 0.85rem', fontSize: '0.8rem', background: '#16a34a', borderColor: '#15803d' }}
                    id="diag-submit-code-btn"
                  >
                    <CheckCircle2 size={13} className={submitting ? 'spinning' : ''} />
                    <span>{submitting ? 'Evaluating...' : 'Submit Solution'}</span>
                  </button>
                </div>
              </div>

              <div style={{ height: '320px' }}>
                <CodeEditor
                  key={`diag-problem-${currentProblem?.id}-${activeLang}`}
                  code={currentCode}
                  value={currentCode}
                  onChange={handleCodeChange}
                  onReset={handleResetCode}
                  disabled={running || submitting || completing}
                  language={activeLang}
                  supportedLanguages={currentProblem?.supported_languages || ['python']}
                  onLanguageChange={handleLanguageChange}
                />
              </div>
            </div>

            {/* Test Case Execution Output */}
            {currentEvalResult && (
              <div className="card" style={{ padding: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                  <span style={{ fontSize: '0.85rem', fontWeight: 600, color: '#f4f4f5' }}>
                    Evaluation Result
                  </span>
                  <span
                    className={`badge ${
                      currentEvalResult.status === 'Accepted'
                        ? 'badge-green'
                        : currentEvalResult.status === 'Wrong Answer'
                        ? 'badge-red'
                        : 'badge-yellow'
                    }`}
                  >
                    {currentEvalResult.status} ({currentEvalResult.passed_test_cases}/{currentEvalResult.total_test_cases})
                  </span>
                </div>

                {currentEvalResult.compile_error && (
                  <pre
                    style={{
                      background: 'rgba(239, 68, 68, 0.1)',
                      border: '1px solid #ef4444',
                      color: '#fca5a5',
                      padding: '0.75rem',
                      borderRadius: '6px',
                      fontSize: '0.75rem',
                      whiteSpace: 'pre-wrap',
                      margin: '0 0 0.5rem'
                    }}
                  >
                    {currentEvalResult.compile_error}
                  </pre>
                )}

                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {(currentEvalResult.results || []).map((r, i) => (
                    <div
                      key={i}
                      style={{
                        background: '#18181b',
                        border: '1px solid #27272a',
                        borderRadius: '6px',
                        padding: '0.6rem 0.8rem',
                        fontSize: '0.75rem',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between'
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                        {r.status === 'Passed' ? (
                          <CheckCircle2 size={14} color="#22c55e" />
                        ) : (
                          <XCircle size={14} color="#ef4444" />
                        )}
                        <span style={{ color: '#f4f4f5' }}>Test Case #{i + 1}</span>
                      </div>
                      <span style={{ color: 'var(--text-muted)' }}>{r.execution_time_ms} ms</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
