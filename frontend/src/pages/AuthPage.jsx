import React, { useState } from 'react';
import { 
  Lock, 
  Mail, 
  User, 
  ArrowRight, 
  Sparkles, 
  AlertCircle, 
  CheckCircle2, 
  ShieldCheck 
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function AuthPage({ initialMode = 'login', onSuccess }) {
  const [mode, setMode] = useState(initialMode); // 'login' | 'register'
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [localError, setLocalError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const { login, register, error: authError, setError } = useAuth();

  const handleTabChange = (newMode) => {
    setMode(newMode);
    setLocalError('');
    setError(null);
    if (newMode === 'register') {
      setSuccessMessage('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLocalError('');
    setError(null);

    if (mode === 'register') {
      if (!name.trim()) {
        setLocalError('Please enter your full name.');
        return;
      }
      if (password.length < 6) {
        setLocalError('Password must be at least 6 characters.');
        return;
      }
      if (password !== confirmPassword) {
        setLocalError('Passwords do not match.');
        return;
      }

      setSubmitting(true);
      const res = await register(name, email, password);
      setSubmitting(false);

      if (res.success) {
        // Required behavior: Show clear message: "Registration successful. Please login to continue."
        // Navigate to Login page, preserve email, do not auto-login
        setSuccessMessage('Registration successful. Please login to continue.');
        setMode('login');
        setPassword('');
        setConfirmPassword('');
        setLocalError('');
      }
    } else {
      if (!email.trim() || !password) {
        setLocalError('Please fill in both email and password.');
        return;
      }

      setSubmitting(true);
      setSuccessMessage('');
      const res = await login(email, password);
      setSubmitting(false);

      if (res.success) {
        if (onSuccess) onSuccess(res.user);
      }
    }
  };

  const activeError = localError || authError;

  return (
    <div className="auth-page-container">
      <div className="auth-card">
        {/* Header */}
        <div className="auth-header">
          <div className="auth-icon-badge">
            <Sparkles size={24} color="white" />
          </div>
          <h2 className="auth-title">
            {mode === 'login' ? 'Welcome Back' : 'Create Your Account'}
          </h2>
          <p className="auth-subtitle">
            {mode === 'login' 
              ? 'Access your personalized DSA learning path and mastery tracking' 
              : 'Join the AI-driven adaptive DSA recommendation platform'}
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="auth-tabs">
          <button
            type="button"
            className={`auth-tab ${mode === 'login' ? 'active' : ''}`}
            onClick={() => handleTabChange('login')}
          >
            Sign In
          </button>
          <button
            type="button"
            className={`auth-tab ${mode === 'register' ? 'active' : ''}`}
            onClick={() => handleTabChange('register')}
          >
            Register
          </button>
        </div>

        {/* Success Banner */}
        {successMessage && (
          <div
            className="auth-alert-success"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.625rem',
              background: 'rgba(34, 197, 94, 0.12)',
              border: '1px solid rgba(34, 197, 94, 0.35)',
              color: '#4ade80',
              padding: '0.75rem 1rem',
              borderRadius: 'var(--radius-md, 6px)',
              marginBottom: '1rem',
              fontSize: '0.875rem',
              fontWeight: 500,
            }}
          >
            <CheckCircle2 size={18} style={{ flexShrink: 0, color: '#4ade80' }} />
            <span>{successMessage}</span>
          </div>
        )}

        {/* Error Banner */}
        {activeError && (
          <div className="auth-error-banner">
            <AlertCircle size={18} style={{ flexShrink: 0 }} />
            <span>{activeError}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="auth-form">
          {mode === 'register' && (
            <div className="form-group">
              <label className="form-label" htmlFor="auth-name">Full Name</label>
              <div className="input-icon-wrapper">
                <User size={18} className="input-icon" />
                <input
                  id="auth-name"
                  type="text"
                  className="form-input with-icon"
                  placeholder="Alex Mercer"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
            </div>
          )}

          <div className="form-group">
            <label className="form-label" htmlFor="auth-email">Email Address</label>
            <div className="input-icon-wrapper">
              <Mail size={18} className="input-icon" />
              <input
                id="auth-email"
                type="email"
                className="form-input with-icon"
                placeholder="alex@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="auth-password">Password</label>
            <div className="input-icon-wrapper">
              <Lock size={18} className="input-icon" />
              <input
                id="auth-password"
                type="password"
                className="form-input with-icon"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          {mode === 'register' && (
            <div className="form-group">
              <label className="form-label" htmlFor="auth-confirm-password">Confirm Password</label>
              <div className="input-icon-wrapper">
                <Lock size={18} className="input-icon" />
                <input
                  id="auth-confirm-password"
                  type="password"
                  className="form-input with-icon"
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>
            </div>
          )}

          <button
            type="submit"
            className="btn btn-primary auth-submit-btn"
            disabled={submitting}
          >
            {submitting ? (
              <span>Processing...</span>
            ) : (
              <>
                <span>{mode === 'login' ? 'Sign In' : 'Get Started'}</span>
                <ArrowRight size={16} />
              </>
            )}
          </button>
        </form>

        {/* Footer info */}
        <div className="auth-footer">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem', color: 'var(--text-muted)', fontSize: '0.75rem' }}>
            <ShieldCheck size={14} />
            <span>Secure bcrypt salted hash &amp; signed JWT session</span>
          </div>
        </div>
      </div>
    </div>
  );
}
