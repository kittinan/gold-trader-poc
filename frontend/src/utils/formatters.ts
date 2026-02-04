/**
 * Formatters for displaying numbers and currency in the application
 */

/**
 * Format number with specified decimal places
 */
export const formatNumber = (value: number, decimals: number = 2): string => {
  if (value === null || value === undefined) return '0';
  
  return new Intl.NumberFormat('th-TH', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
};

/**
 * Format currency in Thai Baht (THB)
 */
export const formatCurrency = (value: number): string => {
  if (value === null || value === undefined) return '฿0.00';
  
  return new Intl.NumberFormat('th-TH', {
    style: 'currency',
    currency: 'THB',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
};

/**
 * Format percentage
 */
export const formatPercentage = (value: number, decimals: number = 2): string => {
  if (value === null || value === undefined) return '0%';
  
  return `${formatNumber(value, decimals)}%`;
};

/**
 * Format weight in grams
 */
export const formatWeight = (grams: number, decimals: number = 3): string => {
  if (grams === null || grams === undefined) return '0g';
  
  return `${formatNumber(grams, decimals)}g`;
};

/**
 * Format weight in baht (Thai unit)
 * 1 baht = 15.244 grams
 */
export const formatWeightInBaht = (grams: number, decimals: number = 2): string => {
  if (grams === null || grams === undefined) return '0 บาท';
  
  const baht = grams / 15.244;
  return `${formatNumber(baht, decimals)} บาท`;
};

/**
 * Format date in Thai format
 */
export const formatDate = (dateString: string): string => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  
  return new Intl.DateTimeFormat('th-TH', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
};

/**
 * Format date without time
 */
export const formatDateShort = (dateString: string): string => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  
  return new Intl.DateTimeFormat('th-TH', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(date);
};

/**
 * Format transaction type with appropriate styling
 */
export const formatTransactionType = (type: string): string => {
  switch (type.toUpperCase()) {
    case 'BUY':
      return 'Buy';
    case 'SELL':
      return 'Sell';
    default:
      return type;
  }
};

/**
 * Get transaction type color class
 */
export const getTransactionTypeColor = (type: string): string => {
  switch (type.toUpperCase()) {
    case 'BUY':
      return 'text-green-600 bg-green-100';
    case 'SELL':
      return 'text-red-600 bg-red-100';
    default:
      return 'text-gray-600 bg-gray-100';
  }
};

/**
 * Format status with appropriate styling
 */
export const formatStatus = (status: string): string => {
  switch (status.toUpperCase()) {
    case 'PENDING':
      return 'Pending';
    case 'COMPLETED':
      return 'Completed';
    case 'CANCELLED':
      return 'Cancelled';
    default:
      return status;
  }
};

/**
 * Get status color class
 */
export const getStatusColor = (status: string): string => {
  switch (status.toUpperCase()) {
    case 'PENDING':
      return 'text-yellow-600 bg-yellow-100';
    case 'COMPLETED':
      return 'text-green-600 bg-green-100';
    case 'CANCELLED':
      return 'text-red-600 bg-red-100';
    default:
      return 'text-gray-600 bg-gray-100';
  }
};

/**
 * Format large numbers with abbreviations (K, M, B)
 */
export const formatLargeNumber = (value: number): string => {
  if (value === null || value === undefined) return '0';
  
  if (value >= 1000000000) {
    return `${(value / 1000000000).toFixed(1)}B`;
  }
  
  if (value >= 1000000) {
    return `${(value / 1000000).toFixed(1)}M`;
  }
  
  if (value >= 1000) {
    return `${(value / 1000).toFixed(1)}K`;
  }
  
  return formatNumber(value, 0);
};

/**
 * Format time ago (e.g., "2 hours ago", "3 days ago")
 */
export const formatTimeAgo = (dateString: string): string => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  const now = new Date();
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);
  
  const intervals = [
    { label: 'year', seconds: 31536000 },
    { label: 'month', seconds: 2592000 },
    { label: 'week', seconds: 604800 },
    { label: 'day', seconds: 86400 },
    { label: 'hour', seconds: 3600 },
    { label: 'minute', seconds: 60 },
  ];
  
  for (const interval of intervals) {
    const count = Math.floor(seconds / interval.seconds);
    
    if (count >= 1) {
      return `${count} ${interval.label}${count > 1 ? 's' : ''} ago`;
    }
  }
  
  return 'Just now';
};