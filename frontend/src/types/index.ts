// User Types
export interface User {
  id: number;
  email: string;
  username: string;
  phone_number?: string;
  date_of_birth?: string;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
  phone_number?: string;
}

// Gold Price Types
export interface GoldPrice {
  id: number;
  price_per_gram: number;
  price_per_baht: number;
  currency: string;
  timestamp: string;
  source?: string;
}

// Transaction Types
export type TransactionType = 'BUY' | 'SELL';
export type TransactionStatus = 'PENDING' | 'COMPLETED' | 'CANCELLED';

export interface Transaction {
  id: number;
  user: number;
  transaction_type: TransactionType;
  gold_weight: number;
  gold_price_per_gram: number;
  total_amount: number;
  status: TransactionStatus;
  transaction_date: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTransactionData {
  transaction_type: TransactionType;
  gold_weight: number;
  gold_price_per_gram: number;
}

// Wallet Types
export interface Wallet {
  id: number;
  user: number;
  balance: number;
  gold_holdings: number;
  created_at: string;
  updated_at: string;
}

// API Response Types
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Common Types
export interface ApiError {
  detail: string;
  [key: string]: any;
}
