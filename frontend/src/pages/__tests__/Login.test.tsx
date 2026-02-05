import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Login } from '../Login'

// Mock useAuth hook
vi.mock('../../hooks/useAuth', () => ({
  useAuth: vi.fn(),
}))

import { useAuth } from '../../hooks/useAuth'

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  )
}

describe('Login', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders login form', () => {
    vi.mocked(useAuth).mockReturnValue({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
      checkAuth: vi.fn(),
      getAuthHeaders: vi.fn(),
    })

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>,
      { wrapper: createWrapper() }
    )

    expect(screen.getByText('Sign in to your account')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Email address')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument()
    expect(screen.getByText('Sign in')).toBeInTheDocument()
  })

  it('has link to register page', () => {
    vi.mocked(useAuth).mockReturnValue({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
      checkAuth: vi.fn(),
      getAuthHeaders: vi.fn(),
    })

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>,
      { wrapper: createWrapper() }
    )

    const registerLink = screen.getByText('create a new account')
    expect(registerLink).toBeInTheDocument()
    expect(registerLink.closest('a')).toHaveAttribute('href', '/register')
  })

  it('allows user to type email and password', async () => {
    const user = userEvent.setup()
    vi.mocked(useAuth).mockReturnValue({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
      checkAuth: vi.fn(),
      getAuthHeaders: vi.fn(),
    })

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>,
      { wrapper: createWrapper() }
    )

    const emailInput = screen.getByPlaceholderText('Email address')
    const passwordInput = screen.getByPlaceholderText('Password')

    await user.type(emailInput, 'test@example.com')
    await user.type(passwordInput, 'password123')

    expect(emailInput).toHaveValue('test@example.com')
    expect(passwordInput).toHaveValue('password123')
  })

  it('calls login function with correct credentials', async () => {
    const user = userEvent.setup()
    const mockLogin = vi.fn().mockResolvedValue(undefined)

    vi.mocked(useAuth).mockReturnValue({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      login: mockLogin,
      register: vi.fn(),
      logout: vi.fn(),
      checkAuth: vi.fn(),
      getAuthHeaders: vi.fn(),
    })

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>,
      { wrapper: createWrapper() }
    )

    const emailInput = screen.getByPlaceholderText('Email address')
    const passwordInput = screen.getByPlaceholderText('Password')
    const submitButton = screen.getByText('Sign in')

    await user.type(emailInput, 'test@example.com')
    await user.type(passwordInput, 'password123')
    await user.click(submitButton)

    expect(mockLogin).toHaveBeenCalledWith('test@example.com', 'password123')
  })

  it('shows error message on login failure', async () => {
    const user = userEvent.setup()
    const mockLogin = vi.fn().mockRejectedValue({
      response: { data: { detail: 'Invalid credentials' } },
    })

    vi.mocked(useAuth).mockReturnValue({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      login: mockLogin,
      register: vi.fn(),
      logout: vi.fn(),
      checkAuth: vi.fn(),
      getAuthHeaders: vi.fn(),
    })

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>,
      { wrapper: createWrapper() }
    )

    const emailInput = screen.getByPlaceholderText('Email address')
    const passwordInput = screen.getByPlaceholderText('Password')
    const submitButton = screen.getByText('Sign in')

    await user.type(emailInput, 'test@example.com')
    await user.type(passwordInput, 'wrongpassword')
    await user.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText('Invalid credentials')).toBeInTheDocument()
    })
  })

  it('disables submit button while loading', async () => {
    const user = userEvent.setup()
    const mockLogin = vi.fn().mockImplementation(
      () => new Promise(() => {}) // Never resolves
    )

    vi.mocked(useAuth).mockReturnValue({
      user: null,
      isAuthenticated: false,
      isLoading: true,
      login: mockLogin,
      register: vi.fn(),
      logout: vi.fn(),
      checkAuth: vi.fn(),
      getAuthHeaders: vi.fn(),
    })

    render(
      <MemoryRouter>
        <Login />
      </MemoryRouter>,
      { wrapper: createWrapper() }
    )

    const submitButton = screen.getByText('Signing in...')

    expect(submitButton).toBeDisabled()
  })

  it('redirects to dashboard when already authenticated', () => {
    vi.mocked(useAuth).mockReturnValue({
      user: { id: 1, email: 'test@example.com' } as any,
      isAuthenticated: true,
      isLoading: false,
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
      checkAuth: vi.fn(),
      getAuthHeaders: vi.fn(),
    })

    const { container } = render(
      <MemoryRouter initialEntries={['/login']}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<div>Dashboard</div>} />
        </Routes>
      </MemoryRouter>,
      { wrapper: createWrapper() }
    )

    expect(screen.getByText('Dashboard')).toBeInTheDocument()
  })
})
