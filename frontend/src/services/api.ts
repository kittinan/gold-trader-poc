import axios, { AxiosError } from 'axios';
import type { AxiosInstance } from 'axios';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as any;

        // Handle token refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const refreshToken = localStorage.getItem('refresh_token');
            const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
              refresh: refreshToken,
            });

            const { access } = response.data;
            localStorage.setItem('access_token', access);

            // Retry original request with new token
            originalRequest.headers.Authorization = `Bearer ${access}`;
            return this.client(originalRequest);
          } catch (refreshError) {
            // Refresh failed - logout user
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  public get(url: string, params?: any) {
    return this.client.get(url, { params });
  }

  public post(url: string, data?: any) {
    return this.client.post(url, data);
  }

  public put(url: string, data?: any) {
    return this.client.put(url, data);
  }

  public patch(url: string, data?: any) {
    return this.client.patch(url, data);
  }

  public delete(url: string) {
    return this.client.delete(url);
  }
}

// Create singleton instance
const apiClient = new ApiClient();

export default apiClient;

// API Service functions
export const authService = {
  login: async (email: string, password: string) => {
    const response = await apiClient.post('/auth/login/', {
      email,
      password,
    });
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  register: async (userData: any) => {
    const response = await apiClient.post('/auth/register/', userData);
    return response.data;
  },

  getProfile: async () => {
    const response = await apiClient.get('/auth/profile/');
    return response.data;
  },
};

export const goldPriceService = {
  getLatest: async () => {
    const response = await apiClient.get('/gold-prices/latest/');
    return response.data;
  },

  getHistory: async (params?: any) => {
    const response = await apiClient.get('/gold-prices/', { params });
    return response.data;
  },
};

export const transactionService = {
  getList: async (params?: any) => {
    const response = await apiClient.get('/transactions/', { params });
    return response.data;
  },

  create: async (data: any) => {
    const response = await apiClient.post('/transactions/', data);
    return response.data;
  },

  getDetail: async (id: number) => {
    const response = await apiClient.get(`/transactions/${id}/`);
    return response.data;
  },
};

export const walletService = {
  getMyWallet: async () => {
    const response = await apiClient.get('/wallets/my_wallet/');
    return response.data;
  },

  getList: async (params?: any) => {
    const response = await apiClient.get('/wallets/', { params });
    return response.data;
  },
};

export const goldHoldingsService = {
  getHoldings: async () => {
    const response = await apiClient.get('/gold-holdings/');
    return response.data;
  },
};
