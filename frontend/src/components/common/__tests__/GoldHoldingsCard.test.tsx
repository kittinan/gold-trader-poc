import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import GoldHoldingsCard from '../GoldHoldingsCard'

// Mock the api service
vi.mock('../../../services/api', async () => {
  const actual = await vi.importActual<any>('../../../services/api')
  return {
    ...actual,
    default: {
      get: vi.fn(),
    },
  }
})

import api from '../../../services/api'

const mockHoldingsData = {
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

describe('GoldHoldingsCard', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders loading state', () => {
    vi.mocked(api.get).mockImplementation(
      () => new Promise(() => {}) // Never resolves to keep loading state
    )

    render(<GoldHoldingsCard />, { wrapper: createWrapper() })
    expect(screen.getByText('Loading card...')).toBeInTheDocument()
  })

  it('renders error state on API failure', async () => {
    vi.mocked(api.get).mockRejectedValue(new Error('Network error'))

    render(<GoldHoldingsCard />, { wrapper: createWrapper() })

    await screen.findByText('Error: Network error')
  })

  it('renders holdings data successfully', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: mockHoldingsData })

    render(<GoldHoldingsCard />, { wrapper: createWrapper() })

    await screen.findByText('Gold Portfolio')
    await screen.findByText(/฿24,627\.75/)
    await screen.findByText(/10\.500g/)
  })

  it('renders with custom className', async () => {
    vi.mocked(api.get).mockResolvedValue({ data: mockHoldingsData })

    const { container } = render(
      <GoldHoldingsCard className="custom-class" />,
      { wrapper: createWrapper() }
    )

    await screen.findByText('Gold Portfolio')
    expect(container.firstChild).toHaveClass('custom-class')
  })
})
