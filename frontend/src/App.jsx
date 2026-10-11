import React, { useState, useEffect } from 'react';
import { RefreshCw } from 'lucide-react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import AuthPage from './pages/AuthPage';
import OnboardingPage from './pages/OnboardingPage';
import DiagnosticPage from './pages/DiagnosticPage';
import ProblemListPage from './pages/ProblemListPage';
import CodingWorkspacePage from './pages/CodingWorkspacePage';
import DashboardPage from './pages/DashboardPage';
import RoadmapPage from './pages/RoadmapPage';
import AdminDashboardPage from './pages/AdminDashboardPage';
import { fetchDiagnosticHistory } from './services/api';

function AppContent() {
  const [currentView, setCurrentView] = useState('login');
  const [activeProblemSlug, setActiveProblemSlug] = useState('two-sum-target-pair');
  const [initialCheckDone, setInitialCheckDone] = useState(false);
  const { user, isAuthenticated, loading } = useAuth();

  // Helper to determine the target route based on learner completion status
  const determineUserRoute = (userData) => {
    if (!userData) return 'login';
    if (userData.role === 'ADMIN') {
      return 'admin';
    }
    if (!userData.onboarding_completed) {
      return 'onboarding';
    }
    const isDiagnosticDone = Boolean(
      userData.diagnostic_completed || userData.diagnostic_exempt || userData.role === 'ADMIN'
    );
    if (!isDiagnosticDone) {
      return 'diagnostic';
    }
    return 'dashboard';
  };

  // Sync route on session initialization
  useEffect(() => {
    if (!loading) {
      if (isAuthenticated && user) {
        const targetRoute = determineUserRoute(user);
        setCurrentView((prev) => {
          if (prev === 'login' || prev === 'register' || prev === 'overview') {
            return targetRoute;
          }
          // Enforce gating if uncompleted student tries to view guarded screens
          const isDiagnosticDone = Boolean(
            user.diagnostic_completed || user.diagnostic_exempt || user.role === 'ADMIN'
          );
          if (!user.onboarding_completed && prev !== 'onboarding') {
            return 'onboarding';
          }
          if (!isDiagnosticDone && prev !== 'diagnostic' && prev !== 'onboarding') {
            return 'diagnostic';
          }
          return prev;
        });
        setInitialCheckDone(true);
      } else {
        setCurrentView((prev) => (prev === 'register' ? 'register' : 'login'));
        setInitialCheckDone(true);
      }
    }
  }, [loading, isAuthenticated, user]);

  const handleNavigate = (view) => {
    const protectedViews = ['dashboard', 'roadmap', 'problems', 'workspace', 'diagnostic', 'onboarding', 'admin'];
    if (!isAuthenticated && protectedViews.includes(view)) {
      setCurrentView('login');
      return;
    }

    if (view === 'admin') {
      if (!isAuthenticated) {
        setCurrentView('login');
        return;
      }
      if (user?.role !== 'ADMIN') {
        setCurrentView('dashboard');
        return;
      }
    }

    if (isAuthenticated && user) {
      if (!user.onboarding_completed && view !== 'onboarding') {
        setCurrentView('onboarding');
        return;
      }
      const isDiagnosticDone = Boolean(
        user.diagnostic_completed || user.diagnostic_exempt || user.role === 'ADMIN'
      );
      if (!isDiagnosticDone && view !== 'diagnostic' && view !== 'onboarding') {
        setCurrentView('diagnostic');
        return;
      }
    }

    setCurrentView(view);
  };

  const handleSelectProblem = (slug) => {
    if (!isAuthenticated) {
      setCurrentView('login');
      return;
    }
    setActiveProblemSlug(slug);
    setCurrentView('workspace');
  };

  const handleAuthSuccess = (authUser) => {
    const targetRoute = determineUserRoute(authUser);
    setCurrentView(targetRoute);
  };

  const handleOnboardingComplete = () => {
    const isDiagnosticDone = Boolean(
      user?.diagnostic_completed || user?.diagnostic_exempt || user?.role === 'ADMIN'
    );
    setCurrentView(isDiagnosticDone ? 'dashboard' : 'diagnostic');
  };

  // Show loading spinner while determining auth state
  if (loading || (isAuthenticated && !initialCheckDone)) {
    return (
      <div className="app-container">
        <Navbar currentView={currentView} onNavigate={handleNavigate} />
        <main className="main-content" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', color: 'var(--text-secondary)' }}>
          <RefreshCw size={36} className="spinning" style={{ marginBottom: '1rem', color: 'var(--accent-primary)' }} />
          <h3 style={{ margin: 0, color: '#f4f4f5' }}>Initializing Adaptive Session...</h3>
        </main>
      </div>
    );
  }

  return (
    <div className="app-container">
      <Navbar currentView={currentView} onNavigate={handleNavigate} />
      <main className="main-content">
        {/* Public / Unauthenticated Views */}
        {currentView === 'overview' && (
          <LandingPage onNavigate={handleNavigate} />
        )}

        {(currentView === 'login' || currentView === 'register') && (
          <AuthPage
            initialMode={currentView}
            onSuccess={handleAuthSuccess}
          />
        )}

        {/* Authenticated Flow Views */}
        {isAuthenticated && currentView === 'onboarding' && (
          <OnboardingPage onComplete={handleOnboardingComplete} />
        )}

        {isAuthenticated && currentView === 'diagnostic' && (
          <DiagnosticPage
            onSelectProblem={handleSelectProblem}
            onNavigate={handleNavigate}
          />
        )}

        {isAuthenticated && currentView === 'dashboard' && (
          <DashboardPage
            onSelectProblem={handleSelectProblem}
            onNavigate={handleNavigate}
          />
        )}

        {isAuthenticated && currentView === 'roadmap' && (
          <RoadmapPage
            onSelectProblem={handleSelectProblem}
            onNavigate={handleNavigate}
          />
        )}

        {isAuthenticated && currentView === 'problems' && (
          <ProblemListPage onSelectProblem={handleSelectProblem} />
        )}

        {isAuthenticated && currentView === 'workspace' && (
          <CodingWorkspacePage
            problemSlug={activeProblemSlug}
            onBack={() => setCurrentView('problems')}
            onNavigateToAuth={(mode) => setCurrentView(mode)}
            onSelectProblem={handleSelectProblem}
          />
        )}

        {isAuthenticated && user?.role === 'ADMIN' && currentView === 'admin' && (
          <AdminDashboardPage onNavigate={handleNavigate} />
        )}

        {/* Fallback for unauthenticated attempt to render protected views */}
        {!isAuthenticated && currentView !== 'overview' && currentView !== 'login' && currentView !== 'register' && (
          <AuthPage
            initialMode="login"
            onSuccess={handleAuthSuccess}
          />
        )}
      </main>
      <footer className="footer">
        AI-Driven Adaptive Learning &amp; Problem Recommendation Framework • Intelligent Personalized DSA Mastery Platform
      </footer>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
