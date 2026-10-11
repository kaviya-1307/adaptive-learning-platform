import React from 'react';
import { Terminal, LogOut, User, Sparkles, CheckCircle2, ShieldCheck } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Navbar({ currentView, onNavigate }) {
  const { user, isAuthenticated, logout } = useAuth();
  const isDiagnosticDone = Boolean(
    user?.diagnostic_completed || user?.diagnostic_exempt || user?.role === 'ADMIN'
  );

  return (
    <nav className="navbar">
      <div
        className="nav-brand"
        onClick={() => onNavigate(isAuthenticated ? (isDiagnosticDone ? 'dashboard' : 'diagnostic') : 'login')}
        style={{ cursor: 'pointer' }}
      >
        <div className="brand-icon">
          <Terminal size={18} />
        </div>
        <span>Adaptive Learning Framework</span>
        <span className="badge badge-purple" style={{ marginLeft: '0.5rem' }}>
          AI-Driven DSA
        </span>
      </div>

      <div className="nav-links">
        {isAuthenticated && (
          <>
            {isDiagnosticDone ? (
              <>
                <button
                  type="button"
                  className={`nav-item ${currentView === 'dashboard' ? 'active' : ''}`}
                  onClick={() => onNavigate('dashboard')}
                >
                  Dashboard
                </button>

                <button
                  type="button"
                  className={`nav-item ${currentView === 'roadmap' ? 'active' : ''}`}
                  onClick={() => onNavigate('roadmap')}
                >
                  Roadmap
                </button>

                <button
                  type="button"
                  className={`nav-item ${currentView === 'problems' || currentView === 'workspace' ? 'active' : ''}`}
                  onClick={() => onNavigate('problems')}
                >
                  Problems
                </button>

                {user?.diagnostic_completed && (
                  <button
                    type="button"
                    className={`nav-item ${currentView === 'diagnostic' ? 'active' : ''}`}
                    onClick={() => onNavigate('diagnostic')}
                    title="View Diagnostic Results & Score"
                  >
                    <CheckCircle2 size={14} style={{ marginRight: '0.35rem', verticalAlign: 'text-bottom', color: '#10b981' }} />
                    Diagnostic Result
                  </button>
                )}

                {user?.role === 'ADMIN' && (
                  <button
                    type="button"
                    className={`nav-item ${currentView === 'admin' ? 'active' : ''}`}
                    onClick={() => onNavigate('admin')}
                    style={{ color: '#c084fc', fontWeight: 600 }}
                    title="Faculty & Admin Live Dataset Monitoring"
                  >
                    <ShieldCheck size={14} style={{ marginRight: '0.35rem', verticalAlign: 'text-bottom' }} />
                    Admin Monitoring
                  </button>
                )}
              </>
            ) : (
              <button
                type="button"
                className={`nav-item ${currentView === 'diagnostic' ? 'active' : ''}`}
                onClick={() => onNavigate('diagnostic')}
                style={{ fontWeight: 600, color: 'var(--accent-primary)' }}
              >
                Diagnostic Assessment
              </button>
            )}

            {!user?.onboarding_completed && (
              <button
                type="button"
                className={`nav-item ${currentView === 'onboarding' ? 'active' : ''}`}
                onClick={() => onNavigate('onboarding')}
              >
                <span>Onboarding</span>
              </button>
            )}
          </>
        )}

        {/* User Auth Section */}
        <div style={{ marginLeft: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          {isAuthenticated ? (
            <div className="user-profile-widget">
              <div className="user-avatar-badge">
                <User size={14} />
              </div>
              <div className="user-info-text">
                <span className="user-name">{user?.name || 'Learner'}</span>
                <span className="user-role">
                  {user?.role === 'ADMIN' ? 'ADMINISTRATOR' : (user?.experience_level ? `${user.experience_level.toUpperCase()} TIER` : (user?.role || 'STUDENT'))}
                  {user?.diagnostic_completed && (
                    <span style={{ marginLeft: '0.4rem', color: '#10b981', fontSize: '0.72rem' }}>
                      (Score: {user.diagnostic_score ?? 0}/{user.diagnostic_total ?? 7})
                    </span>
                  )}
                </span>
              </div>
              <button
                type="button"
                className="btn-icon-logout"
                onClick={logout}
                title="Log out"
              >
                <LogOut size={16} />
              </button>
            </div>
          ) : (
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                type="button"
                className="btn btn-secondary btn-sm"
                onClick={() => onNavigate('login')}
              >
                Sign In
              </button>
              <button
                type="button"
                className="btn btn-primary btn-sm"
                onClick={() => onNavigate('register')}
              >
                Register
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
