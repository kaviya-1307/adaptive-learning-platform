import React, { useState } from 'react';
import {
  CheckCircle2,
  XCircle,
  Clock,
  AlertTriangle,
  Terminal,
  Layers,
  Sparkles,
  ChevronRight,
  Code2
} from 'lucide-react';

export default function TestCasePanel({
  testCases = [],
  executionResult = null,
  activeTab = 'cases', // 'cases' | 'result'
  onTabChange,
  isRunning = false,
  isSubmitting = false,
  onNavigateToAuth,
  nextRecommendation = null,
  onSelectNextProblem,
}) {
  const [selectedCaseIdx, setSelectedCaseIdx] = useState(0);

  const results = executionResult?.results || [];
  const status = executionResult?.status;

  const getStatusBadge = (st) => {
    switch (st) {
      case 'Accepted':
      case 'Passed':
        return {
          color: '#4ade80',
          bg: 'rgba(74, 222, 128, 0.15)',
          border: 'rgba(74, 222, 128, 0.3)',
          icon: <CheckCircle2 size={16} color="#4ade80" />,
          label: 'Accepted',
        };
      case 'Wrong Answer':
        return {
          color: '#f87171',
          bg: 'rgba(248, 113, 113, 0.15)',
          border: 'rgba(248, 113, 113, 0.3)',
          icon: <XCircle size={16} color="#f87171" />,
          label: 'Wrong Answer',
        };
      case 'Time Limit Exceeded':
        return {
          color: '#fbbf24',
          bg: 'rgba(251, 191, 36, 0.15)',
          border: 'rgba(251, 191, 36, 0.3)',
          icon: <Clock size={16} color="#fbbf24" />,
          label: 'Time Limit Exceeded',
        };
      case 'Compilation Error':
        return {
          color: '#f43f5e',
          bg: 'rgba(244, 63, 94, 0.15)',
          border: 'rgba(244, 63, 94, 0.3)',
          icon: <AlertTriangle size={16} color="#f43f5e" />,
          label: 'Compilation Error',
        };
      case 'Authentication Required':
        return {
          color: '#fbbf24',
          bg: 'rgba(251, 191, 36, 0.15)',
          border: 'rgba(251, 191, 36, 0.3)',
          icon: <AlertTriangle size={16} color="#fbbf24" />,
          label: 'Authentication Required',
        };
      case 'Runtime Error':
      default:
        return {
          color: '#f87171',
          bg: 'rgba(248, 113, 113, 0.15)',
          border: 'rgba(248, 113, 113, 0.3)',
          icon: <AlertTriangle size={16} color="#f87171" />,
          label: st || 'Runtime Error',
        };
    }
  };

  const currentResultCase = results[selectedCaseIdx];
  const currentStaticCase = testCases[selectedCaseIdx];

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        background: '#18181b',
        border: '1px solid var(--border-color)',
        borderRadius: 'var(--radius-md)',
        overflow: 'hidden',
      }}
    >
      {/* Top Header Tabs */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0.375rem 0.75rem',
          background: '#202023',
          borderBottom: '1px solid var(--border-color)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <button
            type="button"
            className={`btn-tab ${activeTab === 'cases' ? 'active' : ''}`}
            onClick={() => onTabChange('cases')}
            style={{
              padding: '0.35rem 0.75rem',
              fontSize: '0.8125rem',
              fontWeight: 600,
              background: activeTab === 'cases' ? '#27272a' : 'transparent',
              color: activeTab === 'cases' ? '#ffffff' : 'var(--text-secondary)',
              border: 'none',
              borderRadius: 'var(--radius-sm)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.375rem',
            }}
          >
            <Layers size={14} />
            <span>Test Cases ({testCases.length})</span>
          </button>

          <button
            type="button"
            className={`btn-tab ${activeTab === 'result' ? 'active' : ''}`}
            onClick={() => onTabChange('result')}
            style={{
              padding: '0.35rem 0.75rem',
              fontSize: '0.8125rem',
              fontWeight: 600,
              background: activeTab === 'result' ? '#27272a' : 'transparent',
              color: activeTab === 'result' ? '#ffffff' : 'var(--text-secondary)',
              border: 'none',
              borderRadius: 'var(--radius-sm)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.375rem',
            }}
          >
            <Terminal size={14} />
            <span>Test Result</span>
            {executionResult && (
              <span
                style={{
                  display: 'inline-block',
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  backgroundColor: status === 'Accepted' ? '#4ade80' : '#f87171',
                }}
              />
            )}
          </button>
        </div>

        {(isRunning || isSubmitting) && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', fontSize: '0.75rem', color: '#60a5fa' }}>
            <span className="spinner-inline" />
            <span>{isSubmitting ? 'Submitting & Evaluating...' : 'Running Code...'}</span>
          </div>
        )}
      </div>

      {/* Main Panel Content */}
      <div style={{ flex: 1, padding: '0.75rem 1rem', overflowY: 'auto' }}>
        {/* ================= MODE: TEST CASES ================= */}
        {activeTab === 'cases' && (
          <div>
            {/* Case Selector Pills */}
            <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
              {testCases.map((tc, idx) => (
                <button
                  key={tc.id || idx}
                  type="button"
                  onClick={() => setSelectedCaseIdx(idx)}
                  style={{
                    padding: '0.35rem 0.75rem',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid',
                    borderColor: selectedCaseIdx === idx ? 'var(--accent-primary)' : '#333338',
                    background: selectedCaseIdx === idx ? 'rgba(59, 130, 246, 0.15)' : '#222226',
                    color: selectedCaseIdx === idx ? '#93c5fd' : '#a1a1aa',
                    cursor: 'pointer',
                  }}
                >
                  Case {idx + 1}
                </button>
              ))}
            </div>

            {currentStaticCase ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.8125rem' }}>
                <div>
                  <div style={{ color: 'var(--text-secondary)', marginBottom: '0.25rem', fontSize: '0.75rem', fontWeight: 600 }}>
                    INPUT
                  </div>
                  <pre
                    style={{
                      background: '#121214',
                      padding: '0.625rem 0.75rem',
                      borderRadius: 'var(--radius-sm)',
                      border: '1px solid #27272a',
                      color: '#e4e4e7',
                      fontFamily: 'monospace',
                      whiteSpace: 'pre-wrap',
                      margin: 0,
                    }}
                  >
                    {currentStaticCase.input_data}
                  </pre>
                </div>

                <div>
                  <div style={{ color: 'var(--text-secondary)', marginBottom: '0.25rem', fontSize: '0.75rem', fontWeight: 600 }}>
                    EXPECTED OUTPUT
                  </div>
                  <pre
                    style={{
                      background: '#121214',
                      padding: '0.625rem 0.75rem',
                      borderRadius: 'var(--radius-sm)',
                      border: '1px solid #27272a',
                      color: '#4ade80',
                      fontFamily: 'monospace',
                      whiteSpace: 'pre-wrap',
                      margin: 0,
                    }}
                  >
                    {currentStaticCase.expected_output}
                  </pre>
                </div>
              </div>
            ) : (
              <div style={{ color: 'var(--text-muted)', fontSize: '0.8125rem' }}>No test cases loaded.</div>
            )}
          </div>
        )}

        {/* ================= MODE: TEST RESULT ================= */}
        {activeTab === 'result' && (
          <div>
            {!executionResult && !isRunning && !isSubmitting && (
              <div
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  padding: '2rem 1rem',
                  color: 'var(--text-muted)',
                  textAlign: 'center',
                  gap: '0.5rem',
                }}
              >
                <Code2 size={28} />
                <p style={{ margin: 0, fontSize: '0.875rem' }}>
                  Click <strong>Run Code</strong> or <strong>Submit</strong> to evaluate your solution.
                </p>
              </div>
            )}

            {executionResult && (
              <div>
                {/* Result Status Banner */}
                {(() => {
                  const badge = getStatusBadge(status);
                  return (
                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        padding: '0.75rem 1rem',
                        borderRadius: 'var(--radius-md)',
                        background: badge.bg,
                        border: `1px solid ${badge.border}`,
                        marginBottom: '1rem',
                        flexWrap: 'wrap',
                        gap: '0.5rem',
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        {badge.icon}
                        <span style={{ fontSize: '1rem', fontWeight: 700, color: badge.color }}>
                          {badge.label}
                        </span>
                      </div>

                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem', fontSize: '0.8125rem' }}>
                        <span style={{ color: 'var(--text-secondary)' }}>
                          Passed: <strong style={{ color: '#fff' }}>{executionResult.passed_test_cases}/{executionResult.total_test_cases}</strong>
                        </span>
                        <span style={{ color: 'var(--text-secondary)' }}>
                          Runtime: <strong style={{ color: '#60a5fa' }}>{executionResult.execution_time_ms} ms</strong>
                        </span>
                      </div>
                    </div>
                  );
                })()}

                {/* Next Recommended Problem Callout after Submission Evaluation */}
                {nextRecommendation?.problem && (
                  <div
                    style={{
                      background: status === 'Accepted'
                        ? 'linear-gradient(135deg, rgba(37, 99, 235, 0.12) 0%, rgba(139, 92, 246, 0.12) 100%)'
                        : 'linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(168, 85, 247, 0.08) 100%)',
                      border: status === 'Accepted'
                        ? '1px solid rgba(99, 102, 241, 0.4)'
                        : '1px solid rgba(239, 68, 68, 0.3)',
                      borderRadius: 'var(--radius-md)',
                      padding: '0.85rem 1rem',
                      marginBottom: '1rem',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      flexWrap: 'wrap',
                      gap: '0.75rem',
                    }}
                  >
                    <div style={{ flex: 1, minWidth: '220px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                        <span className="badge badge-purple" style={{ fontSize: '0.7rem' }}>
                          {status === 'Accepted' ? 'Next Recommended Problem (ZPD)' : 'Targeted Practice Recommendation'}
                        </span>
                        <span className="badge badge-blue" style={{ fontSize: '0.7rem' }}>{nextRecommendation.problem.difficulty}</span>
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{nextRecommendation.problem.topic_name}</span>
                      </div>
                      <div style={{ fontWeight: 600, color: '#ffffff', fontSize: '0.9rem' }}>
                        {nextRecommendation.problem.id}. {nextRecommendation.problem.title}
                      </div>
                      <p style={{ margin: '0.2rem 0 0', fontSize: '0.75rem', color: '#cbd5e1', lineHeight: 1.4 }}>
                        {nextRecommendation.explanation_text}
                      </p>
                    </div>

                    <button
                      type="button"
                      className="btn btn-primary btn-sm"
                      onClick={() => onSelectNextProblem && onSelectNextProblem(nextRecommendation.problem.slug)}
                      style={{ fontWeight: 600, whiteSpace: 'nowrap' }}
                    >
                      <span>{status === 'Accepted' ? 'Solve Next Problem' : 'Practice Target Concept'}</span>
                      <ChevronRight size={14} />
                    </button>
                  </div>
                )}

                {/* Compilation / Auth Error Output */}
                {executionResult.compile_error && (
                  <div style={{ marginBottom: '1rem' }}>
                    <div style={{ color: executionResult.authRequired ? '#fbbf24' : '#f87171', fontSize: '0.75rem', fontWeight: 600, marginBottom: '0.25rem' }}>
                      {executionResult.authRequired ? 'AUTHENTICATION NOTICE' : 'ERROR TRACEBACK'}
                    </div>
                    <pre
                      style={{
                        background: executionResult.authRequired ? 'rgba(251, 191, 36, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                        padding: '0.75rem',
                        borderRadius: 'var(--radius-sm)',
                        border: `1px solid ${executionResult.authRequired ? 'rgba(251, 191, 36, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
                        color: executionResult.authRequired ? '#fde68a' : '#fca5a5',
                        fontFamily: 'monospace',
                        fontSize: '0.8125rem',
                        whiteSpace: 'pre-wrap',
                        margin: 0,
                      }}
                    >
                      {executionResult.compile_error}
                    </pre>

                    {executionResult.authRequired && onNavigateToAuth && (
                      <div style={{ marginTop: '0.75rem' }}>
                        <button
                          type="button"
                          className="btn btn-primary btn-sm"
                          onClick={() => onNavigateToAuth('login')}
                        >
                          Sign In to Your Account
                        </button>
                      </div>
                    )}
                  </div>
                )}

                {/* Case Selector Pills for Results */}
                {results.length > 0 && (
                  <div>
                    <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.875rem', flexWrap: 'wrap' }}>
                      {results.map((r, idx) => {
                        const isPassed = r.status === 'Passed';
                        const isSelected = selectedCaseIdx === idx;
                        return (
                          <button
                            key={r.test_case_id || idx}
                            type="button"
                            onClick={() => setSelectedCaseIdx(idx)}
                            style={{
                              padding: '0.35rem 0.65rem',
                              fontSize: '0.75rem',
                              fontWeight: 600,
                              borderRadius: 'var(--radius-sm)',
                              border: '1px solid',
                              borderColor: isSelected
                                ? 'var(--accent-primary)'
                                : isPassed
                                ? 'rgba(74, 222, 128, 0.3)'
                                : 'rgba(248, 113, 113, 0.3)',
                              background: isSelected
                                ? 'rgba(59, 130, 246, 0.2)'
                                : isPassed
                                ? 'rgba(74, 222, 128, 0.08)'
                                : 'rgba(248, 113, 113, 0.08)',
                              color: isPassed ? '#4ade80' : '#f87171',
                              cursor: 'pointer',
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '0.3rem',
                            }}
                          >
                            <span>Case {idx + 1}</span>
                            {isPassed ? (
                              <CheckCircle2 size={12} color="#4ade80" />
                            ) : (
                              <XCircle size={12} color="#f87171" />
                            )}
                          </button>
                        );
                      })}
                    </div>

                    {currentResultCase && (
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.8125rem' }}>
                        {/* Input */}
                        <div>
                          <div style={{ color: 'var(--text-secondary)', marginBottom: '0.25rem', fontSize: '0.75rem', fontWeight: 600 }}>
                            INPUT
                          </div>
                          <pre
                            style={{
                              background: '#121214',
                              padding: '0.625rem 0.75rem',
                              borderRadius: 'var(--radius-sm)',
                              border: '1px solid #27272a',
                              color: '#e4e4e7',
                              fontFamily: 'monospace',
                              whiteSpace: 'pre-wrap',
                              margin: 0,
                            }}
                          >
                            {currentResultCase.input_data}
                          </pre>
                        </div>

                        {/* Actual Output */}
                        <div>
                          <div style={{ color: 'var(--text-secondary)', marginBottom: '0.25rem', fontSize: '0.75rem', fontWeight: 600 }}>
                            YOUR OUTPUT
                          </div>
                          <pre
                            style={{
                              background: '#121214',
                              padding: '0.625rem 0.75rem',
                              borderRadius: 'var(--radius-sm)',
                              border: '1px solid #27272a',
                              color: currentResultCase.status === 'Passed' ? '#4ade80' : '#f87171',
                              fontFamily: 'monospace',
                              whiteSpace: 'pre-wrap',
                              margin: 0,
                            }}
                          >
                            {currentResultCase.actual_output}
                          </pre>
                        </div>

                        {/* Expected Output */}
                        <div>
                          <div style={{ color: 'var(--text-secondary)', marginBottom: '0.25rem', fontSize: '0.75rem', fontWeight: 600 }}>
                            EXPECTED OUTPUT
                          </div>
                          <pre
                            style={{
                              background: '#121214',
                              padding: '0.625rem 0.75rem',
                              borderRadius: 'var(--radius-sm)',
                              border: '1px solid #27272a',
                              color: '#4ade80',
                              fontFamily: 'monospace',
                              whiteSpace: 'pre-wrap',
                              margin: 0,
                            }}
                          >
                            {currentResultCase.expected_output}
                          </pre>
                        </div>

                        {/* Console Stdout if any */}
                        {currentResultCase.stdout && (
                          <div>
                            <div style={{ color: '#38bdf8', marginBottom: '0.25rem', fontSize: '0.75rem', fontWeight: 600 }}>
                              CONSOLE OUTPUT (STDOUT)
                            </div>
                            <pre
                              style={{
                                background: '#090d16',
                                padding: '0.625rem 0.75rem',
                                borderRadius: 'var(--radius-sm)',
                                border: '1px solid rgba(56, 189, 248, 0.3)',
                                color: '#bae6fd',
                                fontFamily: 'monospace',
                                whiteSpace: 'pre-wrap',
                                margin: 0,
                              }}
                            >
                              {currentResultCase.stdout}
                            </pre>
                          </div>
                        )}

                        {/* Error traceback if any */}
                        {currentResultCase.error_message && (
                          <div>
                            <div style={{ color: '#f87171', marginBottom: '0.25rem', fontSize: '0.75rem', fontWeight: 600 }}>
                              RUNTIME ERROR
                            </div>
                            <pre
                              style={{
                                background: 'rgba(239, 68, 68, 0.1)',
                                padding: '0.625rem 0.75rem',
                                borderRadius: 'var(--radius-sm)',
                                border: '1px solid rgba(239, 68, 68, 0.3)',
                                color: '#fca5a5',
                                fontFamily: 'monospace',
                                whiteSpace: 'pre-wrap',
                                margin: 0,
                              }}
                            >
                              {currentResultCase.error_message}
                            </pre>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
