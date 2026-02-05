import { http, HttpResponse } from 'msw'

const API_BASE_URL = '/api'

// Mock user data
const mockUser = {
  id: 1,
  email: 'test@example.com',
  username: 'testuser',
  phone_number: '0812345678',
  date_of_birth: '1990-01-01',
  is_verified: true,
  balance: 100000,
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
}

// Mock auth tokens
const mockTokens = {
  access: 'mock-access-token',
  refresh: 'mock-refresh-token',
}

// Mock gold price
const mockGoldPrice = {
  id: 1,
  price_per_gram: 2345.50,
  price_per_baht: 35740.00,
  currency: 'THB',
  timestamp: new Date().toISOString(),
  source: 'API',
}

// Mock gold holdings
const mockGoldHoldings = {
  current_holdings: {
    gold_weight_grams: 10.5,
    gold_weight_baht: 0.69,
    average_purchase_price_per_gram: 2300.00,
    average_purchase_price_per_baht: 35000.00,
  },
  market_value: {
    current_price_per_gram: 2345.50,
    current_price_per_baht: 35740.00,
    current_market_value_thb: 24627.75,
    total_cost_thb: 24150.00,
  },
  profit_loss: {
    unrealized_pl_thb: 477.75,
    unrealized_pl_percent: 1.98,
    realized_pl_thb: 0,
    total_pl_thb: 477.75,
  },
  transactions: {
    total_buy_transactions: 3,
    total_sell_transactions: 0,
    recent_transactions: [],
  },
}

// Mock transactions
const mockTransactions = [
  {
    id: 1,
    user: 1,
    transaction_type: 'BUY' as const,
    gold_weight: 5.0,
    gold_price_per_gram: 2300.00,
    total_amount: 11500.00,
    status: 'COMPLETED' as const,
    transaction_date: '2024-01-15T10:00:00Z',
    created_at: '2024-01-15T10:00:00Z',
    updated_at: '2024-01-15T10:00:00Z',
  },
  {
    id: 2,
    user: 1,
    transaction_type: 'BUY' as const,
    gold_weight: 5.5,
    gold_price_per_gram: 2309.09,
    total_amount: 12700.00,
    status: 'COMPLETED' as const,
    transaction_date: '2024-01-16T14:30:00Z',
    created_at: '2024-01-16T14:30:00Z',
    updated_at: '2024-01-16T14:30:00Z',
  },
]

// Mock wallet
const mockWallet = {
  id: 1,
  user: 1,
  balance: 100000,
  gold_holdings: 10.5,
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
}

// Auth handlers
export const authHandlers = [
  http.post(`${API_BASE_URL}/auth/login/`, async ({ request }) => {
    const body = await request.json() as { email: string; password: string }
    
    if (body.email === 'test@example.com' && body.password === 'password123') {
      return HttpResponse.json(mockTokens)
    }
    
    return HttpResponse.json(
      { detail: 'Invalid credentials' },
      { status: 401 }
    )
  }),

  http.post(`${API_BASE_URL}/auth/register/`, async ({ request }) => {
    const body = await request.json()
    
    return HttpResponse.json({ message: 'Registration successful' })
  }),

  http.post(`${API_BASE_URL}/auth/token/refresh/`, async ({ request }) => {
    const body = await request.json() as { refresh: string }
    
    if (body.refresh === 'mock-refresh-token') {
      return HttpResponse.json({ access: 'new-mock-access-token' })
    }
    
    return HttpResponse.json(
      { detail: 'Invalid refresh token' },
      { status: 401 }
    )
  }),

  http.get(`${API_BASE_URL}/auth/profile/`, () => {
    return HttpResponse.json(mockUser)
  }),
]

// Gold price handlers
export const goldPriceHandlers = [
  http.get(`${API_BASE_URL}/gold-prices/latest/`, () => {
    return HttpResponse.json(mockGoldPrice)
  }),

  http.get(`${API_BASE_URL}/gold-prices/`, () => {
    return HttpResponse.json({
      count: 1,
      next: null,
      previous: null,
      results: [mockGoldPrice],
    })
  }),
]

// Transaction handlers
export const transactionHandlers = [
  http.get(`${API_BASE_URL}/transactions/`, ({ request }) => {
    const url = new URL(request.url)
    const userId = url.searchParams.get('user')
    
    return HttpResponse.json({
      count: mockTransactions.length,
      next: null,
      previous: null,
      results: mockTransactions,
    })
  }),

  http.get(`${API_BASE_URL}/gold/transactions/`, ({ request }) => {
    const url = new URL(request.url)
    const userId = url.searchParams.get('user')
    
    return HttpResponse.json({
      count: mockTransactions.length,
      next: null,
      previous: null,
      results: mockTransactions,
    })
  }),

  http.post(`${API_BASE_URL}/gold/trade/`, async ({ request }) => {
    const body = await request.json() as { type: string; amount: number }
    
    const newTransaction = {
      id: mockTransactions.length + 1,
      user: mockUser.id,
      transaction_type: body.type === 'BUY' ? ('BUY' as const) : ('SELL' as const),
      gold_weight: body.amount,
      gold_price_per_gram: mockGoldPrice.price_per_gram,
      total_amount: body.amount * mockGoldPrice.price_per_gram,
      status: 'COMPLETED' as const,
      transaction_date: new Date().toISOString(),
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }
    
    return HttpResponse.json({ transaction: newTransaction })
  }),
]

// Wallet handlers
export const walletHandlers = [
  http.get(`${API_BASE_URL}/wallets/my_wallet/`, () => {
    return HttpResponse.json(mockWallet)
  }),

  http.get(`${API_BASE_URL}/wallets/`, () => {
    return HttpResponse.json({
      count: 1,
      next: null,
      previous: null,
      results: [mockWallet],
    })
  }),
]

// Gold holdings handlers
export const goldHoldingsHandlers = [
  http.get(`${API_BASE_URL}/gold/holdings/`, () => {
    return HttpResponse.json(mockGoldHoldings)
  }),

  http.get(`${API_BASE_URL}/gold-holdings/`, () => {
    return HttpResponse.json(mockGoldHoldings)
  }),
]

// Combine all handlers
export const handlers = [
  ...authHandlers,
  ...goldPriceHandlers,
  ...transactionHandlers,
  ...walletHandlers,
  ...goldHoldingsHandlers,
]
