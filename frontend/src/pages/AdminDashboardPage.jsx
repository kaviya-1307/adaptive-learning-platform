import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  Users,
  CheckCircle2,
  AlertCircle,
  Clock,
  Download,
  Search,
  Filter,
  RefreshCw,
  FileText,
  Activity,
  Award,
  Code2,
  X,
  BrainCircuit,
  BarChart3,
  Layers,
  ChevronRight
} from 'lucide-react';
import {
  fetchAdminOverview,
  fetchAdminUsers,
  fetchAdminUserDetail,
  exportAdminDataset
} from '../services/api';

export default function AdminDashboardPage({ onNavigate }) {
  const [overview, setOverview] = useState(null);
  const [students, setStudents] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loadingOverview, setLoadingOverview] = useState(true);
  const [loadingStudents, setLoadingStudents] = useState(true);
  const [error, setError] = useState(null);

  // Search & Filter state
  const [searchQuery, setSearchQuery] = useState('');
  const [diagnosticFilter, setDiagnosticFilter] = useState('all');

  // Selected student for detailed inspection
  const [selectedStudentId, setSelectedStudentId] = useState(null);
  const [studentDetail, setStudentDetail] = useState(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [detailError, setDetailError] = useState(null);

  // Export state
  const [exportingFormat, setExportingFormat] = useState(null); // 'json' | 'csv' | null
  const [exportMessage, setExportMessage] = useState(null);

  const loadOverview = async () => {
    setLoadingOverview(true);
    try {
      const data = await fetchAdminOverview();
      setOverview(data);
    } catch (err) {
      console.error('Failed to load admin overview:', err);
      setError(err.response?.data?.detail || 'Failed to load platform overview metrics.');
    } finally {
      setLoadingOverview(false);
    }
  };

  const loadStudents = async () => {
    setLoadingStudents(true);
    try {
      const params = {};
      if (searchQuery.trim()) params.search = searchQuery.trim();
      if (diagnosticFilter !== 'all') params.diagnostic_filter = diagnosticFilter;
      const res = await fetchAdminUsers(params);
      setStudents(res.students || []);
      setTotalCount(res.total_count || 0);
    } catch (err) {
      console.error('Failed to load students:', err);
      setError(err.response?.data?.detail || 'Failed to load student monitoring records.');
    } finally {
      setLoadingStudents(false);
    }
  };

  useEffect(() => {
    loadOverview();
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      loadStudents();
    }, 300);
    return () => clearTimeout(timer);
  }, [searchQuery, diagnosticFilter]);

  const handleInspectStudent = async (studentId) => {
    setSelectedStudentId(studentId);
    setLoadingDetail(true);
    setDetailError(null);
    try {
      const detail = await fetchAdminUserDetail(studentId);
      setStudentDetail(detail);
    } catch (err) {
      console.error('Failed to load student detail:', err);
      setDetailError(err.response?.data?.detail || 'Failed to inspect student record.');
    } finally {
      setLoadingDetail(false);
    }
  };

  const closeInspectionModal = () => {
    setSelectedStudentId(null);
    setStudentDetail(null);
    setDetailError(null);
  };

  const handleExport = async (format) => {
    setExportingFormat(format);
    setExportMessage(null);
    try {
      const data = await exportAdminDataset(format);
      if (format === 'csv') {
        const blob = new Blob([data], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `adaptive_learning_live_dataset_${Date.now()}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      } else {
        const jsonStr = JSON.stringify(data, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `adaptive_learning_live_dataset_${Date.now()}.json`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      }
      setExportMessage({ type: 'success', text: `Successfully exported live dataset in ${format.toUpperCase()} format!` });
      setTimeout(() => setExportMessage(null), 4000);
    } catch (err) {
      console.error('Export failed:', err);
      setExportMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to export live dataset.' });
    } finally {
      setExportingFormat(null);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem', paddingBottom: '3rem' }}>
      {/* 1. Header Banner */}
      <div
        className="card"
        style={{
          padding: '1.75rem 2rem',
          background: 'linear-gradient(135deg, #18181b 0%, #1f1d2b 50%, #27272a 100%)',
          border: '1px solid rgba(168, 85, 247, 0.3)',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.35)'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1.25rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <span className="badge badge-purple" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', fontWeight: 600 }}>
                <ShieldCheck size={14} color="#a855f7" /> Faculty &amp; Administrative Monitoring
              </span>
              <span className="badge badge-blue">Phase 5 Live Dataset</span>
            </div>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800, margin: '0 0 0.35rem', color: '#ffffff' }}>
              Live Student Dataset &amp; Performance Monitoring
            </h1>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem', margin: 0, maxWidth: '750px' }}>
              Aggregated administrative view of genuine student platform activity persisted in MySQL.
              Inspect diagnostic results, code submissions, topic mastery, and download research-grade datasets.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '0.65rem', alignItems: 'center', flexWrap: 'wrap' }}>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={() => handleExport('json')}
              disabled={Boolean(exportingFormat)}
              style={{ fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '0.4rem' }}
              title="Download sanitized live student dataset as JSON for evaluation/research"
            >
              <Download size={14} />
              <span>{exportingFormat === 'json' ? 'Exporting...' : 'Export Dataset (JSON)'}</span>
            </button>
            <button
              type="button"
              className="btn btn-primary btn-sm"
              onClick={() => handleExport('csv')}
              disabled={Boolean(exportingFormat)}
              style={{ fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '0.4rem' }}
              title="Download sanitized live student dataset as CSV for spreadsheet analysis"
            >
              <Download size={14} />
              <span>{exportingFormat === 'csv' ? 'Exporting...' : 'Export Dataset (CSV)'}</span>
            </button>
          </div>
        </div>

        {/* Export Notification Toast */}
        {exportMessage && (
          <div
            style={{
              marginTop: '1rem',
              padding: '0.65rem 1rem',
              borderRadius: '8px',
              fontSize: '0.85rem',
              background: exportMessage.type === 'success' ? 'rgba(34, 197, 94, 0.15)' : 'rgba(239, 68, 68, 0.15)',
              border: `1px solid ${exportMessage.type === 'success' ? '#22c55e' : '#ef4444'}`,
              color: exportMessage.type === 'success' ? '#86efac' : '#fca5a5'
            }}
          >
            {exportMessage.text}
          </div>
        )}
      </div>

      {/* 2. Platform Overview Metric Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
        <div className="card" style={{ padding: '1.25rem', border: '1px solid rgba(255,255,255,0.06)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.8rem', marginBottom: '0.35rem' }}>
            <Users size={15} color="#3b82f6" /> Total Registered
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#ffffff' }}>
            {loadingOverview ? '...' : (overview?.total_registered_students ?? 0)}
          </div>
          <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            Active student accounts
          </div>
        </div>

        <div className="card" style={{ padding: '1.25rem', border: '1px solid rgba(255,255,255,0.06)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.8rem', marginBottom: '0.35rem' }}>
            <Award size={15} color="#10b981" /> Onboarding Done
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#10b981' }}>
            {loadingOverview ? '...' : (overview?.onboarding_completed_count ?? 0)}
          </div>
          <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            Configured learning goals
          </div>
        </div>

        <div className="card" style={{ padding: '1.25rem', border: '1px solid rgba(255,255,255,0.06)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.8rem', marginBottom: '0.35rem' }}>
            <CheckCircle2 size={15} color="#a855f7" /> Diagnostic Done
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#a855f7' }}>
            {loadingOverview ? '...' : (overview?.diagnostic_completed_count ?? 0)}
          </div>
          <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            Completed 7-problem test
          </div>
        </div>

        <div className="card" style={{ padding: '1.25rem', border: '1px solid rgba(255,255,255,0.06)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.8rem', marginBottom: '0.35rem' }}>
            <Code2 size={15} color="#f59e0b" /> Total Submissions
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#ffffff' }}>
            {loadingOverview ? '...' : (overview?.total_submissions_count ?? 0)}
          </div>
          <div style={{ fontSize: '0.72rem', color: '#10b981', marginTop: '0.2rem' }}>
            {loadingOverview ? '...' : `${overview?.total_solved_submissions_count ?? 0} Accepted`}
          </div>
        </div>

        <div className="card" style={{ padding: '1.25rem', border: '1px solid rgba(255,255,255,0.06)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.8rem', marginBottom: '0.35rem' }}>
            <Activity size={15} color="#06b6d4" /> Active Students
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#06b6d4' }}>
            {loadingOverview ? '...' : (overview?.active_students_count ?? 0)}
          </div>
          <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            Interacted with practice/diagnostic
          </div>
        </div>

        <div className="card" style={{ padding: '1.25rem', border: '1px solid rgba(255,255,255,0.06)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.8rem', marginBottom: '0.35rem' }}>
            <BrainCircuit size={15} color="#ec4899" /> Recommendations
          </div>
          <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#ffffff' }}>
            {loadingOverview ? '...' : (overview?.total_recommendations_count ?? 0)}
          </div>
          <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            Generated by ML pipeline
          </div>
        </div>
      </div>

      {/* 3. Student Monitoring Table Section */}
      <div className="card" style={{ padding: '1.5rem', border: '1px solid rgba(255, 255, 255, 0.08)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.25rem' }}>
          <div>
            <h3 style={{ margin: '0 0 0.25rem', fontSize: '1.15rem', color: '#ffffff' }}>
              Live Student Directory ({totalCount} Registered Learners)
            </h3>
            <p style={{ margin: 0, fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
              Real-world student performance records. Email addresses are visible solely to administrators for course grading and evaluation.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', flexWrap: 'wrap' }}>
            {/* Search Input */}
            <div style={{ position: 'relative' }}>
              <Search size={14} color="var(--text-muted)" style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)' }} />
              <input
                type="text"
                className="input-field"
                placeholder="Search name or email..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                style={{ paddingLeft: '2.2rem', minWidth: '220px', fontSize: '0.85rem', height: '36px' }}
              />
            </div>

            {/* Diagnostic Filter Dropdown */}
            <select
              className="input-field"
              value={diagnosticFilter}
              onChange={(e) => setDiagnosticFilter(e.target.value)}
              style={{ height: '36px', fontSize: '0.85rem', minWidth: '150px' }}
            >
              <option value="all">All Diagnostic States</option>
              <option value="completed">Diagnostic Completed</option>
              <option value="pending">Diagnostic Pending</option>
            </select>

            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={() => { loadOverview(); loadStudents(); }}
              title="Refresh student records"
              style={{ height: '36px', display: 'inline-flex', alignItems: 'center', gap: '0.35rem' }}
            >
              <RefreshCw size={14} className={loadingStudents ? 'spinning' : ''} />
              <span>Refresh</span>
            </button>
          </div>
        </div>

        {/* Table */}
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.86rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.1)', color: 'var(--text-muted)', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                <th style={{ padding: '0.75rem 1rem' }}>Student</th>
                <th style={{ padding: '0.75rem 1rem' }}>Email Address</th>
                <th style={{ padding: '0.75rem 1rem' }}>Onboarding</th>
                <th style={{ padding: '0.75rem 1rem' }}>Diagnostic</th>
                <th style={{ padding: '0.75rem 1rem' }}>Problems Solved</th>
                <th style={{ padding: '0.75rem 1rem' }}>Submissions</th>
                <th style={{ padding: '0.75rem 1rem' }}>Last Activity</th>
                <th style={{ padding: '0.75rem 1rem', textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {loadingStudents ? (
                <tr>
                  <td colSpan="8" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
                    <RefreshCw size={24} className="spinning" style={{ margin: '0 auto 0.5rem', color: 'var(--accent-primary)' }} />
                    <div>Loading live student dataset...</div>
                  </td>
                </tr>
              ) : students.length === 0 ? (
                <tr>
                  <td colSpan="8" style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
                    No students found matching your criteria.
                  </td>
                </tr>
              ) : (
                students.map((st) => (
                  <tr
                    key={st.id}
                    style={{
                      borderBottom: '1px solid rgba(255, 255, 255, 0.05)',
                      transition: 'background 0.15s ease'
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.02)'}
                    onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
                  >
                    <td style={{ padding: '0.85rem 1rem', fontWeight: 600, color: '#f4f4f5' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <div style={{ width: '28px', height: '28px', borderRadius: '50%', background: 'rgba(168, 85, 247, 0.2)', color: '#c084fc', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', fontWeight: 700 }}>
                          {st.name ? st.name.charAt(0).toUpperCase() : 'S'}
                        </div>
                        <div>
                          <div>{st.name || 'Unnamed Student'}</div>
                          <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>ID #{st.id}</div>
                        </div>
                      </div>
                    </td>

                    <td style={{ padding: '0.85rem 1rem', color: 'var(--text-secondary)', fontFamily: 'monospace', fontSize: '0.82rem' }}>
                      {st.email}
                    </td>

                    <td style={{ padding: '0.85rem 1rem' }}>
                      {st.onboarding_completed ? (
                        <span className="badge badge-green" style={{ fontSize: '0.72rem' }}>
                          {st.experience_level ? st.experience_level.toUpperCase() : 'ONBOARDED'}
                        </span>
                      ) : (
                        <span className="badge badge-yellow" style={{ fontSize: '0.72rem' }}>Pending</span>
                      )}
                    </td>

                    <td style={{ padding: '0.85rem 1rem' }}>
                      {st.diagnostic_completed ? (
                        <span className="badge badge-purple" style={{ fontSize: '0.72rem', display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
                          <CheckCircle2 size={11} color="#10b981" />
                          {st.diagnostic_score !== null ? `${st.diagnostic_score}/${st.diagnostic_total ?? 7}` : 'Completed'}
                        </span>
                      ) : (
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Not completed</span>
                      )}
                    </td>

                    <td style={{ padding: '0.85rem 1rem', fontWeight: 600, color: st.solved_problems_count > 0 ? '#10b981' : 'var(--text-secondary)' }}>
                      {st.solved_problems_count} solved
                    </td>

                    <td style={{ padding: '0.85rem 1rem', color: 'var(--text-secondary)' }}>
                      {st.total_submissions} attempts
                    </td>

                    <td style={{ padding: '0.85rem 1rem', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                      {st.last_activity_at ? new Date(st.last_activity_at).toLocaleDateString() : '—'}
                    </td>

                    <td style={{ padding: '0.85rem 1rem', textAlign: 'right' }}>
                      <button
                        type="button"
                        className="btn btn-secondary btn-sm"
                        onClick={() => handleInspectStudent(st.id)}
                        style={{ fontSize: '0.78rem', padding: '0.35rem 0.75rem', display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}
                      >
                        <span>Inspect</span>
                        <ChevronRight size={13} />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* 4. Student Detail Inspection Modal */}
      {selectedStudentId && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0, 0, 0, 0.75)',
            backdropFilter: 'blur(4px)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            padding: '1.5rem'
          }}
          onClick={closeInspectionModal}
        >
          <div
            className="card"
            style={{
              width: '100%',
              maxWidth: '850px',
              maxHeight: '90vh',
              overflowY: 'auto',
              background: '#18181b',
              border: '1px solid rgba(168, 85, 247, 0.35)',
              boxShadow: '0 20px 50px rgba(0, 0, 0, 0.7)',
              padding: '2rem'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '1rem', marginBottom: '1.5rem' }}>
              <div>
                <span className="badge badge-purple" style={{ marginBottom: '0.4rem', display: 'inline-block' }}>
                  Student Learning Inspection
                </span>
                <h2 style={{ margin: 0, color: '#ffffff', fontSize: '1.4rem' }}>
                  {studentDetail?.name || `Student #${selectedStudentId}`}
                </h2>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
                  Email: <span style={{ color: '#c084fc', fontFamily: 'monospace' }}>{studentDetail?.email}</span> • Registered on {studentDetail?.created_at ? new Date(studentDetail.created_at).toLocaleDateString() : '—'}
                </div>
              </div>

              <button
                type="button"
                className="btn btn-secondary btn-sm"
                onClick={closeInspectionModal}
                style={{ padding: '0.4rem' }}
              >
                <X size={18} />
              </button>
            </div>

            {loadingDetail ? (
              <div style={{ textAlign: 'center', padding: '4rem 0', color: 'var(--text-secondary)' }}>
                <RefreshCw size={32} className="spinning" style={{ margin: '0 auto 1rem', color: 'var(--accent-primary)' }} />
                <h3>Loading Student Performance History...</h3>
              </div>
            ) : detailError ? (
              <div style={{ padding: '1.5rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', borderRadius: '8px', color: '#fca5a5' }}>
                {detailError}
              </div>
            ) : studentDetail ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                {/* Highlights Row */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))', gap: '0.75rem' }}>
                  <div style={{ padding: '0.85rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.06)' }}>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Learning Goal</div>
                    <div style={{ fontWeight: 600, color: '#f4f4f5', marginTop: '0.2rem', textTransform: 'capitalize' }}>
                      {studentDetail.learning_goal ? studentDetail.learning_goal.replace('_', ' ') : 'Not set'}
                    </div>
                  </div>

                  <div style={{ padding: '0.85rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.06)' }}>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Diagnostic Score</div>
                    <div style={{ fontWeight: 700, color: '#a855f7', marginTop: '0.2rem' }}>
                      {studentDetail.diagnostic_completed ? `${studentDetail.diagnostic_score} / ${studentDetail.diagnostic_total} Solved` : 'Incomplete'}
                    </div>
                  </div>

                  <div style={{ padding: '0.85rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.06)' }}>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Total Submissions</div>
                    <div style={{ fontWeight: 700, color: '#ffffff', marginTop: '0.2rem' }}>
                      {studentDetail.total_submissions} ({studentDetail.solved_problems_count} Accepted)
                    </div>
                  </div>

                  <div style={{ padding: '0.85rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.06)' }}>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Last Active</div>
                    <div style={{ fontWeight: 600, color: '#f4f4f5', marginTop: '0.2rem' }}>
                      {studentDetail.last_activity_at ? new Date(studentDetail.last_activity_at).toLocaleString() : '—'}
                    </div>
                  </div>
                </div>

                {/* 10-Topic Mastery Breakdown */}
                {studentDetail.topic_mastery && studentDetail.topic_mastery.length > 0 && (
                  <div>
                    <h4 style={{ margin: '0 0 0.75rem', fontSize: '0.95rem', color: '#f4f4f5', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                      <BrainCircuit size={15} color="#a855f7" /> 10-Topic Concept Mastery State
                    </h4>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '0.65rem' }}>
                      {studentDetail.topic_mastery.map((tm) => (
                        <div key={tm.topic_id} style={{ padding: '0.75rem', background: 'rgba(255,255,255,0.02)', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.05)' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '0.35rem' }}>
                            <span style={{ color: '#f4f4f5', fontWeight: 500 }}>{tm.topic_name}</span>
                            <span style={{ color: '#a855f7', fontWeight: 700 }}>{Math.round(tm.mastery_score * 100)}%</span>
                          </div>
                          <div style={{ width: '100%', height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                            <div style={{ width: `${Math.round(tm.mastery_score * 100)}%`, height: '100%', background: 'linear-gradient(90deg, #8b5cf6, #ec4899)', borderRadius: '3px' }} />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Recent Submissions */}
                {studentDetail.recent_submissions && studentDetail.recent_submissions.length > 0 && (
                  <div>
                    <h4 style={{ margin: '0 0 0.75rem', fontSize: '0.95rem', color: '#f4f4f5', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                      <Code2 size={15} color="#3b82f6" /> Recent Coding Submissions
                    </h4>
                    <div style={{ border: '1px solid rgba(255,255,255,0.08)', borderRadius: '6px', overflow: 'hidden' }}>
                      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem', textAlign: 'left' }}>
                        <thead>
                          <tr style={{ background: 'rgba(255,255,255,0.03)', borderBottom: '1px solid rgba(255,255,255,0.08)', color: 'var(--text-muted)' }}>
                            <th style={{ padding: '0.55rem 0.85rem' }}>Problem</th>
                            <th style={{ padding: '0.55rem 0.85rem' }}>Language</th>
                            <th style={{ padding: '0.55rem 0.85rem' }}>Status</th>
                            <th style={{ padding: '0.55rem 0.85rem' }}>Tests Passed</th>
                            <th style={{ padding: '0.55rem 0.85rem' }}>Time</th>
                          </tr>
                        </thead>
                        <tbody>
                          {studentDetail.recent_submissions.map((sub) => (
                            <tr key={sub.submission_id} style={{ borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
                              <td style={{ padding: '0.55rem 0.85rem', color: '#ffffff', fontWeight: 500 }}>{sub.problem_title}</td>
                              <td style={{ padding: '0.55rem 0.85rem', textTransform: 'capitalize', color: 'var(--text-secondary)' }}>{sub.language}</td>
                              <td style={{ padding: '0.55rem 0.85rem' }}>
                                <span className={sub.status === 'Accepted' ? 'badge badge-green' : 'badge badge-red'} style={{ fontSize: '0.7rem' }}>
                                  {sub.status}
                                </span>
                              </td>
                              <td style={{ padding: '0.55rem 0.85rem', color: 'var(--text-muted)' }}>{sub.passed_test_cases}/{sub.total_test_cases}</td>
                              <td style={{ padding: '0.55rem 0.85rem', color: 'var(--text-muted)', fontSize: '0.75rem' }}>
                                {new Date(sub.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            ) : null}
          </div>
        </div>
      )}
    </div>
  );
}
