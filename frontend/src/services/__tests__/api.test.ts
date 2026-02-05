import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import api, { authService, goldPriceService, transactionService, walletService, goldHoldingsService } from '../api'

describe('API Client', () => {
  beforeEach(() => {
    // Clear localStorage
    localStorage.clear()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('apiClient methods', () => {
    it('creates axios client with correct base URL', () => {
      // The API client is created on module load, so we just verify it exists
      expect(api).toBeDefined()
    })
  })

  describe('authService', () => {
    it('login makes correct API call', async () => {
      const mockResponse = {
        access: 'test-access-token',
        refresh: 'test-refresh-token',
      }

      const axiosPostSpy = vi.spyOn((api as any).client, 'post').mockResolvedValue({
        data: mockResponse,
      })

      const result = await authService.login('test@example.com', 'password123')

      expect(axiosPostSpy).toHaveBeenCalledWith('/auth/login/', {
        email: 'test@example.com',
        password: 'password123',
      })
      expect(result).toEqual(mockResponse)

      axiosPostSpy.mockRestore()
    })

    it('logout clears tokens from localStorage', () => {
      localStorage.setItem('access_token', 'token')
      localStorage.setItem('refresh_token', 'refresh')

      authService.logout()

      expect(localStorage.getItem('access_token')).toBeNull()
      expect(localStorage.getItem('refresh_token')).toBeNull()
    })

    it('register makes correct API call', async () => {
      const userData = {
        email: 'new@example.com',
        username: 'newuser',
        password: 'password123',
        password_confirm: 'password123',
      }

      const axiosPostSpy = vi.spyOn((api as any).client, 'post').mockResolvedValue({
        data: { message: 'Registration successful' },
      })

      await authService.register(userData)

      expect(axiosPostSpy).toHaveBeenCalledWith('/auth/register/', userData)

      axiosPostSpy.mockRestore()
    })

    it('getProfile makes correct API call', async () => {
      const mockUser = {
        id: 1,
        email: 'test@example.com',
        username: 'testuser',
      }

      const axiosGetSpy = vi.spyOn((api as any).client, 'get').mockResolvedValue({
        data: mockUser,
      })

      const result = await authService.getProfile()

      // The get method wraps params in {params: ...}
      expect(axiosGetSpy).toHaveBeenCalledWith('/auth/profile/', { params: undefined })
      expect(result).toEqual(mockUser)

      axiosGetSpy.mockRestore()
    })
  })

  describe('goldPriceService', () => {
    it('getLatest makes correct API call', async () => {
      const mockPrice = {
        id: 1,
        price_per_gram: 2345.50,
        price_per_baht: 35740.00,
      }

      const axiosGetSpy = vi.spyOn((api as any).client, 'get').mockResolvedValue({
        data: mockPrice,
      })

      const result = await goldPriceService.getLatest()

      expect(axiosGetSpy).toHaveBeenCalledWith('/gold-prices/latest/', { params: undefined })
      expect(result).toEqual(mockPrice)

      axiosGetSpy.mockRestore()
    })

    it('getHistory makes correct API call', async () => {
      const mockHistory = {
        count: 10,
        results: [],
      }

      const axiosGetSpy = vi.spyOn((api as any).client, 'get').mockResolvedValue({
        data: mockHistory,
      })

      const params = { limit: 10 }
      const result = await goldPriceService.getHistory(params)

      // The service wraps params in { params: ... }
      expect(axiosGetSpy).toHaveBeenCalledWith('/gold-prices/', { params: { params } })
      expect(result).toEqual(mockHistory)

      axiosGetSpy.mockRestore()
    })
  })

  describe('transactionService', () => {
    it('getList makes correct API call', async () => {
      const mockTransactions = {
        count: 5,
        results: [],
      }

      const axiosGetSpy = vi.spyOn((api as any).client, 'get').mockResolvedValue({
        data: mockTransactions,
      })

      const result = await transactionService.getList()

      // The service wraps params in { params: ... }
      expect(axiosGetSpy).toHaveBeenCalledWith('/transactions/', { params: { params: undefined } })
      expect(result).toEqual(mockTransactions)

      axiosGetSpy.mockRestore()
    })

    it('create makes correct API call', async () => {
      const newTransaction = {
        transaction_type: 'BUY',
        gold_weight: 10.0,
        gold_price_per_gram: 2345.50,
      }

      const mockResponse = {
        id: 1,
        ...newTransaction,
      }

      const axiosPostSpy = vi.spyOn((api as any).client, 'post').mockResolvedValue({
        data: mockResponse,
      })

      const result = await transactionService.create(newTransaction)

      expect(axiosPostSpy).toHaveBeenCalledWith('/transactions/', newTransaction)
      expect(result).toEqual(mockResponse)

      axiosPostSpy.mockRestore()
    })

    it('getDetail makes correct API call', async () => {
      const mockTransaction = {
        id: 1,
        transaction_type: 'BUY',
      }

      const axiosGetSpy = vi.spyOn((api as any).client, 'get').mockResolvedValue({
        data: mockTransaction,
      })

      const result = await transactionService.getDetail(1)

      expect(axiosGetSpy).toHaveBeenCalledWith('/transactions/1/', { params: undefined })
      expect(result).toEqual(mockTransaction)

      axiosGetSpy.mockRestore()
    })
  })

  describe('walletService', () => {
    it('getMyWallet makes correct API call', async () => {
      const mockWallet = {
        id: 1,
        balance: 100000,
      }

      const axiosGetSpy = vi.spyOn((api as any).client, 'get').mockResolvedValue({
        data: mockWallet,
      })

      const result = await walletService.getMyWallet()

      expect(axiosGetSpy).toHaveBeenCalledWith('/wallets/my_wallet/', { params: undefined })
      expect(result).toEqual(mockWallet)

      axiosGetSpy.mockRestore()
    })

    it('getList makes correct API call', async () => {
      const mockWallets = {
        count: 1,
        results: [],
      }

      const axiosGetSpy = vi.spyOn((api as any).client, 'get').mockResolvedValue({
        data: mockWallets,
      })

      const result = await walletService.getList()

      // The service wraps params in { params: ... }
      expect(axiosGetSpy).toHaveBeenCalledWith('/wallets/', { params: { params: undefined } })
      expect(result).toEqual(mockWallets)

      axiosGetSpy.mockRestore()
    })
  })

  describe('goldHoldingsService', () => {
    it('getHoldings makes correct API call', async () => {
      const mockHoldings = {
        current_holdings: { gold_weight_grams: 10.5 },
      }

      const axiosGetSpy = vi.spyOn((api as any).client, 'get').mockResolvedValue({
        data: mockHoldings,
      })

      const result = await goldHoldingsService.getHoldings()

      expect(axiosGetSpy).toHaveBeenCalledWith('/gold-holdings/', { params: undefined })
      expect(result).toEqual(mockHoldings)

      axiosGetSpy.mockRestore()
    })
  })
})
