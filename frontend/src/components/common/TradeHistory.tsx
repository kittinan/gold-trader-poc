import { useState, useEffect, useCallback } from 'react';
import { transactionService } from '../services/api';
import { useWebSocket } from '../services/websocket';
import { Transaction, TransactionType, TransactionStatus } from '../types';
import { formatCurrency, formatNumber, formatDateTime } from '../utils/formatters';

interface TradeHistoryProps {
  className?: string;
  refreshTrigger?: number;
  userId?: number;
}

const TradeHistory: React.FC<TradeHistoryProps> = ({ 
  className = '', 
  refreshTrigger,
  userId 
}) => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'buy' | 'sell'>('all');
  const [statusFilter, setStatusFilter] = useState<'all' | 'pending' | 'completed' | 'cancelled'>('all');

  const { subscribeToEvent } = useWebSocket();

  // Fetch transactions
  const fetchTransactions = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const params: any = {};
      if (userId) params.user = userId;
      
      const response = await transactionService.getList(params);
      setTransactions(response.results || []);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch transactions');
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchTransactions();
  }, [fetchTransactions, refreshTrigger]);

  // Handle WebSocket trade updates
  const handleTradeUpdate = useCallback((data: any) => {
    // Update transactions list when new trade occurs
    setTransactions(prev => {
      const existingIndex = prev.findIndex(t => t.id === data.id);
      
      if (existingIndex >= 0) {
        // Update existing transaction
        const updated = [...prev];
        updated[existingIndex] = {
          ...updated[existingIndex],
          status: data.status,
          updated_at: data.timestamp
        };
        return updated;
      } else {
        // Add new transaction
        const newTransaction: Transaction = {
          id: data.transaction_id,
          user: data.user_id,
          transaction_type: data.transaction_type,
          gold_weight: data.gold_weight,
          gold_price_per_gram: data.gold_price_per_gram,
          total_amount: data.total_amount,
          status: data.status,
          transaction_date: data.timestamp,
          created_at: data.timestamp,
          updated_at: data.timestamp
        };
        return [newTransaction, ...prev];
      }
    });
  }, []);

  // Subscribe to WebSocket trade updates
  useEffect(() => {
    const handleTradeEvent = (event: CustomEvent) => {
      handleTradeUpdate(event.detail);
    };

    window.addEventListener('ws_trade_update', handleTradeEvent as EventListener);

    return () => {
      window.removeEventListener('ws_trade_update', handleTradeEvent as EventListener);
    };
  }, [handleTradeUpdate]);

  // Filter transactions
  const filteredTransactions = transactions.filter(transaction => {
    if (filter !== 'all' && transaction.transaction_type !== filter.toUpperCase()) {
      return false;
    }
    
    if (statusFilter !== 'all' && transaction.status !== statusFilter.toUpperCase()) {
      return false;
    }
    
    return true;
  });

  // Sort transactions by date (newest first)
  const sortedTransactions = [...filteredTransactions].sort(
    (a, b) => new Date(b.transaction_date).getTime() - new Date(a.transaction_date).getTime()
  );

  const getStatusColor = (status: TransactionStatus) => {
    switch (status) {
      case 'COMPLETED':
        return 'text-green-600 bg-green-100';
      case 'PENDING':
        return 'text-yellow-600 bg-yellow-100';
      case 'CANCELLED':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getTypeColor = (type: TransactionType) => {
    switch (type) {
      case 'BUY':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'SELL':
        return 'text-red-600 bg-red-50 border-red-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  if (loading && transactions.length === 0) {
    return (
      <div className={`bg-white rounded-xl shadow-sm border border-gray-200 p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
          {[1, 2, 3].map((i) => (
            <div key={i} className="border-t border-gray-200 pt-4 mb-4">
              <div className="grid grid-cols-4 gap-4">
                {[1, 2, 3, 4].map((j) => (
                  <div key={j} className="h-4 bg-gray-200 rounded"></div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <h3 className="text-lg font-semibold text-gray-900 mb-2 sm:mb-0">
            Trade History
          </h3>
          
          {/* Filters */}
          <div className="flex flex-wrap gap-2">
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value as any)}
              className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="all">All Types</option>
              <option value="buy">Buy Only</option>
              <option value="sell">Sell Only</option>
            </select>
            
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as any)}
              className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="all">All Status</option>
              <option value="pending">Pending</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </select>
            
            <button
              onClick={fetchTransactions}
              className="px-3 py-1 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700 transition-colors"
            >
              Refresh
            </button>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mx-6 mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {/* Transactions List */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date & Time
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Quantity
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Price
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Total
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {sortedTransactions.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-6 py-8 text-center text-gray-500">
                  <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  <p className="text-lg font-medium text-gray-900 mb-1">No transactions found</p>
                  <p className="text-sm">Start trading to see your transaction history here.</p>
                </td>
              </tr>
            ) : (
              sortedTransactions.map((transaction) => (
                <tr key={transaction.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {formatDateTime(transaction.transaction_date)}
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full border ${getTypeColor(transaction.transaction_type)}`}>
                      {transaction.transaction_type}
                    </span>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {formatNumber(transaction.gold_weight, 4)}g
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      ฿{formatNumber(transaction.gold_price_per_gram, 2)}
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      ฿{formatCurrency(transaction.total_amount)}
                    </div>
                  </td>
                  
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(transaction.status)}`}>
                      {transaction.status}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Summary Footer */}
      {transactions.length > 0 && (
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="text-gray-500">Total Trades:</span>
              <span className="ml-2 font-medium text-gray-900">{transactions.length}</span>
            </div>
            <div>
              <span className="text-gray-500">Buy Trades:</span>
              <span className="ml-2 font-medium text-green-600">
                {transactions.filter(t => t.transaction_type === 'BUY').length}
              </span>
            </div>
            <div>
              <span className="text-gray-500">Sell Trades:</span>
              <span className="ml-2 font-medium text-red-600">
                {transactions.filter(t => t.transaction_type === 'SELL').length}
              </span>
            </div>
            <div>
              <span className="text-gray-500">Completed:</span>
              <span className="ml-2 font-medium text-green-600">
                {transactions.filter(t => t.status === 'COMPLETED').length}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TradeHistory;