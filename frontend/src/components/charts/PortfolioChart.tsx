import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

interface PortfolioDataPoint {
  date: string;
  value: number;
  profit_loss: number;
}

interface PortfolioChartProps {
  data: PortfolioDataPoint[];
  className?: string;
}

const PortfolioChart: React.FC<PortfolioChartProps> = ({ 
  data, 
  className = '' 
}) => {
  const formatCurrency = (value: number) => {
    return `฿${value.toLocaleString('th-TH', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    })}`;
  };

  const formatProfitLoss = (value: number) => {
    const sign = value >= 0 ? '+' : '';
    return `${sign}${value.toFixed(2)}%`;
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="text-sm font-medium text-gray-900">{`Date: ${label}`}</p>
          <p className="text-sm text-gray-700">{`Portfolio Value: ${formatCurrency(data.value)}`}</p>
          <p className={`text-sm ${data.profit_loss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {`P/L: ${formatProfitLoss(data.profit_loss)}`}
          </p>
        </div>
      );
    }
    return null;
  };

  // Calculate gradient based on performance
  const getGradient = () => {
    const lastPoint = data[data.length - 1];
    const firstPoint = data[0];
    if (!lastPoint || !firstPoint) return ['#10b981', '#10b981'];
    
    const isProfit = lastPoint.value > firstPoint.value;
    return isProfit ? ['#10b981', '#34d399'] : ['#ef4444', '#f87171'];
  };

  const gradients = getGradient();

  return (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-200 p-6 ${className}`}>
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Portfolio Performance</h3>
        {data.length > 0 && (
          <div className="text-right">
            <div className="text-2xl font-bold text-gray-900">
              {formatCurrency(data[data.length - 1].value)}
            </div>
            <div className={`text-sm ${
              data[data.length - 1].profit_loss >= 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              {formatProfitLoss(data[data.length - 1].profit_loss)}
            </div>
          </div>
        )}
      </div>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            data={data}
            margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
          >
            <defs>
              <linearGradient id="portfolioGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={gradients[0]} stopOpacity={0.3}/>
                <stop offset="95%" stopColor={gradients[0]} stopOpacity={0}/>
              </linearGradient>
            </defs>
            <XAxis 
              dataKey="date"
              tick={{ fontSize: 12 }}
              tickLine={false}
            />
            <YAxis 
              tick={{ fontSize: 12 }}
              tickLine={false}
              tickFormatter={formatCurrency}
            />
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="value"
              stroke={gradients[0]}
              fillOpacity={1}
              fill="url(#portfolioGradient)"
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 flex items-center justify-between text-sm text-gray-600">
        <span>Portfolio Value Over Time</span>
        {data.length > 1 && (
          <span className={
            data[data.length - 1].profit_loss >= 0 ? 'text-green-600' : 'text-red-600'
          }>
            {data[data.length - 1].profit_loss >= 0 ? '↑' : '↓'} 
            {Math.abs(data[data.length - 1].profit_loss).toFixed(2)}% 
            from start
          </span>
        )}
      </div>
    </div>
  );
};

export default PortfolioChart;