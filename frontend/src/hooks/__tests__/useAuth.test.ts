import { describe, it, expect, beforeEach, vi } from 'vitest'
import { renderHook, act, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import React from 'react'

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {}
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => { store[key] = value },
    removeItem: (key: string) => { delete store[key] },
    clear: () => { store = {} },
  }
})()

Object.defineProperty(window, 'localStorage', { value: localStorageMock })

// Mock services before importing
const mockLogin = vi.fn()
const mockLogout = vi.fn(() => {
  // Clear tokens when logout is called
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
})
const mockRegister = vi.fn()
const mockGetProfile = vi.fn()

vi.mock('../../services/api', () => ({
  authService: {
    login: () => mockLogin(),
    logout: () => mockLogout(),
    register: () => mockRegister(),
    getProfile: () => mockGetProfile(),
  },
}))

// Import after mocking
import { useAuth } from '../useAuth'

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })
  return ({ children }: { children: React.ReactNode }) => {
    return React.createElement(QueryClientProvider, { client: queryClient }, children)
  }
}

describe('useAuth', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.clearAllMocks()
    mockGetProfile.mockResolvedValue({
      id: 1,
      email: 'test@example.com',
      username: 'testuser',
      is_verified: true,
      balance: 100000,
      created_at: '2024-01-01',
      updated_at: '2024-01-01',
    })
    mockLogin.mockResolvedValue({
      access: 'mock-access-token',
      refresh: 'mock-refresh-token',
    })
    mockRegister.mockResolvedValue({})
  })

  it('initializes with unauthenticated state when no token exists', async () => {
    const { result } = renderHook(() => useAuth(), { wrapper: createWrapper() })

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.user).toBeNull()
    expect(result.current.isAuthenticated).toBe(false)
  })

  it('initializes with authenticated state when token exists', async () => {
    localStorage.setItem('access_token', 'existing-token')
    
    const { result } = renderHook(() => useAuth(), { wrapper: createWrapper() })

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.isAuthenticated).toBe(true)
    expect(result.current.user).not.toBeNull()
  })

  it('logs in successfully', async () => {
    const { result } = renderHook(() => useAuth(), { wrapper: createWrapper() })

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    await act(async () => {
      await result.current.login('test@example.com', 'password123')
    })

    expect(localStorage.getItem('access_token')).toBe('mock-access-token')
    expect(localStorage.getItem('refresh_token')).toBe('mock-refresh-token')
    expect(result.current.isAuthenticated).toBe(true)
  })

  it('logs out successfully', async () => {
    localStorage.setItem('access_token', 'existing-token')
    const { result } = renderHook(() => useAuth(), { wrapper: createWrapper() })

    await waitFor(() => {
      expect(result.current.isAuthenticated).toBe(true)
    })

    act(() => {
      result.current.logout()
    })

    expect(localStorage.getItem('access_token')).toBeNull()
    expect(localStorage.getItem('refresh_token')).toBeNull()
    expect(result.current.isAuthenticated).toBe(false)
    expect(result.current.user).toBeNull()
  })

  it('registers and auto-logs in', async () => {
    const { result } = renderHook(() => useAuth(), { wrapper: createWrapper() })

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    await act(async () => {
      await result.current.register({
        email: 'newuser@example.com',
        username: 'newuser',
        password: 'password123',
        password_confirm: 'password123',
      })
    })

    expect(result.current.isAuthenticated).toBe(true)
  })

  it('returns auth headers correctly', async () => {
    const { result } = renderHook(() => useAuth(), { wrapper: createWrapper() })

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    let headers = result.current.getAuthHeaders()
    expect(headers.Authorization).toBe('')

    await act(async () => {
      await result.current.login('test@example.com', 'password123')
    })

    headers = result.current.getAuthHeaders()
    expect(headers.Authorization).toBe('Bearer mock-access-token')
  })
})
