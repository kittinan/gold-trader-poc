import { useState, useEffect } from 'react';
import { goldHoldingsService } from '../services/api';
import { GoldHoldingsData } from '../types';
import { formatCurrency, formatNumber } from '../utils/formatters';

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
        const data = await goldHoldingsService.getHoldings();
        setHoldingsData(data);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch gold holdings');
      } finally {
        setLoading(false);
      }
    };

    fetchHoldings();
  }, []);

  const getPLColor = (value: number) => {
    if (value > 0) return 'text-green-600';
    if (value < 0) return 'text-red-600';
    return 'text-gray-600';
  };

  const getPLSign = (value: number) => {
    if (value > 0) return '+';
    if (value < 0) return '-';
    return '';
  };

  if (loading) {
    return (
      <div className={`bg-white rounded-xl shadow-lg p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-gray-50 rounded-lg p-4">
                <div className="h-4 bg-gray-200 rounded w-2/3 mb-2"></div>
                <div className="h-6 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`bg-red-50 border border-red-200 rounded-xl p-6 ${className}`}>
        <div className="flex items-center">
          <svg className="w-5 h-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          <span className="text-red-800 font-medium">{error}</span>
        </div>
      </div>
    );
  }

  if (!holdingsData) {
    return null;
  }

  const { current_holdings, market_value, profit_loss } = holdingsData;

  return (
    <div className={`bg-white rounded-xl shadow-lg overflow-hidden ${className}`}>
      {/* Header */}
      <div className="bg-gradient-to-r from-yellow-500 to-yellow-600 px-6 py-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold text-white flex items-center">
            <svg className="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.736 6.979C9.208 7.193 9.5 7.68 9.5 8.25v4.5a.75.75 0 01-1.5 0V8.25c0-.57.292-1.057.736-1.271a5.501 5.501 0 017.028 0c.444.214.736.701.736 1.271v4.5a.75.75 0 11-1.5 0V8.25a.75.75 0 00-.364-.643 4 4 0 00-4.872 0 .75.75 0 00-.364.643z" clipRule="evenodd" />
            </svg>
            Gold Holdings
          </h3>
          <div className="bg-white/20 rounded-full px-3 py-1">
            <span className="text-white text-sm font-medium">
              {current_holdings.gold_weight_baht.toFixed(2)} บาท
            </span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {/* Main Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Current Holdings */}
          <div className="bg-gradient-to-br from-amber-50 to-yellow-50 rounded-lg p-4 border border-amber-200">
            <div className="flex items-center justify-between mb-2">
              <span className="text-amber-700 text-sm font-medium">Current Holdings</span>
              <svg className="w-4 h-4 text-amber-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="text-2xl font-bold text-amber-900 mb-1">
              {formatNumber(current_holdings.gold_weight_grams, 3)}g
            </div>
            <div className="text-xs text-amber-600">
              ({formatNumber(current_holdings.gold_weight_baht, 2)} บาท)
            </div>
          </div>

          {/* Market Value */}
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-4 border border-blue-200">
            <div className="flex items-center justify-between mb-2">
              <span className="text-blue-700 text-sm font-medium">Market Value</span>
              <svg className="w-4 h-4 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="text-2xl font-bold text-blue-900 mb-1">
              {formatCurrency(market_value.current_market_value_thb)}
            </div>
            <div className="text-xs text-blue-600">
              ฿{formatNumber(market_value.current_price_per_gram, 2)}/g
            </div>
          </div>

          {/* Profit/Loss */}
          <div className={`bg-gradient-to-br rounded-lg p-4 border ${profit_loss.unrealized_pl_thb >= 0 ? 'from-green-50 to-emerald-50 border-green-200' : 'from-red-50 to-pink-50 border-red-200'}`}>
            <div className="flex items-center justify-between mb-2">
              <span className={`${profit_loss.unrealized_pl_thb >= 0 ? 'text-green-700' : 'text-red-700'} text-sm font-medium`}>
                P&L
              </span>
              <svg className={`w-4 h-4 ${profit_loss.unrealized_pl_thb >= 0 ? 'text-green-500' : 'text-red-500'}`} fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
              </svg>
            </div>
            <div className={`text-2xl font-bold mb-1 ${getPLColor(profit_loss.total_pl_thb)}`}>
              {getPLSign(profit_loss.total_pl_thb)}{formatCurrency(Math.abs(profit_loss.total_pl_thb))}
            </div>
            <div className={`text-xs ${getPLColor(profit_loss.unrealized_pl_percent)}`}>
              {getPLSign(profit_loss.unrealized_pl_percent)}{formatNumber(Math.abs(profit_loss.unrealized_pl_percent), 2)}%
            </div>
          </div>
        </div>

        {/* Detailed Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Cost Basis */}
          <div className="bg-gray-50 rounded-lg p-4">
            <h4 className="text-sm font-medium text-gray-700 mb-3">Cost Basis</h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Avg Purchase Price:</span>
                <span className="text-sm font-medium text-gray-900">
                  ฿{formatNumber(current_holdings.average_purchase_price_per_gram, 2)}/g
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Total Cost:</span>
                <span className="text-sm font-medium text-gray-900">
                  {formatCurrency(market_value.total_cost_thb)}
                </span>
              </div>
            </div>
          </div>

          {/* Performance */}
          <div className="bg-gray-50 rounded-lg p-4">
            <h4 className="text-sm font-medium text-gray-700 mb-3">Performance</h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Unrealized P&L:</span>
                <span className={`text-sm font-medium ${getPLColor(profit_loss.unrealized_pl_thb)}`}>
                  {getPLSign(profit_loss.unrealized_pl_thb)}{formatCurrency(Math.abs(profit_loss.unrealized_pl_thb))}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Realized P&L:</span>
                <span className={`text-sm font-medium ${getPLColor(profit_loss.realized_pl_thb)}`}>
                  {getPLSign(profit_loss.realized_pl_thb)}{formatCurrency(Math.abs(profit_loss.realized_pl_thb))}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Transaction Summary */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex space-x-6 text-sm">
              <span className="text-gray-600">
                <span className="font-medium text-gray-900">{holdingsData.transactions.total_buy_transactions}</span> Buy
              </span>
              <span className="text-gray-600">
                <span className="font-medium text-gray-900">{holdingsData.transactions.total_sell_transactions}</span> Sell
              </span>
            </div>
            <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
              View Details →
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GoldHoldingsCard;