import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import api from '../services/api';
import { GoldHolding, Transaction, GoldPrice } from '../types';

const Trading: React.FC = () => {
  const { user } = useAuth();
  const [holdings, setHoldings] = useState<GoldHolding[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [currentPrice, setCurrentPrice] = useState<GoldPrice | null>(null);
  const [amount, setAmount] = useState<number>(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
    const ws = new WebSocket(`ws://localhost:8001/ws/gold-price/`);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'gold_price_update') {
        setCurrentPrice(data.price);
      }
    };
    return () => ws.close();
  }, []);

  const fetchData = async () => {
    try {
      const [holdingsRes, transRes, priceRes] = await Promise.all([
        api.get('/gold/holdings/'),
        api.get('/gold/transactions/'),
        api.get('/gold/prices/current/')
      ]);
      setHoldings(holdingsRes.data);
      setTransactions(transRes.data);
      setCurrentPrice(priceRes.data);
    } catch (err) {
      console.error('Failed to fetch trading data', err);
    }
  };

  const handleTrade = async (type: 'BUY' | 'SELL') => {
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      await api.post('/gold/trade/', {
        type,
        amount,
      });
      setSuccess(`${type === 'BUY' ? 'ซื้อ' : 'ขาย'}ทองคำสำเร็จ!`);
      setAmount(0);
      fetchData();
    } catch (err: any) {
      setError(err.response?.data?.error || 'การส่งคำสั่งล้มเหลว');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6 text-gold-600">Trading Center</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Price & Trade Form */}
        <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
          <h2 className="text-xl font-semibold mb-4">Market Price</h2>
          {currentPrice ? (
            <div className="mb-6">
              <div className="text-4xl font-bold text-gray-800">
                {currentPrice.price_per_baht.toLocaleString()} <span className="text-lg font-normal">THB/Baht</span>
              </div>
              <div className="text-sm text-gray-500 mt-1">
                Last updated: {new Date(currentPrice.timestamp).toLocaleTimeString()}
              </div>
            </div>
          ) : (
            <div className="animate-pulse bg-gray-200 h-12 w-48 rounded mb-6"></div>
          )}

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Amount (Grams)</label>
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(parseFloat(e.target.value))}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-gold-500 focus:border-gold-500"
                placeholder="0.000"
                step="0.001"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => handleTrade('BUY')}
                disabled={loading || amount <= 0}
                className="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition duration-200 disabled:opacity-50"
              >
                {loading ? 'Processing...' : 'Buy Gold'}
              </button>
              <button
                onClick={() => handleTrade('SELL')}
                disabled={loading || amount <= 0}
                className="w-full bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 transition duration-200 disabled:opacity-50"
              >
                {loading ? 'Processing...' : 'Sell Gold'}
              </button>
            </div>

            {error && <div className="text-red-600 text-sm">{error}</div>}
            {success && <div className="text-green-600 text-sm">{success}</div>}
          </div>
        </div>

        {/* Holdings */}
        <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
          <h2 className="text-xl font-semibold mb-4">Your Portfolio</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-gray-600">Available Balance</span>
              <span className="font-bold text-gray-800">{user?.balance.toLocaleString()} THB</span>
            </div>
            {holdings.map((h) => (
              <div key={h.id} className="flex justify-between items-center p-3 bg-gold-50 rounded-lg border border-gold-100">
                <span className="text-gold-800">Gold Holding</span>
                <span className="font-bold text-gold-900">{h.amount} Grams</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Transaction History */}
      <div className="mt-8 bg-white p-6 rounded-xl shadow-lg border border-gray-100">
        <h2 className="text-xl font-semibold mb-4">Recent Trades</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {transactions.map((t) => (
                <tr key={t.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(t.transaction_date).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                      t.transaction_type === 'BUY' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {t.transaction_type}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{t.gold_weight}g</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{t.gold_price_per_gram.toLocaleString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{t.total_amount.toLocaleString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="text-sm text-gray-500">{t.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Trading;
