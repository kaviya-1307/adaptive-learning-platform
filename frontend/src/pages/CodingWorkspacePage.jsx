import React, { useState, useEffect } from 'react';
import {
  Play,
  CheckCircle,
  ArrowLeft,
  BookOpen,
  History,
  Clock,
  Sparkles,
  AlertCircle,
  RefreshCw,
  FileCode2,
  Tag,
  CheckCircle2,
  XCircle
} from 'lucide-react';
import CodeEditor from '../components/CodeEditor';
import TestCasePanel from '../components/TestCasePanel';
import { fetchProblemBySlug, runCode, submitCode, fetchSubmissionHistory, fetchNextRecommendation } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function CodingWorkspacePage({
  problemSlug = 'two-sum-target-pair',
  onBack,
  onNavigateToAuth,
  onSelectProblem
}) {
  const { user, isAuthenticated } = useAuth();

  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [code, setCode] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('python');
  const [activeLeftTab, setActiveLeftTab] = useState('description'); // 'description' | 'submissions'
  const [activeBottomTab, setActiveBottomTab] = useState('cases'); // 'cases' | 'result'

  const [isRunning, setIsRunning] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [executionResult, setExecutionResult] = useState(null);
  const [nextRecommendation, setNextRecommendation] = useState(null);

  const [submissionHistory, setSubmissionHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  const getStarterCode = (prob, lang) => {
    if (!prob) return '';
    switch (lang) {
      case 'java':
        return prob.starter_code_java || prob.starter_code_python || '';
      case 'cpp':
        return prob.starter_code_cpp || prob.starter_code_python || '';
      case 'javascript':
        return prob.starter_code_javascript || prob.starter_code_python || '';
      case 'python':
      default:
        return prob.starter_code_python || '';
    }
  };

  // Fetch problem details
  useEffect(() => {
    let isMounted = true;
    setNextRecommendation(null);
    const loadProblem = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchProblemBySlug(problemSlug);
        if (isMounted) {
          setProblem(data);
          setSelectedLanguage('python');
          setCode(data.starter_code_python || '');
        }
      } catch (err) {
        if (isMounted) {
          setError(err.response?.data?.detail || err.message || 'Failed to load problem.');
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    loadProblem();
    return () => {
      isMounted = false;
    };
  }, [problemSlug]);

  const handleLanguageChange = (newLang) => {
    setSelectedLanguage(newLang);
    setCode(getStarterCode(problem, newLang));
  };

  // Fetch submission history when submissions tab is activated
  const loadHistory = async () => {
    if (!problem?.id || !isAuthenticated) return;
    setLoadingHistory(true);
    try {
      const history = await fetchSubmissionHistory(problem.id);
      setSubmissionHistory(history);
    } catch (err) {
      console.error('Failed to load submission history:', err);
    } finally {
      setLoadingHistory(false);
    }
  };

  useEffect(() => {
    if (activeLeftTab === 'submissions' && problem?.id) {
      loadHistory();
    }
  }, [activeLeftTab, problem?.id, isAuthenticated]);

  const handleResetCode = () => {
    setCode(getStarterCode(problem, selectedLanguage));
  };

  const handleRunCode = async () => {
    if (!problem) return;
    if (!isAuthenticated) {
      setActiveBottomTab('result');
      setExecutionResult({
        status: 'Authentication Required',
        passed_test_cases: 0,
        total_test_cases: problem.visible_test_cases?.length || 0,
        execution_time_ms: 0,
        compile_error: 'Please sign in to your learner account to execute code against test cases.',
        results: [],
        authRequired: true,
      });
      return;
    }

    setIsRunning(true);
    setActiveBottomTab('result');
    try {
      const result = await runCode({
        problem_id: problem.id,
        code: code,
        language: selectedLanguage,
      });
      setExecutionResult(result);
    } catch (err) {
      const is401 = err.response?.status === 401;
      setExecutionResult({
        status: is401 ? 'Authentication Required' : 'Runtime Error',
        passed_test_cases: 0,
        total_test_cases: problem.visible_test_cases?.length || 0,
        execution_time_ms: 0,
        compile_error: is401
          ? 'Your session may have expired or is not authenticated. Please sign in to run code.'
          : (err.response?.data?.detail || err.message || 'Execution failed'),
        results: [],
        authRequired: is401,
      });
    } finally {
      setIsRunning(false);
    }
  };

  const handleSubmitCode = async () => {
    if (!problem) return;
    if (!isAuthenticated) {
      setActiveBottomTab('result');
      setExecutionResult({
        status: 'Authentication Required',
        passed_test_cases: 0,
        total_test_cases: problem.visible_test_cases?.length || 0,
        execution_time_ms: 0,
        compile_error: 'Please sign in to your learner account to submit your solution and record progress.',
        results: [],
        authRequired: true,
      });
      return;
    }

    setIsSubmitting(true);
    setActiveBottomTab('result');
    try {
      const result = await submitCode({
        problem_id: problem.id,
        code: code,
        language: selectedLanguage,
      });
      setExecutionResult(result);
      try {
        const nextRec = await fetchNextRecommendation();
        setNextRecommendation(nextRec);
      } catch (recErr) {
        console.warn('Could not load next recommendation after submission:', recErr);
      }
      if (activeLeftTab === 'submissions') {
        loadHistory();
      }
    } catch (err) {
      const is401 = err.response?.status === 401;
      setExecutionResult({
        status: is401 ? 'Authentication Required' : 'Runtime Error',
        passed_test_cases: 0,
        total_test_cases: problem.visible_test_cases?.length || 0,
        execution_time_ms: 0,
        compile_error: is401
          ? 'Your session may have expired. Please sign in again to submit solutions.'
          : (err.response?.data?.detail || err.message || 'Submission failed'),
        results: [],
        authRequired: is401,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  // Keyboard shortcut Ctrl+Enter to run
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (!isRunning && !isSubmitting) {
          handleRunCode();
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [code, problem, isRunning, isSubmitting]);

  const getDifficultyBadgeClass = (diff) => {
    switch (diff?.toLowerCase()) {
      case 'easy':
        return 'badge-green';
      case 'medium':
        return 'badge-blue';
      case 'hard':
        return 'badge-red';
      default:
        return 'badge-blue';
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', color: 'var(--text-secondary)' }}>
        <RefreshCw size={24} className="spinning" style={{ marginRight: '0.5rem' }} />
        <span>Loading problem workspace...</span>
      </div>
    );
  }

  if (error || !problem) {
    return (
      <div className="card" style={{ maxWidth: '600px', margin: '2rem auto', textAlign: 'center' }}>
        <AlertCircle size={36} color="#f87171" style={{ margin: '0 auto 1rem' }} />
        <h3>Failed to Load Problem</h3>
        <p style={{ color: 'var(--text-secondary)', margin: '0.5rem 0 1.5rem' }}>{error}</p>
        <button type="button" className="btn btn-primary" onClick={onBack}>
          <ArrowLeft size={16} />
          <span>Back to Problem List</span>
        </button>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', height: 'calc(100vh - 120px)', minHeight: '700px' }}>
      {/* Top Breadcrumb & Actions Bar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0.5rem 0',
          borderBottom: '1px solid var(--border-color)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={onBack}
            title="Return to Problem Catalog"
          >
            <ArrowLeft size={14} />
            <span>Catalog</span>
          </button>

          <h2 style={{ fontSize: '1.125rem', fontWeight: 600, margin: 0, color: 'var(--text-primary)' }}>
            {problem.id}. {problem.title}
          </h2>

          <span className={`badge ${getDifficultyBadgeClass(problem.difficulty)}`}>
            {problem.difficulty}
          </span>

          <span className="badge" style={{ background: '#27272a', color: '#a1a1aa', border: '1px solid #3f3f46' }}>
            <Tag size={11} style={{ marginRight: 4 }} />
            {problem.topic?.name}
          </span>

          {problem.is_diagnostic && (
            <span className="badge badge-purple" style={{ fontSize: '0.6875rem' }}>
              <Sparkles size={11} style={{ marginRight: 3 }} /> Diagnostic
            </span>
          )}
        </div>

        {/* Action Buttons: Run & Submit */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={handleRunCode}
            disabled={isRunning || isSubmitting}
            style={{ fontWeight: 600 }}
          >
            <Play size={14} color="#38bdf8" />
            <span>{isRunning ? 'Running...' : 'Run Code (Ctrl+Enter)'}</span>
          </button>

          <button
            type="button"
            className="btn btn-primary btn-sm"
            onClick={handleSubmitCode}
            disabled={isRunning || isSubmitting}
            style={{ fontWeight: 600, background: '#16a34a', borderColor: '#15803d' }}
          >
            <CheckCircle size={14} />
            <span>{isSubmitting ? 'Submitting...' : 'Submit Solution'}</span>
          </button>
        </div>
      </div>

      {/* Main Split Layout: 50% Left Description/History, 50% Right Code/Testcases */}
      <div style={{ display: 'grid', gridTemplateColumns: '45% 55%', gap: '0.75rem', flex: 1, minHeight: 0 }}>
        {/* ================= LEFT PANE ================= */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            background: 'var(--bg-secondary)',
            border: '1px solid var(--border-color)',
            borderRadius: 'var(--radius-md)',
            overflow: 'hidden',
          }}
        >
          {/* Left Pane Navigation Tabs */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              borderBottom: '1px solid var(--border-color)',
              background: '#202023',
              padding: '0.25rem 0.5rem',
              gap: '0.375rem',
            }}
          >
            <button
              type="button"
              onClick={() => setActiveLeftTab('description')}
              style={{
                padding: '0.4rem 0.75rem',
                fontSize: '0.8125rem',
                fontWeight: 600,
                background: activeLeftTab === 'description' ? '#27272a' : 'transparent',
                color: activeLeftTab === 'description' ? '#ffffff' : 'var(--text-secondary)',
                border: 'none',
                borderRadius: 'var(--radius-sm)',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.375rem',
              }}
            >
              <BookOpen size={14} />
              <span>Description</span>
            </button>

            <button
              type="button"
              onClick={() => setActiveLeftTab('submissions')}
              style={{
                padding: '0.4rem 0.75rem',
                fontSize: '0.8125rem',
                fontWeight: 600,
                background: activeLeftTab === 'submissions' ? '#27272a' : 'transparent',
                color: activeLeftTab === 'submissions' ? '#ffffff' : 'var(--text-secondary)',
                border: 'none',
                borderRadius: 'var(--radius-sm)',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '0.375rem',
              }}
            >
              <History size={14} />
              <span>Submissions</span>
            </button>
          </div>

          {/* Left Pane Scrollable Body */}
          <div style={{ flex: 1, padding: '1.25rem', overflowY: 'auto' }}>
            {activeLeftTab === 'description' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', lineHeight: 1.6 }}>
                <div>
                  <h3 style={{ fontSize: '1.125rem', fontWeight: 600, marginBottom: '0.75rem', color: '#f4f4f5' }}>
                    Problem Statement
                  </h3>
                  <div
                    style={{ color: '#d4d4d8', fontSize: '0.875rem', whiteSpace: 'pre-line' }}
                  >
                    {problem.description_markdown}
                  </div>
                </div>

                {/* Example Test Cases */}
                {problem.visible_test_cases && problem.visible_test_cases.length > 0 && (
                  <div>
                    <h4 style={{ fontSize: '0.9375rem', fontWeight: 600, marginBottom: '0.5rem', color: '#f4f4f5' }}>
                      Examples
                    </h4>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                      {problem.visible_test_cases.map((tc, idx) => (
                        <div
                          key={tc.id || idx}
                          style={{
                            background: '#18181b',
                            border: '1px solid #27272a',
                            borderRadius: 'var(--radius-sm)',
                            padding: '0.75rem',
                            fontSize: '0.8125rem',
                          }}
                        >
                          <div style={{ fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                            Example {idx + 1}:
                          </div>
                          <div style={{ fontFamily: 'monospace', color: '#e4e4e7', marginBottom: '0.25rem' }}>
                            <strong style={{ color: 'var(--text-secondary)' }}>Input:</strong> {tc.input_data}
                          </div>
                          <div style={{ fontFamily: 'monospace', color: '#4ade80' }}>
                            <strong style={{ color: 'var(--text-secondary)' }}>Output:</strong> {tc.expected_output}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Constraints */}
                {problem.constraints_markdown && (
                  <div>
                    <h4 style={{ fontSize: '0.9375rem', fontWeight: 600, marginBottom: '0.5rem', color: '#f4f4f5' }}>
                      Constraints
                    </h4>
                    <div
                      style={{
                        background: '#18181b',
                        border: '1px solid #27272a',
                        borderRadius: 'var(--radius-sm)',
                        padding: '0.75rem',
                        fontSize: '0.8125rem',
                        color: '#a1a1aa',
                        whiteSpace: 'pre-line',
                      }}
                    >
                      {problem.constraints_markdown}
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeLeftTab === 'submissions' && (
              <div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
                  <h3 style={{ fontSize: '1rem', fontWeight: 600, margin: 0 }}>Submission History</h3>
                  {isAuthenticated && (
                    <button
                      type="button"
                      className="btn btn-secondary btn-sm"
                      onClick={loadHistory}
                      disabled={loadingHistory}
                      style={{ padding: '0.2rem 0.5rem', fontSize: '0.75rem' }}
                    >
                      <RefreshCw size={12} className={loadingHistory ? 'spinning' : ''} />
                      <span>Refresh</span>
                    </button>
                  )}
                </div>

                {!isAuthenticated ? (
                  <div className="card" style={{ textAlign: 'center', padding: '2rem 1rem' }}>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '1rem' }}>
                      Sign in to track your submission history and adaptive knowledge state.
                    </p>
                    <button
                      type="button"
                      className="btn btn-primary btn-sm"
                      onClick={() => onNavigateToAuth && onNavigateToAuth('login')}
                    >
                      Sign In
                    </button>
                  </div>
                ) : loadingHistory ? (
                  <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                    <RefreshCw size={18} className="spinning" style={{ marginRight: 6 }} />
                    <span>Loading submissions...</span>
                  </div>
                ) : submissionHistory.length === 0 ? (
                  <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                    No submissions recorded yet for this problem.
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    {submissionHistory.map((sub) => {
                      const isAccepted = sub.status === 'Accepted';
                      return (
                        <div
                          key={sub.id}
                          style={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            padding: '0.625rem 0.875rem',
                            borderRadius: 'var(--radius-sm)',
                            background: '#18181b',
                            border: `1px solid ${isAccepted ? 'rgba(74, 222, 128, 0.2)' : 'rgba(248, 113, 113, 0.2)'}`,
                            fontSize: '0.8125rem',
                          }}
                        >
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            {isAccepted ? (
                              <CheckCircle2 size={16} color="#4ade80" />
                            ) : (
                              <XCircle size={16} color="#f87171" />
                            )}
                            <span style={{ fontWeight: 600, color: isAccepted ? '#4ade80' : '#f87171' }}>
                              {sub.status}
                            </span>
                            <span className="badge" style={{ fontSize: '0.6875rem', padding: '0.1rem 0.35rem', background: '#27272a', color: '#38bdf8', textTransform: 'capitalize' }}>
                              {sub.language || 'python'}
                            </span>
                            <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>
                              ({sub.passed_test_cases}/{sub.total_test_cases})
                            </span>
                          </div>

                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: 'var(--text-secondary)', fontSize: '0.75rem' }}>
                            <span>{sub.execution_time_ms} ms</span>
                            <span>{new Date(sub.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* ================= RIGHT PANE ================= */}
        <div style={{ display: 'grid', gridTemplateRows: '58% 42%', gap: '0.75rem', height: '100%', minHeight: 0 }}>
          {/* Top: Monaco Code Editor */}
          <CodeEditor
            code={code}
            onChange={(val) => setCode(val || '')}
            onReset={handleResetCode}
            disabled={isRunning || isSubmitting}
            language={selectedLanguage}
            supportedLanguages={problem.supported_languages || ['python']}
            onLanguageChange={handleLanguageChange}
          />

          {/* Bottom: Test Case & Result Panel */}
          <TestCasePanel
            testCases={problem.visible_test_cases || []}
            executionResult={executionResult}
            activeTab={activeBottomTab}
            onTabChange={setActiveBottomTab}
            isRunning={isRunning}
            isSubmitting={isSubmitting}
            onNavigateToAuth={onNavigateToAuth}
            nextRecommendation={nextRecommendation}
            onSelectNextProblem={(slug) => onSelectProblem && onSelectProblem(slug)}
          />
        </div>
      </div>
    </div>
  );
}
