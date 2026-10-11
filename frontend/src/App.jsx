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

  // Helper to determine the target route based on user role and completion status
  const determineUserRoute = (userData) => {
    if (!userData) return 'login';
    if (userData.role === 'ADMIN') {
      return 'admin';
    }
    if (!userData.onboarding_completed) {
      return 'onboarding';
    }
    const isDiagnosticDone = Boolean(
      userData.diagnostic_completed || userData.diagnostic_exempt
    );
    if (!isDiagnosticDone) {
      return 'diagnostic';
    }
    return 'dashboard';
  };

  // Helper to extract requested route from URL (hash, query param, or pathname)
  const getViewFromUrl = () => {
    try {
      const hash = window.location.hash.replace(/^#\/?/, '').trim();
      if (hash) return hash;
      const params = new URLSearchParams(window.location.search);
      const viewParam = params.get('view');
      if (viewParam) return viewParam;
      const path = window.location.pathname.replace(/^\//, '').trim();
      if (path && ['dashboard', 'roadmap', 'problems', 'workspace', 'diagnostic', 'onboarding', 'admin', 'login', 'register', 'overview'].includes(path)) {
        return path;
      }
    } catch {
      // In non-browser environments
    }
    return null;
  };

  // Helper to sync current view into window URL hash
  const syncUrl = (view) => {
    try {
      if (window.location.hash !== `#${view}`) {
        window.history.replaceState(null, '', `#${view}`);
      }
    } catch {
      // In non-browser environments
    }
  };

  // Route Protection & RBAC Enforcement Gate
  const guardView = (targetView, currentUser, authenticated) => {
    const studentViews = ['dashboard', 'roadmap', 'problems', 'workspace', 'diagnostic', 'onboarding'];
    const adminViews = ['admin'];
    const protectedViews = [...studentViews, ...adminViews];

    if (!authenticated) {
      if (protectedViews.includes(targetView)) {
        return 'login';
      }
      return targetView || 'login';
    }

    // ADMIN USERS: Restricted strictly to 'admin'
    if (currentUser?.role === 'ADMIN') {
      if (studentViews.includes(targetView) || targetView !== 'admin') {
        return 'admin';
      }
      return 'admin';
    }

    // STUDENT USERS: Restricted from 'admin'
    if (adminViews.includes(targetView)) {
      return determineUserRoute(currentUser);
    }

    // Student Onboarding & Diagnostic Progression Gating
    if (!currentUser?.onboarding_completed && targetView !== 'onboarding') {
      return 'onboarding';
    }
    const isDiagnosticDone = Boolean(
      currentUser?.diagnostic_completed || currentUser?.diagnostic_exempt
    );
    if (!isDiagnosticDone && targetView !== 'diagnostic' && targetView !== 'onboarding') {
      return 'diagnostic';
    }

    return targetView;
  };

  // Sync route on session initialization & auth changes
  useEffect(() => {
    if (!loading) {
      const urlView = getViewFromUrl();
      if (isAuthenticated && user) {
        const initialTarget = urlView ? guardView(urlView, user, true) : determineUserRoute(user);
        setCurrentView(initialTarget);
        syncUrl(initialTarget);
      } else {
        const initialTarget = (urlView === 'register' || urlView === 'overview') ? urlView : 'login';
        setCurrentView(initialTarget);
        syncUrl(initialTarget);
      }
      setInitialCheckDone(true);
    }
  }, [loading, isAuthenticated, user]);

  // Listen to direct URL changes (e.g. hash changes or back/forward buttons)
  useEffect(() => {
    const handleUrlChange = () => {
      const urlView = getViewFromUrl();
      if (urlView) {
        const guarded = guardView(urlView, user, isAuthenticated);
        setCurrentView(guarded);
        syncUrl(guarded);
      }
    };
    window.addEventListener('hashchange', handleUrlChange);
    window.addEventListener('popstate', handleUrlChange);
    return () => {
      window.removeEventListener('hashchange', handleUrlChange);
      window.removeEventListener('popstate', handleUrlChange);
    };
  }, [user, isAuthenticated]);

  const handleNavigate = (view) => {
    const guarded = guardView(view, user, isAuthenticated);
    setCurrentView(guarded);
    syncUrl(guarded);
  };

  const handleSelectProblem = (slug) => {
    if (!isAuthenticated) {
      handleNavigate('login');
      return;
    }
    if (user?.role === 'ADMIN') {
      handleNavigate('admin');
      return;
    }
    setActiveProblemSlug(slug);
    setCurrentView('workspace');
    syncUrl('workspace');
  };

  const handleAuthSuccess = (authUser) => {
    const targetRoute = determineUserRoute(authUser);
    setCurrentView(targetRoute);
    syncUrl(targetRoute);
  };

  const handleOnboardingComplete = () => {
    const isDiagnosticDone = Boolean(
      user?.diagnostic_completed || user?.diagnostic_exempt
    );
    const target = isDiagnosticDone ? 'dashboard' : 'diagnostic';
    setCurrentView(target);
    syncUrl(target);
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

        {/* Authenticated Flow Views - STUDENT ONLY */}
        {isAuthenticated && user?.role !== 'ADMIN' && currentView === 'onboarding' && (
          <OnboardingPage onComplete={handleOnboardingComplete} />
        )}

        {isAuthenticated && user?.role !== 'ADMIN' && currentView === 'diagnostic' && (
          <DiagnosticPage
            onSelectProblem={handleSelectProblem}
            onNavigate={handleNavigate}
          />
        )}

        {isAuthenticated && user?.role !== 'ADMIN' && currentView === 'dashboard' && (
          <DashboardPage
            onSelectProblem={handleSelectProblem}
            onNavigate={handleNavigate}
          />
        )}

        {isAuthenticated && user?.role !== 'ADMIN' && currentView === 'roadmap' && (
          <RoadmapPage
            onSelectProblem={handleSelectProblem}
            onNavigate={handleNavigate}
          />
        )}

        {isAuthenticated && user?.role !== 'ADMIN' && currentView === 'problems' && (
          <ProblemListPage onSelectProblem={handleSelectProblem} />
        )}

        {isAuthenticated && user?.role !== 'ADMIN' && currentView === 'workspace' && (
          <CodingWorkspacePage
            problemSlug={activeProblemSlug}
            onBack={() => handleNavigate('problems')}
            onNavigateToAuth={(mode) => handleNavigate(mode)}
            onSelectProblem={handleSelectProblem}
          />
        )}

        {/* Authenticated Flow Views - ADMIN ONLY */}
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
