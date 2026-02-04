import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import api from '../../services/api';
import type { GoldHoldingsData } from '../../types';
import { formatCurrency, formatNumber } from '../../utils/formatters';

interface GoldHoldingsCardProps {
  className?: string;
}

const GoldHoldingsCard: React.FC<GoldHoldingsCardProps> = ({ className = '' }) => {
  const [holdingsData, setHoldingsData] = useState<GoldHoldingsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHoldings = async () => {
      try {
        setLoading(true);
        setError(null);
        const res = await api.get('/gold/holdings/');
        // Transform API response to match GoldHoldingsData if needed or just handle it
        setHoldingsData(res.data);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch gold holdings');
      } finally {
        setLoading(false);
      }
    };

    fetchHoldings();
  }, []);

  if (loading) return <div className={className}>Loading card...</div>;
  if (error) return <div className={className}>Error: {error}</div>;
  if (!holdingsData) return null;

  return (
    <div className={`bg-white rounded-xl shadow-lg overflow-hidden ${className}`}>
      <div className="bg-gradient-to-r from-yellow-500 to-yellow-600 px-6 py-4 text-white font-bold">
        Gold Portfolio
      </div>
      <div className="p-6">
        <div className="text-2xl font-bold">฿{formatCurrency(holdingsData.market_value?.current_market_value_thb || 0)}</div>
        <div className="text-sm text-gray-500">{formatNumber(holdingsData.current_holdings?.gold_weight_grams || 0, 3)}g</div>
      </div>
    </div>
  );
};

export default GoldHoldingsCard;
