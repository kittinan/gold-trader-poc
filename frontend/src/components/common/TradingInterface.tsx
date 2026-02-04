import { useState, useEffect, useCallback } from 'react';
import { useWebSocket } from '../services/websocket';
import { goldPriceService } from '../services/api';
import { GoldPrice, Transaction } from '../types';
import { formatCurrency, formatNumber } from '../utils/formatters';

interface TradingInterfaceProps {
  className?: string;
  onTradeComplete?: (transaction: Transaction) => void;
}

interface PriceData {
  currentPrice: number;
  pricePerBaht: number;
  change24h: number;
  changePercent: number;
  volume24h: number;
  lastUpdate: string;
}

const TradingInterface: React.FC<TradingInterfaceProps> = ({ 
  className = '', 
  onTradeComplete 
}) => {
  const [priceData, setPriceData] = useState<PriceData | null>(null);
  const [loading, setLoading] = useState(true);
  const [tradeType, setTradeType] = useState<'BUY' | 'SELL'>('BUY');
  const [amount, setAmount] = useState<string>('');
  const [quantity, setQuantity] = useState<string>('');
  const [isMarketOrder, setIsMarketOrder] = useState(true);
  const [limitPrice, setLimitPrice] = useState<string>('');
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const { connect, disconnect, subscribe, placeOrder, isConnected } = useWebSocket();

  // Fetch initial price data
  useEffect(() => {
    const fetchPriceData = async () => {
      try {
        setLoading(true);
        const response = await goldPriceService.getLatest();
        setPriceData({
          currentPrice: response.price_per_gram,
          pricePerBaht: response.price_per_baht,
          change24h: 0, // Will be updated by WebSocket
          changePercent: 0,
          volume24h: 0,
          lastUpdate: response.timestamp
        });
      } catch (err: any) {
        setError(err.message || 'Failed to fetch price data');
      } finally {
        setLoading(false);
      }
    };

    fetchPriceData();
  }, []);

  // Setup WebSocket connection and subscriptions
  useEffect(() => {
    const setupWebSocket = async () => {
      try {
        await connect();
        subscribe('price_update');
        subscribe('trade_update');
      } catch (err) {
        console.error('WebSocket connection failed:', err);
      }
    };

    setupWebSocket();

    // Cleanup on unmount
    return () => {
      disconnect();
    };
  }, []);

  // Handle WebSocket price updates
  const handlePriceUpdate = useCallback((data: any) => {
    setPriceData(prev => ({
      currentPrice: data.price_per_gram,
      pricePerBaht: data.price_per_baht,
      change24h: data.change_24h || prev?.change24h || 0,
      changePercent: data.change_percent_24h || prev?.changePercent || 0,
      volume24h: data.volume_24h || prev?.volume24h || 0,
      lastUpdate: data.timestamp
    }));
  }, []);

  // Handle trade updates
  const handleTradeUpdate = useCallback((data: any) => {
    if (data.status === 'COMPLETED') {
      setSuccess('Trade completed successfully!');
      onTradeComplete?.(data);
      
      // Clear form
      setAmount('');
      setQuantity('');
      setLimitPrice('');
    } else if (data.status === 'CANCELLED') {
      setError('Trade was cancelled');
    }
  }, [onTradeComplete]);

  // Subscribe to WebSocket events
  useEffect(() => {
    const handlePriceEvent = (event: CustomEvent) => {
      handlePriceUpdate(event.detail);
    };

    const handleTradeEvent = (event: CustomEvent) => {
      handleTradeUpdate(event.detail);
    };

    window.addEventListener('ws_price_update', handlePriceEvent as EventListener);
    window.addEventListener('ws_trade_update', handleTradeEvent as EventListener);

    return () => {
      window.removeEventListener('ws_price_update', handlePriceEvent as EventListener);
      window.removeEventListener('ws_trade_update', handleTradeEvent as EventListener);
    };
  }, [handlePriceUpdate, handleTradeUpdate]);

  // Calculate totals
  const calculateTotal = useCallback(() => {
    if (!priceData || !amount && !quantity) return 0;
    
    const amountNum = parseFloat(amount) || 0;
    const quantityNum = parseFloat(quantity) || 0;
    
    if (amountNum > 0) {
      return amountNum;
    }
    
    return quantityNum * priceData.currentPrice;
  }, [amount, quantity, priceData]);

  // Handle amount/quantity change
  const handleAmountChange = (value: string) => {
    setAmount(value);
    if (priceData && value) {
      const amountNum = parseFloat(value);
      const quantityInGrams = amountNum / priceData.currentPrice;
      setQuantity(quantityInGrams.toFixed(4));
    }
  };

  const handleQuantityChange = (value: string) => {
    setQuantity(value);
    if (priceData && value) {
      const quantityNum = parseFloat(value);
      const totalAmount = quantityNum * priceData.currentPrice;
      setAmount(totalAmount.toFixed(2));
    }
  };

  // Place order
  const handlePlaceOrder = async () => {
    const amountNum = parseFloat(amount);
    const quantityNum = parseFloat(quantity);
    
    if (!amountNum || !quantityNum) {
      setError('Please enter valid amount and quantity');
      return;
    }

    if (!isMarketOrder && !limitPrice) {
      setError('Please enter limit price for limit orders');
      return;
    }

    setProcessing(true);
    setError(null);
    setSuccess(null);

    try {
      const orderData = {
        transaction_type: tradeType,
        gold_weight: quantityNum,
        gold_price_per_gram: isMarketOrder ? priceData!.currentPrice : parseFloat(limitPrice!)
      };

      placeOrder(orderData);
      
      // For demo, we'll simulate a successful trade
      setTimeout(() => {
        setProcessing(false);
        setSuccess(`${tradeType === 'BUY' ? 'Buy' : 'Sell'} order placed successfully!`);
      }, 2000);

    } catch (err: any) {
      setError(err.message || 'Failed to place order');
      setProcessing(false);
    }
  };

  if (loading) {
    return (
      <div className={`bg-white rounded-xl shadow-lg p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[1, 2, 3, 4].map((i) => (
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

  return (
    <div className={`bg-white rounded-xl shadow-lg overflow-hidden ${className}`}>
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-4">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold text-white">Gold Trading</h3>
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${isConnected() ? 'bg-green-400' : 'bg-red-400'}`}></div>
            <span className="text-white text-sm">
              {isConnected() ? 'Live' : 'Offline'}
            </span>
          </div>
        </div>
      </div>

      {/* Price Information */}
      {priceData && (
        <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-sm text-gray-500">Current Price</div>
              <div className="text-lg font-bold text-gray-900">
                ฿{formatNumber(priceData.currentPrice, 2)}/g
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-500">24h Change</div>
              <div className={`text-lg font-bold ${priceData.changePercent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {priceData.changePercent >= 0 ? '+' : ''}{formatNumber(priceData.changePercent, 2)}%
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-500">24h Volume</div>
              <div className="text-lg font-bold text-gray-900">
                {formatNumber(priceData.volume24h, 0)}g
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Last Update</div>
              <div className="text-sm font-medium text-gray-900">
                {new Date(priceData.lastUpdate).toLocaleTimeString()}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Trade Form */}
      <div className="p-6">
        {/* Trade Type Selector */}
        <div className="flex space-x-4 mb-6">
          <button
            onClick={() => setTradeType('BUY')}
            className={`flex-1 py-3 px-4 rounded-lg font-medium transition-colors ${
              tradeType === 'BUY'
                ? 'bg-green-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Buy Gold
          </button>
          <button
            onClick={() => setTradeType('SELL')}
            className={`flex-1 py-3 px-4 rounded-lg font-medium transition-colors ${
              tradeType === 'SELL'
                ? 'bg-red-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Sell Gold
          </button>
        </div>

        {/* Order Type */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Order Type</label>
          <div className="flex space-x-4">
            <label className="flex items-center">
              <input
                type="radio"
                checked={isMarketOrder}
                onChange={() => setIsMarketOrder(true)}
                className="mr-2"
              />
              Market Order
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                checked={!isMarketOrder}
                onChange={() => setIsMarketOrder(false)}
                className="mr-2"
              />
              Limit Order
            </label>
          </div>
        </div>

        {/* Trade Inputs */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Amount (THB)
            </label>
            <input
              type="number"
              value={amount}
              onChange={(e) => handleAmountChange(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="0.00"
              min="0"
              step="0.01"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Quantity (grams)
            </label>
            <input
              type="number"
              value={quantity}
              onChange={(e) => handleQuantityChange(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="0.0000"
              min="0"
              step="0.0001"
            />
          </div>
        </div>

        {/* Limit Price (for limit orders) */}
        {!isMarketOrder && (
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Limit Price (THB/gram)
            </label>
            <input
              type="number"
              value={limitPrice}
              onChange={(e) => setLimitPrice(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="0.00"
              min="0"
              step="0.01"
            />
          </div>
        )}

        {/* Total Amount */}
        <div className="bg-gray-50 rounded-lg p-4 mb-6">
          <div className="flex justify-between items-center">
            <span className="text-sm font-medium text-gray-700">Total Amount:</span>
            <span className="text-xl font-bold text-gray-900">
              ฿{formatNumber(calculateTotal(), 2)}
            </span>
          </div>
        </div>

        {/* Messages */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        {success && (
          <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-sm text-green-800">{success}</p>
          </div>
        )}

        {/* Submit Button */}
        <button
          onClick={handlePlaceOrder}
          disabled={processing || !amount || !quantity}
          className={`w-full py-3 px-4 rounded-lg font-medium text-white transition-colors ${
            processing || !amount || !quantity
              ? 'bg-gray-400 cursor-not-allowed'
              : tradeType === 'BUY'
              ? 'bg-green-600 hover:bg-green-700'
              : 'bg-red-600 hover:bg-red-700'
          }`}
        >
          {processing
            ? 'Processing...'
            : tradeType === 'BUY'
            ? 'Place Buy Order'
            : 'Place Sell Order'}
        </button>
      </div>
    </div>
  );
};

export default TradingInterface;