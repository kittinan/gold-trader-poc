import React, { useState, useEffect, useCallback } from 'react';
import api from '../../services/api';
import type { Transaction } from '../../types';
import { formatNumber, formatDate } from '../../utils/formatters';

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

  const fetchTransactions = useCallback(async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (userId) params.user = userId;
      const response = await api.get('/gold/transactions/', params);
      setTransactions(Array.isArray(response.data) ? response.data : (response.data.results || []));
    } catch (err: any) {
      console.error('Failed to fetch transactions', err);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchTransactions();
  }, [fetchTransactions, refreshTrigger]);

  if (loading && transactions.length === 0) return <div>Loading...</div>;

  return (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-200 ${className}`}>
      <div className="px-6 py-4 border-b border-gray-200 font-bold">Trade History</div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <tbody>
            {transactions.map((t) => (
              <tr key={t.id} className="border-b">
                <td className="p-4">{formatDate(t.transaction_date)}</td>
                <td className="p-4 font-bold">{t.transaction_type}</td>
                <td className="p-4">{formatNumber(t.gold_weight, 3)}g</td>
                <td className="p-4">฿{formatNumber(t.total_amount, 2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TradeHistory;
