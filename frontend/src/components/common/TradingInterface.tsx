import React, { useState, useEffect } from 'react';
import wsService from '../../services/websocket';
import api from '../../services/api';
import type { Transaction } from '../../types';
import { formatNumber } from '../../utils/formatters';

interface TradingInterfaceProps {
  className?: string;
  onTradeComplete?: (transaction: Transaction) => void;
}

const TradingInterface: React.FC<TradingInterfaceProps> = ({ 
  className = '', 
  onTradeComplete 
}) => {
  const [price, setPrice] = useState<number>(0);
  const [amount, setAmount] = useState<string>('');
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    wsService.connect();
    return () => wsService.disconnect();
  }, []);

  const handlePlaceOrder = async () => {
    setProcessing(true);
    try {
      const res = await api.post('/gold/trade/', { type: 'BUY', amount: parseFloat(amount) });
      onTradeComplete?.(res.data.transaction);
    } catch (err) {
      console.error(err);
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className={`bg-white rounded-xl shadow-lg p-6 ${className}`}>
      <h3 className="text-xl font-bold mb-4">Trading</h3>
      <div className="mb-4">Price: ฿{formatNumber(price, 2)}/g</div>
      <input 
        type="number" 
        value={amount} 
        onChange={e => setAmount(e.target.value)}
        className="w-full border p-2 rounded mb-4"
        placeholder="Grams"
      />
      <button 
        onClick={handlePlaceOrder}
        disabled={processing}
        className="w-full py-3 bg-blue-600 text-white rounded-lg font-bold"
      >
        {processing ? 'Processing...' : 'Place Order'}
      </button>
    </div>
  );
};

export default TradingInterface;
