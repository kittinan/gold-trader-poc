// Test fixtures for E2E tests

export const TEST_USERS = {
  new: {
    email: 'testuser@example.com',
    password: 'TestPassword123!',
    firstName: 'Test',
    lastName: 'User'
  },
  existing: {
    email: 'existinguser@example.com',
    password: 'ExistingPassword123!',
    firstName: 'Existing',
    lastName: 'User'
  },
  invalid: {
    email: 'invalid@example.com',
    password: 'WrongPassword123!'
  }
};

export const TEST_DATA = {
  goldTrades: {
    small: {
      amount: 0.1,
      expectedPriceRange: { min: 5000, max: 10000 }
    },
    medium: {
      amount: 1,
      expectedPriceRange: { min: 50000, max: 100000 }
    },
    large: {
      amount: 5,
      expectedPriceRange: { min: 250000, max: 500000 }
    }
  },
  deposits: {
    small: 1000,
    medium: 10000,
    large: 100000
  }
};

export const API_ENDPOINTS = {
  auth: {
    login: '/api/auth/login/',
    register: '/api/auth/register/',
    refresh: '/api/auth/refresh/'
  },
  trading: {
    goldPrice: '/api/trading/gold-price/',
    buyGold: '/api/trading/buy/',
    sellGold: '/api/trading/sell/',
    transactions: '/api/trading/transactions/'
  },
  wallet: {
    balance: '/api/wallet/balance/',
    deposit: '/api/wallet/deposit/',
    history: '/api/wallet/history/'
  }
};

export const SELECTORS = {
  common: {
    loadingSpinner: '[data-testid="loading"], .spinner',
    errorMessage: '[data-testid="error"], .alert-error',
    successMessage: '[data-testid="success"], .alert-success'
  },
  auth: {
    loginForm: '[data-testid="login-form"], form:has-text("Login")',
    registerForm: '[data-testid="register-form"], form:has-text("Register")'
  }
};