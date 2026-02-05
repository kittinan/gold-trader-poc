import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';
import type { GoldPrice } from '../../types';

interface GoldPriceChartProps {
  data: GoldPrice[];
  currentPrice?: number;
  className?: string;
}

const GoldPriceChart: React.FC<GoldPriceChartProps> = ({ 
  data, 
  currentPrice,
  className = '' 
}) => {
  // Transform data for the chart
  const chartData = data.map((item, index) => ({
    time: new Date(item.timestamp || Date.now()).toLocaleTimeString('th-TH', {
      hour: '2-digit',
      minute: '2-digit'
    }),
    price: item.bid, // Using bid price as the main price
    ask: item.ask,
    timestamp: item.timestamp || Date.now() + index,
  }));

  const formatPrice = (value: number) => {
    return `฿${value.toLocaleString('th-TH', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    })}`;
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="text-sm font-medium text-gray-900">{`Time: ${label}`}</p>
          <p className="text-sm text-green-600">{`Bid: ${formatPrice(data.price)}`}</p>
          <p className="text-sm text-red-600">{`Ask: ${formatPrice(data.ask)}`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-200 p-6 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Gold Price Trend</h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="time" 
              tick={{ fontSize: 12 }}
              tickLine={false}
            />
            <YAxis 
              domain={['dataMin - 50', 'dataMax + 50']}
              tick={{ fontSize: 12 }}
              tickLine={false}
              tickFormatter={formatPrice}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line
              type="monotone"
              dataKey="price"
              stroke="#f59e0b"
              strokeWidth={2}
              dot={{ fill: '#f59e0b', strokeWidth: 2, r: 3 }}
              activeDot={{ r: 5, stroke: '#f59e0b', strokeWidth: 2 }}
              name="Bid Price"
            />
            {/* Current price reference line */}
            {currentPrice && (
              <ReferenceLine
                y={currentPrice}
                stroke="#6b7280"
                strokeDasharray="5 5"
                label={{
                  value: `Current: ${formatPrice(currentPrice)}`,
                  position: 'top',
                  fill: '#6b7280',
                  fontSize: 12,
                }}
              />
            )}
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 flex items-center justify-center space-x-6 text-sm">
        <div className="flex items-center">
          <div className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
          <span className="text-gray-600">Bid Price</span>
        </div>
        {currentPrice && (
          <div className="flex items-center">
            <div className="w-3 h-0.5 bg-gray-400 mr-2"></div>
            <span className="text-gray-600">Current Price</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default GoldPriceChart;