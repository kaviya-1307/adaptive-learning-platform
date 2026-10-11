import React, { createContext, useContext, useState, useEffect } from 'react';
import { 
  loginUser, 
  registerUser, 
  fetchCurrentUser, 
  submitOnboarding 
} from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('adaptive_token') || null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize auth state on mount
  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem('adaptive_token');
      if (storedToken) {
        try {
          const userData = await fetchCurrentUser();
          setUser(userData);
        } catch (err) {
          console.warn('Session expired or invalid token:', err);
          localStorage.removeItem('adaptive_token');
          setToken(null);
          setUser(null);
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email, password) => {
    setError(null);
    try {
      const res = await loginUser({ email, password });
      localStorage.setItem('adaptive_token', res.access_token);
      setToken(res.access_token);
      setUser(res.user);
      return { success: true, user: res.user };
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Login failed';
      setError(msg);
      return { success: false, error: msg };
    }
  };

  const register = async (name, email, password) => {
    setError(null);
    try {
      const res = await registerUser({ name, email, password });
      // Registration creates the user normally in the DB but does NOT authenticate the session
      return { success: true, user: res.user, email };
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Registration failed';
      setError(msg);
      return { success: false, error: msg };
    }
  };

  const logout = () => {
    localStorage.removeItem('adaptive_token');
    setToken(null);
    setUser(null);
    setError(null);
  };

  const completeOnboarding = async (learningGoal, experienceLevel) => {
    setError(null);
    try {
      const res = await submitOnboarding({
        learning_goal: learningGoal,
        experience_level: experienceLevel
      });
      // Refresh user profile
      const updatedUser = await fetchCurrentUser();
      setUser(updatedUser);
      return { success: true, data: res, user: updatedUser };
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Failed to submit onboarding';
      setError(msg);
      return { success: false, error: msg };
    }
  };

  const refreshUser = async () => {
    if (!token) return;
    try {
      const userData = await fetchCurrentUser();
      setUser(userData);
    } catch (err) {
      console.warn('Failed to refresh user:', err);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user,
        loading,
        error,
        setError,
        login,
        register,
        logout,
        completeOnboarding,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
