import { describe, it, expect } from 'vitest'
import {
  formatNumber,
  formatCurrency,
  formatPercentage,
  formatWeight,
  formatWeightInBaht,
  formatDate,
  formatDateShort,
  formatTransactionType,
  getTransactionTypeColor,
  formatStatus,
  getStatusColor,
  formatLargeNumber,
  formatTimeAgo,
} from '../formatters'

describe('formatNumber', () => {
  it('formats numbers with specified decimals', () => {
    expect(formatNumber(1234.5678, 2)).toBe('1,234.57')
    expect(formatNumber(1234.5, 1)).toBe('1,234.5')
    expect(formatNumber(1000000, 0)).toBe('1,000,000')
  })

  it('handles null and undefined', () => {
    expect(formatNumber(null, 2)).toBe('0')
    expect(formatNumber(undefined, 2)).toBe('0')
  })
})

describe('formatCurrency', () => {
  it('formats currency in THB', () => {
    expect(formatCurrency(1234.56)).toBe('฿1,234.56')
    expect(formatCurrency(1000000)).toBe('฿1,000,000.00')
  })

  it('handles null and undefined', () => {
    expect(formatCurrency(null)).toBe('฿0.00')
    expect(formatCurrency(undefined)).toBe('฿0.00')
  })
})

describe('formatPercentage', () => {
  it('formats percentages', () => {
    expect(formatPercentage(12.5)).toBe('12.50%')
    expect(formatPercentage(100)).toBe('100.00%')
  })

  it('handles negative percentages', () => {
    expect(formatPercentage(-12.5)).toBe('-12.50%')
  })
})

describe('formatWeight', () => {
  it('formats weight in grams', () => {
    expect(formatWeight(10.5, 3)).toBe('10.500g')
    expect(formatWeight(1.2345, 4)).toBe('1.2345g')
  })

  it('handles null and undefined', () => {
    expect(formatWeight(null)).toBe('0g')
    expect(formatWeight(undefined)).toBe('0g')
  })
})

describe('formatWeightInBaht', () => {
  it('formats weight in baht (Thai unit)', () => {
    // 1 baht = 15.244 grams
    expect(formatWeightInBaht(15.244)).toBe('1.00 บาท')
    expect(formatWeightInBaht(30.488)).toBe('2.00 บาท')
  })
})

describe('formatDate', () => {
  it('formats date in Thai format', () => {
    const dateStr = '2024-01-15T10:30:00Z'
    const formatted = formatDate(dateStr)
    expect(formatted).toMatch(/\d+ .* \d{4}/) // e.g., 15 ม.ค. 2567
    expect(formatted).toMatch(/\d{2}:\d{2}/) // Should include time
  })

  it('handles empty date', () => {
    expect(formatDate('')).toBe('')
  })
})

describe('formatDateShort', () => {
  it('formats date without time', () => {
    const dateStr = '2024-01-15T10:30:00Z'
    const formatted = formatDateShort(dateStr)
    expect(formatted).toMatch(/\d+ .* \d{4}/)
    expect(formatted).not.toMatch(/\d{2}:\d{2}/)
  })
})

describe('formatTransactionType', () => {
  it('formats transaction type', () => {
    expect(formatTransactionType('BUY')).toBe('Buy')
    expect(formatTransactionType('SELL')).toBe('Sell')
    expect(formatTransactionType('OTHER')).toBe('OTHER')
  })
})

describe('getTransactionTypeColor', () => {
  it('returns correct color class for transaction type', () => {
    expect(getTransactionTypeColor('BUY')).toBe('text-green-600 bg-green-100')
    expect(getTransactionTypeColor('SELL')).toBe('text-red-600 bg-red-100')
    expect(getTransactionTypeColor('OTHER')).toBe('text-gray-600 bg-gray-100')
  })
})

describe('formatStatus', () => {
  it('formats status', () => {
    expect(formatStatus('PENDING')).toBe('Pending')
    expect(formatStatus('COMPLETED')).toBe('Completed')
    expect(formatStatus('CANCELLED')).toBe('Cancelled')
    expect(formatStatus('OTHER')).toBe('OTHER')
  })
})

describe('getStatusColor', () => {
  it('returns correct color class for status', () => {
    expect(getStatusColor('PENDING')).toBe('text-yellow-600 bg-yellow-100')
    expect(getStatusColor('COMPLETED')).toBe('text-green-600 bg-green-100')
    expect(getStatusColor('CANCELLED')).toBe('text-red-600 bg-red-100')
  })
})

describe('formatLargeNumber', () => {
  it('formats large numbers with abbreviations', () => {
    expect(formatLargeNumber(500)).toBe('500')
    expect(formatLargeNumber(1500)).toBe('1.5K')
    expect(formatLargeNumber(1500000)).toBe('1.5M')
    expect(formatLargeNumber(2000000000)).toBe('2.0B')
  })
})

describe('formatTimeAgo', () => {
  it('formats time ago for various intervals', () => {
    const now = new Date()
    
    // 5 minutes ago
    const fiveMinsAgo = new Date(now.getTime() - 5 * 60 * 1000)
    expect(formatTimeAgo(fiveMinsAgo.toISOString())).toBe('5 minutes ago')
    
    // 2 hours ago
    const twoHoursAgo = new Date(now.getTime() - 2 * 60 * 60 * 1000)
    expect(formatTimeAgo(twoHoursAgo.toISOString())).toBe('2 hours ago')
    
    // 3 days ago
    const threeDaysAgo = new Date(now.getTime() - 3 * 24 * 60 * 60 * 1000)
    expect(formatTimeAgo(threeDaysAgo.toISOString())).toBe('3 days ago')
  })

  it('handles empty date', () => {
    expect(formatTimeAgo('')).toBe('')
  })
})
