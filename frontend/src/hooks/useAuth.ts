import { useState, useEffect } from 'react';
import { authService } from '../services/api';
import type { User, AuthResponse, RegisterData } from '../types';

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const userData = await authService.getProfile();
        setUser(userData);
        setIsAuthenticated(true);
      } catch (error) {
        logout();
      }
    }
    setIsLoading(false);
  };

  const login = async (email: string, password: string) => {
    const response: AuthResponse = await authService.login(email, password);
    localStorage.setItem('access_token', response.access);
    localStorage.setItem('refresh_token', response.refresh);
    await checkAuth();
  };

  const register = async (data: RegisterData) => {
    await authService.register(data);
    // After registration, auto-login
    await login(data.email, data.password);
  };

  const logout = () => {
    authService.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  return {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    checkAuth,
  };
};
