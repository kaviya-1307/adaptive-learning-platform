import React, { useState } from 'react';
import { 
  Target, 
  Compass, 
  Briefcase, 
  GraduationCap, 
  Trophy, 
  Code, 
  Zap, 
  Award, 
  ArrowRight, 
  ArrowLeft, 
  CheckCircle2, 
  BrainCircuit, 
  Sparkles,
  Layers
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function OnboardingPage({ onComplete }) {
  const { user, completeOnboarding } = useAuth();

  const [step, setStep] = useState(1);
  const [learningGoal, setLearningGoal] = useState('interview_prep');
  const [experienceLevel, setExperienceLevel] = useState('intermediate');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [completedProfile, setCompletedProfile] = useState(null);

  const goalOptions = [
    {
      id: 'placement_prep',
      title: 'Campus Placement Prep',
      icon: GraduationCap,
      color: '#38bdf8',
      desc: 'Master standard hiring patterns, Arrays, Strings, Trees, and core coding questions for campus drives.',
      badge: 'College & Entry-Level'
    },
    {
      id: 'interview_prep',
      title: 'Tech Interview Prep',
      icon: Briefcase,
      color: '#60a5fa',
      desc: 'Focused curriculum for product companies (FAANG/MAANG) prioritizing Medium-Hard DP, Graphs, and Hash Maps.',
      badge: 'Product & SDE Roles'
    },
    {
      id: 'learn_dsa',
      title: 'Learn DSA from Scratch',
      icon: Compass,
      color: '#34d399',
      desc: 'Comprehensive step-by-step foundation covering linear structures, searching, sorting, and problem intuition.',
      badge: 'Foundations First'
    },
    {
      id: 'competitive_programming',
      title: 'Competitive Programming',
      icon: Trophy,
      color: '#fbbf24',
      desc: 'High-difficulty optimization, advanced dynamic programming, topological sorting, and math algorithms.',
      badge: 'Contests & Rating'
    },
  ];

  const experienceOptions = [
    {
      id: 'beginner',
      title: 'Beginner',
      levelText: 'Level 1',
      icon: Code,
      priorMastery: '0.25 (25%)',
      color: '#34d399',
      desc: 'Basic syntax known; new to algorithmic problem solving, recursion, and time complexity analysis.',
      topicsFocus: 'Linear structures, basic loops, two pointers'
    },
    {
      id: 'intermediate',
      title: 'Intermediate',
      levelText: 'Level 2',
      icon: Zap,
      priorMastery: '0.50 (50%)',
      color: '#60a5fa',
      desc: 'Solved 20–50 coding problems; familiar with Binary Trees, Hash Tables, and common recursion patterns.',
      topicsFocus: 'Trees, BFS/DFS, basic Dynamic Programming'
    },
    {
      id: 'advanced',
      title: 'Advanced',
      levelText: 'Level 3',
      icon: Award,
      priorMastery: '0.75 (75%)',
      color: '#a78bfa',
      desc: 'Comfortable with complex data structures, multi-dimensional DP, backtracking, and graph traversals.',
      topicsFocus: 'Advanced DP, Segment Trees, Hard Graphs'
    },
  ];

  const selectedGoalObj = goalOptions.find(g => g.id === learningGoal);
  const selectedExpObj = experienceOptions.find(e => e.id === experienceLevel);

  const handleSubmit = async () => {
    setError('');
    setSubmitting(true);

    const res = await completeOnboarding(learningGoal, experienceLevel);
    setSubmitting(false);

    if (res.success) {
      setCompletedProfile(res.data);
      setStep(3); // Success step
    } else {
      setError(res.error || 'Failed to save onboarding preferences.');
    }
  };

  const handleFinish = () => {
    if (onComplete) onComplete();
  };

  return (
    <div className="onboarding-container">
      {/* Stepper Header */}
      <div className="onboarding-stepper">
        <div className={`stepper-step ${step >= 1 ? 'active' : ''} ${step > 1 ? 'completed' : ''}`}>
          <div className="stepper-circle">{step > 1 ? '✓' : '1'}</div>
          <span>Target Goal</span>
        </div>
        <div className="stepper-divider" />
        <div className={`stepper-step ${step >= 2 ? 'active' : ''} ${step > 2 ? 'completed' : ''}`}>
          <div className="stepper-circle">{step > 2 ? '✓' : '2'}</div>
          <span>Experience Level</span>
        </div>
        <div className="stepper-divider" />
        <div className={`stepper-step ${step >= 3 ? 'active' : ''}`}>
          <div className="stepper-circle">3</div>
          <span>Calibration</span>
        </div>
      </div>

      {/* Step 1: Learning Goal */}
      {step === 1 && (
        <div className="card onboarding-card">
          <div className="onboarding-header">
            <div className="badge badge-blue" style={{ marginBottom: '0.5rem' }}>
              <Target size={14} /> Step 1 of 2
            </div>
            <h2 className="onboarding-title">What is your primary learning goal?</h2>
            <p className="onboarding-subtitle">
              The adaptive recommendation engine uses your goal to weight problem difficulty and topic priority.
            </p>
          </div>

          <div className="onboarding-grid">
            {goalOptions.map((goal) => {
              const IconComp = goal.icon;
              const isSelected = learningGoal === goal.id;
              return (
                <div
                  key={goal.id}
                  className={`selection-card ${isSelected ? 'selected' : ''}`}
                  onClick={() => setLearningGoal(goal.id)}
                >
                  <div className="selection-card-header">
                    <div 
                      className="selection-icon-box"
                      style={{ backgroundColor: `${goal.color}20`, color: goal.color }}
                    >
                      <IconComp size={22} />
                    </div>
                    <span className="badge badge-blue" style={{ fontSize: '0.6875rem' }}>
                      {goal.badge}
                    </span>
                  </div>
                  <h3 className="selection-title">{goal.title}</h3>
                  <p className="selection-desc">{goal.desc}</p>
                  {isSelected && (
                    <div className="selection-check">
                      <CheckCircle2 size={16} color="var(--accent-primary)" />
                      <span>Selected</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          <div className="onboarding-actions">
            <div />
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => setStep(2)}
            >
              <span>Next: Experience Level</span>
              <ArrowRight size={16} />
            </button>
          </div>
        </div>
      )}

      {/* Step 2: Experience Level */}
      {step === 2 && (
        <div className="card onboarding-card">
          <div className="onboarding-header">
            <div className="badge badge-green" style={{ marginBottom: '0.5rem' }}>
              <BrainCircuit size={14} /> Step 2 of 2
            </div>
            <h2 className="onboarding-title">What is your current coding background?</h2>
            <p className="onboarding-subtitle">
              We initialize your baseline prior knowledge state $\mu_0$ across 10 DSA topics based on this calibration.
            </p>
          </div>

          {error && (
            <div className="auth-error-banner" style={{ marginBottom: '1.25rem' }}>
              <span>{error}</span>
            </div>
          )}

          <div className="onboarding-grid">
            {experienceOptions.map((exp) => {
              const IconComp = exp.icon;
              const isSelected = experienceLevel === exp.id;
              return (
                <div
                  key={exp.id}
                  className={`selection-card ${isSelected ? 'selected' : ''}`}
                  onClick={() => setExperienceLevel(exp.id)}
                >
                  <div className="selection-card-header">
                    <div 
                      className="selection-icon-box"
                      style={{ backgroundColor: `${exp.color}20`, color: exp.color }}
                    >
                      <IconComp size={22} />
                    </div>
                    <span className="badge badge-green" style={{ fontSize: '0.6875rem' }}>
                      Prior: {exp.priorMastery}
                    </span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.5rem', marginTop: '0.5rem' }}>
                    <h3 className="selection-title">{exp.title}</h3>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>({exp.levelText})</span>
                  </div>
                  <p className="selection-desc">{exp.desc}</p>
                  <div style={{ marginTop: '0.75rem', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                    <strong>Focus:</strong> {exp.topicsFocus}
                  </div>
                  {isSelected && (
                    <div className="selection-check">
                      <CheckCircle2 size={16} color="var(--accent-success)" />
                      <span>Selected</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          <div className="onboarding-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => setStep(1)}
              disabled={submitting}
            >
              <ArrowLeft size={16} />
              <span>Back</span>
            </button>
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleSubmit}
              disabled={submitting}
            >
              {submitting ? (
                <span>Calibrating Prior State...</span>
              ) : (
                <>
                  <span>Save &amp; Calibrate Profile</span>
                  <ArrowRight size={16} />
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Success & Calibration Summary */}
      {step === 3 && (
        <div className="card onboarding-card" style={{ textAlign: 'center' }}>
          <div style={{ margin: '1rem auto 1.5rem', width: 64, height: 64, borderRadius: '50%', backgroundColor: 'rgba(16, 185, 129, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--accent-success)' }}>
            <CheckCircle2 size={36} />
          </div>

          <h2 className="onboarding-title" style={{ fontSize: '1.75rem' }}>
            Onboarding Completed Successfully!
          </h2>
          <p className="onboarding-subtitle" style={{ maxWidth: 580, margin: '0.5rem auto 1.75rem' }}>
            Your learner profile has been calibrated in MySQL and mapped to the AI recommendation pipeline.
          </p>

          <div className="calibration-summary-box">
            <div className="summary-item">
              <span className="summary-label">Target Learning Goal</span>
              <strong className="summary-val" style={{ color: selectedGoalObj?.color }}>
                {selectedGoalObj?.title}
              </strong>
            </div>
            <div className="summary-item">
              <span className="summary-label">Experience Tier</span>
              <strong className="summary-val" style={{ color: selectedExpObj?.color }}>
                {selectedExpObj?.title}
              </strong>
            </div>
            <div className="summary-item">
              <span className="summary-label">Initial Prior Mastery</span>
              <strong className="summary-val" style={{ color: '#34d399' }}>
                {selectedExpObj?.priorMastery}
              </strong>
            </div>
            <div className="summary-item">
              <span className="summary-label">Active Learner</span>
              <strong className="summary-val">
                {user?.name || 'Active User'} ({user?.email})
              </strong>
            </div>
          </div>

          <div style={{ margin: '2rem 0 1rem', display: 'flex', gap: '0.75rem', justifyContent: 'center', flexWrap: 'wrap' }}>
            <button
              type="button"
              className="btn btn-primary"
              style={{ minWidth: 240, padding: '0.75rem 1.5rem' }}
              onClick={handleFinish}
            >
              <span>Start Diagnostic Assessment</span>
              <ArrowRight size={18} />
            </button>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            Calibrate your baseline 10-topic knowledge state through the 7-problem diagnostic assessment suite.
          </p>
        </div>
      )}
    </div>
  );
}
