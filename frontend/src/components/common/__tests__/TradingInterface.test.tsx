import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

vi.mock('../../../services/websocket', () => ({
  default: {
    connect: vi.fn(),
    disconnect: vi.fn(),
  },
}))

vi.mock('../../../services/api', () => ({
  default: {
    post: vi.fn(),
  },
}))

import TradingInterface from '../TradingInterface'
import api from '../../../services/api'
import wsService from '../../../services/websocket'

describe('TradingInterface', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders trading form', () => {
    render(<TradingInterface />)

    expect(screen.getByText('Trading')).toBeInTheDocument()
    expect(screen.getByText('Price: ฿0.00/g')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Grams')).toBeInTheDocument()
    expect(screen.getByText('Place Order')).toBeInTheDocument()
  })

  it('connects to websocket on mount', () => {
    render(<TradingInterface />)
    expect(wsService.connect).toHaveBeenCalledTimes(1)
  })

  it('disconnects from websocket on unmount', () => {
    const { unmount } = render(<TradingInterface />)
    unmount()
    expect(wsService.disconnect).toHaveBeenCalledTimes(1)
  })

  it('handles input changes', async () => {
    const user = userEvent.setup()
    render(<TradingInterface />)

    const input = screen.getByPlaceholderText('Grams')
    await user.type(input, '10.5')

    expect(input).toHaveValue(10.5)
  })

  it('disables button while processing', async () => {
    vi.mocked(api.post).mockImplementation(
      () => new Promise(() => {}) // Never resolves
    )

    const user = userEvent.setup()
    render(<TradingInterface />)

    const input = screen.getByPlaceholderText('Grams')
    await user.type(input, '10')

    const button = screen.getByText('Place Order')
    await user.click(button)

    await waitFor(() => {
      expect(button).toBeDisabled()
      expect(button).toHaveTextContent('Processing...')
    })
  })

  it('calls onTradeComplete after successful trade', async () => {
    const mockTransaction = {
      id: 1,
      transaction_type: 'BUY',
      gold_weight: 10,
      total_amount: 23455,
    }

    vi.mocked(api.post).mockResolvedValue({
      data: { transaction: mockTransaction },
    })

    const onTradeComplete = vi.fn()
    const user = userEvent.setup()
    render(<TradingInterface onTradeComplete={onTradeComplete} />)

    const input = screen.getByPlaceholderText('Grams')
    await user.type(input, '10')

    const button = screen.getByText('Place Order')
    await user.click(button)

    await waitFor(() => {
      expect(onTradeComplete).toHaveBeenCalledWith(mockTransaction)
    })
  })

  it('handles API error gracefully', async () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
    vi.mocked(api.post).mockRejectedValue(new Error('Network error'))

    const user = userEvent.setup()
    render(<TradingInterface />)

    const input = screen.getByPlaceholderText('Grams')
    await user.type(input, '10')

    const button = screen.getByText('Place Order')
    await user.click(button)

    await waitFor(() => {
      expect(button).not.toBeDisabled()
      expect(button).toHaveTextContent('Place Order')
    })

    expect(consoleSpy).toHaveBeenCalled()
    consoleSpy.mockRestore()
  })
})
