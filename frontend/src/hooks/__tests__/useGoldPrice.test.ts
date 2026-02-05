import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'
import { renderHook, waitFor, act } from '@testing-library/react'

const mockGoldPrice = {
  id: 1,
  price_per_gram: 2345.50,
  price_per_baht: 35740.00,
  currency: 'THB',
  timestamp: '2024-01-15T10:00:00Z',
  source: 'API',
}

vi.mock('../../services/api', () => ({
  goldPriceService: {
    getLatest: vi.fn(),
    getHistory: vi.fn(),
  },
}))

import { useGoldPrice } from '../useGoldPrice'
import { goldPriceService } from '../../services/api'

describe('useGoldPrice', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(goldPriceService.getLatest).mockResolvedValue(mockGoldPrice)
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  it('fetches gold price on mount', async () => {
    const { result } = renderHook(() => useGoldPrice())

    expect(result.current.isLoading).toBe(true)

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.goldPrice).toEqual(mockGoldPrice)
    expect(result.current.error).toBeNull()
    expect(goldPriceService.getLatest).toHaveBeenCalledTimes(1)
  })

  it('handles fetch error', async () => {
    vi.mocked(goldPriceService.getLatest).mockRejectedValue(new Error('Network error'))

    const { result } = renderHook(() => useGoldPrice())

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.goldPrice).toBeNull()
    expect(result.current.error).toBe('Network error')
  })

  it('refetches gold price when calling refetch', async () => {
    const { result } = renderHook(() => useGoldPrice())

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(goldPriceService.getLatest).toHaveBeenCalledTimes(1)

    // Call refetch
    await act(async () => {
      await result.current.refetch()
    })

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(goldPriceService.getLatest).toHaveBeenCalledTimes(2)
  })
})
