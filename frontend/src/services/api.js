import axios from 'axios';

// Base API URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 8000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach JWT token to outgoing requests if available
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('adaptive_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Intercept 401 responses to clear stale tokens
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear token if unauthorized
      localStorage.removeItem('adaptive_token');
    }
    return Promise.reject(error);
  }
);

/**
 * Health check service call (Milestone 1)
 */
export const fetchHealthStatus = async () => {
  try {
    const startTime = performance.now();
    const response = await apiClient.get('/health');
    const latency = Math.round(performance.now() - startTime);
    return {
      success: true,
      data: response.data,
      latency,
      error: null,
    };
  } catch (error) {
    return {
      success: false,
      data: null,
      latency: null,
      error: error.response?.data?.message || error.message || 'Failed to connect to backend server',
    };
  }
};

/**
 * Register a new user
 * @param {{ name: string, email: string, password: string }} userData
 */
export const registerUser = async (userData) => {
  const response = await apiClient.post('/auth/register', userData);
  return response.data;
};

/**
 * Log in with email and password
 * @param {{ email: string, password: string }} credentials
 */
export const loginUser = async (credentials) => {
  const response = await apiClient.post('/auth/login', credentials);
  return response.data;
};

/**
 * Fetch currently authenticated user profile
 */
export const fetchCurrentUser = async () => {
  const response = await apiClient.get('/auth/me');
  return response.data;
};

/**
 * Submit onboarding preferences
 * @param {{ learning_goal: string, experience_level: string }} payload
 */
export const submitOnboarding = async (payload) => {
  const response = await apiClient.post('/onboarding', payload);
  return response.data;
};

/**
 * Fetch current user's onboarding profile
 */
export const fetchOnboardingProfile = async () => {
  const response = await apiClient.get('/onboarding/me');
  return response.data;
};

/**
 * Fetch all DSA topics
 */
export const fetchTopics = async () => {
  const response = await apiClient.get('/problems/topics');
  return response.data;
};

/**
 * Fetch list of curated problems with optional filters
 * @param {{ topic?: string, difficulty?: string, is_diagnostic?: boolean }} params
 */
export const fetchProblems = async (params = {}) => {
  const response = await apiClient.get('/problems', { params });
  return response.data;
};

/**
 * Fetch problem details by slug
 * @param {string} slug
 */
export const fetchProblemBySlug = async (slug) => {
  const response = await apiClient.get(`/problems/${slug}`);
  return response.data;
};

/**
 * Run user code against visible test cases (Milestone 4)
 * @param {{ problem_id: number, code: string }} payload
 */
export const runCode = async (payload) => {
  const response = await apiClient.post('/submissions/run', payload);
  return response.data;
};

/**
 * Submit solution against all test cases and persist in DB (Milestone 4)
 * @param {{ problem_id: number, code: string }} payload
 */
export const submitCode = async (payload) => {
  const response = await apiClient.post('/submissions/submit', payload);
  return response.data;
};

/**
 * Fetch past submission history for a problem (Milestone 4)
 * @param {number} problemId
 */
export const fetchSubmissionHistory = async (problemId) => {
  const response = await apiClient.get(`/submissions/history/${problemId}`);
  return response.data;
};

/**
 * Fetch diagnostic problems suite (Milestone 3)
 */
export const fetchDiagnosticProblems = async () => {
  const response = await apiClient.get('/diagnostic/problems');
  return response.data;
};

/**
 * Submit single diagnostic attempt (Milestone 3)
 */
export const submitDiagnosticAttempt = async (payload) => {
  const response = await apiClient.post('/diagnostic/submit', payload);
  return response.data;
};

/**
 * Finalize diagnostic assessment (Milestone 3)
 */
export const completeDiagnostic = async () => {
  const response = await apiClient.post('/diagnostic/complete');
  return response.data;
};

/**
 * Fetch past diagnostic assessment history for authenticated user
 */
export const fetchDiagnosticHistory = async () => {
  const response = await apiClient.get('/diagnostic/history');
  return response.data;
};

/**
 * Fetch diagnostic assessment status and completion metadata
 */
export const fetchDiagnosticStatus = async () => {
  const response = await apiClient.get('/diagnostic/status');
  return response.data;
};

/**
 * Fetch authoritative diagnostic score and completion result
 */
export const fetchDiagnosticScore = async () => {
  const response = await apiClient.get('/diagnostic/score');
  return response.data;
};

/**
 * Fetch 10-topic knowledge state (Milestone 5)
 */
export const fetchKnowledgeState = async () => {
  const response = await apiClient.get('/knowledge-state');
  return response.data;
};

/**
 * Recalculate knowledge state from full interaction history (Milestone 5)
 */
export const recalculateKnowledgeState = async () => {
  const response = await apiClient.post('/knowledge-state/recalculate');
  return response.data;
};

/**
 * Fetch active next problem recommendation in ZPD (Milestone 6)
 */
export const fetchNextRecommendation = async () => {
  const response = await apiClient.get('/recommendations/next');
  return response.data;
};

/**
 * Force generate a fresh recommendation (Milestone 6)
 */
export const generateRecommendation = async () => {
  const response = await apiClient.post('/recommendations/generate');
  return response.data;
};

/**
 * Fetch recommendation history (Milestone 6)
 */
export const fetchRecommendationHistory = async () => {
  const response = await apiClient.get('/recommendations/history');
  return response.data;
};

/**
 * Fetch aggregated learner dashboard summary and analytics (Milestone 7)
 */
export const fetchDashboardSummary = async () => {
  const response = await apiClient.get('/dashboard/summary');
  return response.data;
};

/**
 * Fetch adaptive 4-stage learning roadmap (Phase 2 Step 4 & 5)
 */
export const fetchRoadmap = async () => {
  const response = await apiClient.get('/roadmap');
  return response.data;
};

/**
 * Fetch granular 37-concept learner knowledge states (Phase 2 Step 2 & 5)
 */
export const fetchConceptStates = async () => {
  const response = await apiClient.get('/knowledge-state/concepts');
  return response.data;
};

/**
 * Verification probe for Admin status (Phase 1 RBAC)
 */
export const fetchAdminStatus = async () => {
  const response = await apiClient.get('/admin/status');
  return response.data;
};

/**
 * Phase 5 Admin Monitoring & Live Dataset Export APIs
 */
export const fetchAdminOverview = async () => {
  const response = await apiClient.get('/admin/overview');
  return response.data;
};

export const fetchAdminUsers = async (params = {}) => {
  const response = await apiClient.get('/admin/users', { params });
  return response.data;
};

export const fetchAdminUserDetail = async (userId) => {
  const response = await apiClient.get(`/admin/users/${userId}`);
  return response.data;
};

export const exportAdminDataset = async (format = 'json') => {
  if (format === 'csv') {
    const response = await apiClient.get('/admin/export', {
      params: { format: 'csv' },
      responseType: 'blob'
    });
    return response.data;
  }
  const response = await apiClient.get('/admin/export', {
    params: { format: 'json' }
  });
  return response.data;
};

