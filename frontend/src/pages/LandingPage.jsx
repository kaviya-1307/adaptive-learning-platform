import React from 'react';
import { 
  Cpu, 
  Database, 
  Code2, 
  Sparkles, 
  BrainCircuit, 
  CheckCircle2, 
  ArrowRight, 
  Target,
  UserCheck,
  Zap,
  Activity,
  Award,
  Layers,
  Check,
  TrendingUp,
  BookOpen
} from 'lucide-react';
import HealthIndicator from '../components/HealthIndicator';
import { useAuth } from '../context/AuthContext';

export default function LandingPage({ onNavigate }) {
  const { user, isAuthenticated } = useAuth();

  const pipelineSteps = [
    {
      num: 1,
      title: 'Target Calibration & Onboarding',
      desc: 'Capture learner goals (Interview Prep, Campus Placement, or Contests) and baseline coding experience level.'
    },
    {
      num: 2,
      title: 'Multi-Topic Diagnostic Assessment',
      desc: '7-problem foundational coding suite assessing skill across core domains to initialize prior mastery.'
    },
    {
      num: 3,
      title: 'Bayesian Concept Mastery & Knowledge State',
      desc: 'Conjugate prior Beta-Binomial smoothing continuously updates 37 concept masteries and weakness profiles from interaction sequences.'
    },
    {
      num: 4,
      title: 'Zone of Proximal Development Dispatch',
      desc: 'Pedagogical recommendation engine selects optimal problems (~70% target success probability) with clear rationale.'
    },
    {
      num: 5,
      title: 'Python Coding Sandbox',
      desc: 'In-browser Monaco editor with sub-process test evaluation, runtime guards, and instant feedback.'
    },
    {
      num: 6,
      title: 'Personalized Progress Analytics',
      desc: 'Multi-topic radar chart, difficulty distribution metrics, recommendation histories, and mastery tiers.'
    }
  ];

  const features = [
    {
      icon: BrainCircuit,
      color: '#a78bfa',
      title: 'Bayesian Concept-Level Mastery',
      desc: 'Empirical Bayesian model traces skill evolution across 37 Codeforces-derived concepts, capturing calibrated learning patterns.'
    },
    {
      icon: Target,
      color: '#38bdf8',
      title: 'ZPD Recommendation Engine',
      desc: 'Logistic sigmoid modeling pairs difficulty with learner mastery to maintain learners in their optimal learning zone.'
    },
    {
      icon: Code2,
      color: '#34d399',
      title: 'Sandboxed Python Runner',
      desc: 'Sub-process code execution sandbox with timeout defense, memory isolation, and multi-test validation.'
    },
    {
      icon: TrendingUp,
      color: '#fbbf24',
      title: '10-Domain DSA Mastery',
      desc: 'Curated and expanded 889-problem catalog covering Arrays, Strings, Hashing, Linked Lists, Trees, Graphs, DP, and more.'
    },
    {
      icon: Zap,
      color: '#f43f5e',
      title: 'Explainable AI Dispatch',
      desc: 'Deterministic educational explanations for every recommended problem, clarifying pedagogical intent.'
    },
    {
      icon: Award,
      color: '#60a5fa',
      title: 'Personalized Learner Dashboard',
      desc: 'Interactive Recharts radar visualization, topic mastery tiers (Novice to Master), and submission history.'
    }
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Hero Section */}
      <section className="hero-section">
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem', flexWrap: 'wrap', justifyContent: 'center' }}>
          <span className="badge badge-purple">
            <BrainCircuit size={14} /> AI-Powered DSA Learning
          </span>
          <span className="badge badge-blue">
            <Target size={14} /> Zone of Proximal Development
          </span>
          <span className="badge badge-green">
            <Sparkles size={14} /> Bayesian Concept Mastery
          </span>
        </div>

        <h1 className="hero-title">
          AI-Driven Adaptive Learning &amp;<br />
          Problem Recommendation Framework
        </h1>
        <p className="hero-subtitle">
          An intelligent personalized DSA learning system that assesses your baseline skill, models concept mastery 
          using Bayesian smoothing, executes Python code in real time, and recommends problems tailored to your optimal learning zone.
        </p>

        {/* Hero Interactive Actions */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '1rem', marginTop: '1.5rem', flexWrap: 'wrap' }}>
          {isAuthenticated ? (
            <>
              <button
                type="button"
                className="btn btn-primary"
                style={{ padding: '0.75rem 1.5rem', fontSize: '0.9375rem' }}
                onClick={() => onNavigate('diagnostic')}
              >
                <BrainCircuit size={18} />
                <span>Start Diagnostic Assessment</span>
                <ArrowRight size={16} />
              </button>

              <button
                type="button"
                className="btn btn-secondary"
                style={{ padding: '0.75rem 1.5rem', fontSize: '0.9375rem' }}
                onClick={() => onNavigate('dashboard')}
              >
                <Award size={18} />
                <span>Go to Learner Dashboard</span>
              </button>

              <button
                type="button"
                className="btn btn-secondary"
                style={{ padding: '0.75rem 1.5rem', fontSize: '0.9375rem' }}
                onClick={() => onNavigate('problems')}
              >
                <BookOpen size={18} />
                <span>Browse 889 Problems</span>
              </button>
            </>
          ) : (
            <>
              <button
                type="button"
                className="btn btn-primary"
                style={{ padding: '0.75rem 1.5rem', fontSize: '0.9375rem' }}
                onClick={() => onNavigate('register')}
              >
                <Sparkles size={18} />
                <span>Get Started Free</span>
                <ArrowRight size={16} />
              </button>

              <button
                type="button"
                className="btn btn-secondary"
                style={{ padding: '0.75rem 1.5rem', fontSize: '0.9375rem' }}
                onClick={() => onNavigate('problems')}
              >
                <Code2 size={18} />
                <span>Explore 889 DSA Problems</span>
              </button>
            </>
          )}
        </div>
      </section>

      {/* Backend Live Connection Status */}
      <HealthIndicator />

      {/* Active Session Overview if authenticated */}
      {isAuthenticated && (
        <div className="card" style={{ borderLeft: '4px solid var(--accent-success)', padding: '1.25rem 1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <div className="auth-icon-badge" style={{ width: 42, height: 42 }}>
                <UserCheck size={22} color="white" />
              </div>
              <div>
                <h3 style={{ fontSize: '1rem', fontWeight: 600, margin: 0, color: '#f4f4f5' }}>
                  Learner Profile: {user?.name}
                </h3>
                <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', margin: '0.2rem 0 0' }}>
                  Email: <strong>{user?.email}</strong> • Onboarding: {user?.onboarding_completed ? 'Completed' : 'Pending'}
                  {user?.learning_goal && ` • Goal: ${user.learning_goal}`}
                  {user?.experience_level && ` • Tier: ${user.experience_level}`}
                </p>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                type="button"
                className="btn btn-secondary btn-sm"
                onClick={() => onNavigate('diagnostic')}
              >
                Diagnostic Assessment
              </button>
              <button
                type="button"
                className="btn btn-primary btn-sm"
                onClick={() => onNavigate('dashboard')}
              >
                Dashboard
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Core Adaptive Loop Pipeline */}
      <div className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
          <BrainCircuit size={22} color="var(--accent-primary)" />
          <h2 style={{ fontSize: '1.25rem', fontWeight: 600, margin: 0, color: '#f4f4f5' }}>
            End-to-End Adaptive Learning Pipeline
          </h2>
        </div>

        <div className="grid-2">
          {pipelineSteps.map((step) => (
            <div key={step.num} className="flow-step">
              <div className="flow-step-num">{step.num}</div>
              <div className="flow-step-text">
                <strong style={{ color: '#f4f4f5' }}>{step.title}</strong>
                <p style={{ margin: '0.25rem 0 0', fontSize: '0.8125rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                  {step.desc}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Intelligent Features Grid */}
      <div>
        <div style={{ marginBottom: '1rem', textAlign: 'left' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 600, margin: 0, color: '#f4f4f5' }}>
            Framework Core Capabilities
          </h2>
          <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)', margin: '0.25rem 0 0' }}>
            Integrated machine learning and pedagogical intelligence designed for maximum DSA mastery.
          </p>
        </div>

        <div className="grid-3">
          {features.map((f, i) => {
            const IconComponent = f.icon;
            return (
              <div key={i} className="card" style={{ padding: '1.25rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
                  <div style={{ width: 36, height: 36, borderRadius: '8px', background: `${f.color}20`, display: 'flex', alignItems: 'center', justifyContent: 'center', color: f.color }}>
                    <IconComponent size={20} />
                  </div>
                  <h3 style={{ fontSize: '0.95rem', fontWeight: 600, margin: 0, color: '#f4f4f5' }}>
                    {f.title}
                  </h3>
                </div>
                <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', lineHeight: 1.6, margin: 0 }}>
                  {f.desc}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
