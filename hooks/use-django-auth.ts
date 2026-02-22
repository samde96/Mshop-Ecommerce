import { useState, useCallback } from 'react';
import apiClient from '@/lib/api-client';

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface UserProfile {
  id: number;
  phone_number: string;
  clerkId: string;
  role: string;
  avatar_url: string;
}

export interface AuthResponse {
  message: string;
  user: User;
}

export function useDjangoAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const register = useCallback(
    async (
      username: string,
      email: string,
      password: string,
      firstName: string = '',
      lastName: string = '',
      phoneNumber: string = ''
    ) => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.post<AuthResponse>('/auth/register/', {
          username,
          email,
          password,
          first_name: firstName,
          last_name: lastName,
          phone_number: phoneNumber,
        });
        setUser(response.data.user);
        return response.data.user;
      } catch (err: any) {
        const errorMessage =
          err.response?.data?.detail ||
          err.response?.data?.error ||
          'Registration failed';
        setError(errorMessage);
        throw new Error(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const login = useCallback(async (username: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.post<AuthResponse>('/auth/login/', {
        username,
        password,
      });
      setUser(response.data.user);
      
      // Save token if provided (for future token-based auth)
      if ((response.data as any).token) {
        localStorage.setItem('auth_token', (response.data as any).token);
      }
      
      return response.data.user;
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.error || 'Login failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    setLoading(true);
    try {
      await apiClient.post('/auth/logout/');
      setUser(null);
      localStorage.removeItem('auth_token');
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Logout failed';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const getProfile = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get('/auth/profile/');
      setUser(response.data.user);
      return response.data;
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.error || 'Failed to fetch profile';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const updateProfile = useCallback(
    async (data: Partial<User & UserProfile>) => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.put('/auth/profile/', data);
        setUser(response.data.user);
        return response.data;
      } catch (err: any) {
        const errorMessage =
          err.response?.data?.error || 'Failed to update profile';
        setError(errorMessage);
        throw new Error(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return {
    user,
    loading,
    error,
    register,
    login,
    logout,
    getProfile,
    updateProfile,
  };
}
