import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import TradeHistory from '../TradeHistory'

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
    transaction_type: 'SELL' as const,
    gold_weight: 3.0,
    gold_price_per_gram: 2350.00,
    total_amount: 7050.00,
    status: 'COMPLETED' as const,
    transaction_date: '2024-01-16T14:30:00Z',
    created_at: '2024-01-16T14:30:00Z',
    updated_at: '2024-01-16T14:30:00Z',
  },
]

describe('TradeHistory', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders loading state initially', () => {
    vi.mocked(api.get).mockImplementation(
      () => new Promise(() => {})
    )

    render(<TradeHistory />)
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('renders transactions successfully', async () => {
    vi.mocked(api.get).mockResolvedValue({
      data: mockTransactions,
    })

    render(<TradeHistory />)

    await waitFor(() => {
      expect(screen.getByText('Trade History')).toBeInTheDocument()
    })

    expect(screen.getByText('BUY')).toBeInTheDocument()
    expect(screen.getByText('SELL')).toBeInTheDocument()
    expect(screen.getByText('5.000g')).toBeInTheDocument()
    expect(screen.getByText('฿11,500.00')).toBeInTheDocument()
  })

  it('renders paginated response correctly', async () => {
    vi.mocked(api.get).mockResolvedValue({
      data: {
        count: 2,
        next: null,
        previous: null,
        results: mockTransactions,
      },
    })

    render(<TradeHistory />)

    await waitFor(() => {
      expect(screen.getByText('Trade History')).toBeInTheDocument()
    })

    expect(screen.getByText('BUY')).toBeInTheDocument()
    expect(screen.getByText('SELL')).toBeInTheDocument()
  })

  it('renders with custom className', async () => {
    vi.mocked(api.get).mockResolvedValue({
      data: mockTransactions,
    })

    const { container } = render(<TradeHistory className="custom-class" />)

    await screen.findByText('Trade History')
    expect(container.firstChild).toHaveClass('custom-class')
  })

  it('refetches when refreshTrigger changes', async () => {
    vi.mocked(api.get).mockResolvedValue({
      data: mockTransactions,
    })

    const { rerender } = render(<TradeHistory refreshTrigger={0} />)

    await screen.findByText('Trade History')
    expect(api.get).toHaveBeenCalledTimes(1)

    rerender(<TradeHistory refreshTrigger={1} />)

    await waitFor(() => {
      expect(api.get).toHaveBeenCalledTimes(2)
    })
  })

  it('passes userId to API call', async () => {
    vi.mocked(api.get).mockResolvedValue({
      data: mockTransactions,
    })

    render(<TradeHistory userId={123} />)

    await screen.findByText('Trade History')
    expect(api.get).toHaveBeenCalledWith('/gold/transactions/', { user: 123 })
  })

  it('handles API errors gracefully', async () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
    vi.mocked(api.get).mockRejectedValue(new Error('Network error'))

    render(<TradeHistory />)

    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument()
    })

    expect(consoleSpy).toHaveBeenCalled()
    consoleSpy.mockRestore()
  })

  it('displays formatted dates and amounts', async () => {
    vi.mocked(api.get).mockResolvedValue({
      data: mockTransactions,
    })

    render(<TradeHistory />)

    await waitFor(() => {
      expect(screen.getByText('Trade History')).toBeInTheDocument()
    })

    expect(screen.getByText('5.000g')).toBeInTheDocument()
    expect(screen.getByText('฿11,500.00')).toBeInTheDocument()
    expect(screen.getByText('3.000g')).toBeInTheDocument()
    expect(screen.getByText('฿7,050.00')).toBeInTheDocument()
  })
})
