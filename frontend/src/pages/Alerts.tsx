import React, { useState } from 'react';
import { ProtectedRoute } from '../components/common/ProtectedRoute';
import { useAuth } from '../hooks/useAuth';

interface PriceAlert {
  id: string;
  target_price: number;
  condition: 'above' | 'below';
  is_active: boolean;
  created_at: string;
  triggered: boolean;
}

const Alerts: React.FC = () => {
  const { user } = useAuth();
  const [alerts, setAlerts] = useState<PriceAlert[]>([
    {
      id: '1',
      target_price: 2500,
      condition: 'above',
      is_active: true,
      created_at: '2026-02-05T08:00:00Z',
      triggered: false,
    },
    {
      id: '2',
      target_price: 2400,
      condition: 'below',
      is_active: true,
      created_at: '2026-02-05T08:30:00Z',
      triggered: false,
    },
  ]);
  
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    target_price: '',
    condition: 'above' as 'above' | 'below',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const newAlert: PriceAlert = {
      id: Date.now().toString(),
      target_price: parseFloat(formData.target_price),
      condition: formData.condition,
      is_active: true,
      created_at: new Date().toISOString(),
      triggered: false,
    };

    setAlerts(prev => [...prev, newAlert]);
    setFormData({ target_price: '', condition: 'above' });
    setShowForm(false);
  };

  const toggleAlert = (id: string) => {
    setAlerts(prev =>
      prev.map(alert =>
        alert.id === id ? { ...alert, is_active: !alert.is_active } : alert
      )
    );
  };

  const deleteAlert = (id: string) => {
    setAlerts(prev => prev.filter(alert => alert.id !== id));
  };

  const formatCurrency = (value: number) => {
    return `฿${value.toLocaleString('th-TH', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })}`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('th-TH');
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <div className="flex-shrink-0 flex items-center">
                  <div className="bg-gradient-to-r from-yellow-400 to-yellow-600 rounded-lg p-2 mr-3">
                    <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <h1 className="text-xl font-bold bg-gradient-to-r from-yellow-600 to-yellow-800 bg-clip-text text-transparent">
                    Gold Trader
                  </h1>
                </div>
                <nav className="ml-10 flex space-x-8">
                  <a
                    href="/dashboard"
                    className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Dashboard
                  </a>
                  <a
                    href="/trade"
                    className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Trading
                  </a>
                  <a
                    href="/alerts"
                    className="border-yellow-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Alerts
                  </a>
                  <a
                    href="/deposit"
                    className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Deposit
                  </a>
                  <a
                    href="/profile"
                    className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Profile
                  </a>
                </nav>
              </div>
              <div className="flex items-center space-x-4">
                <div className="bg-yellow-50 rounded-full px-3 py-1 border border-yellow-200">
                  <span className="text-sm font-medium text-yellow-800">
                    Welcome, {user?.username}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main>
          <div className="max-w-4xl mx-auto py-8 sm:px-6 lg:px-8">
            <div className="px-4 sm:px-0">
              {/* Page Header */}
              <div className="mb-8 flex justify-between items-center">
                <div>
                  <h2 className="text-3xl font-bold text-gray-900 mb-2">
                    Price Alerts
                  </h2>
                  <p className="text-gray-600">
                    Get notified when gold prices reach your target levels.
                  </p>
                </div>
                <button
                  onClick={() => setShowForm(true)}
                  className="bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-700 transition-colors duration-200 font-medium flex items-center"
                >
                  <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
                  </svg>
                  Create Alert
                </button>
              </div>

              {/* Create Alert Form */}
              {showForm && (
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Create New Price Alert</h3>
                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Target Price (THB per gram)
                      </label>
                      <input
                        type="number"
                        step="0.01"
                        required
                        value={formData.target_price}
                        onChange={(e) => setFormData(prev => ({ ...prev, target_price: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-yellow-500 focus:border-yellow-500"
                        placeholder="2500.00"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Alert Condition
                      </label>
                      <div className="flex space-x-4">
                        <label className="flex items-center">
                          <input
                            type="radio"
                            name="condition"
                            value="above"
                            checked={formData.condition === 'above'}
                            onChange={(e) => setFormData(prev => ({ ...prev, condition: e.target.value as 'above' | 'below' }))}
                            className="mr-2 text-yellow-600 focus:ring-yellow-500"
                          />
                          <span>Alert when price goes ABOVE target</span>
                        </label>
                        <label className="flex items-center">
                          <input
                            type="radio"
                            name="condition"
                            value="below"
                            checked={formData.condition === 'below'}
                            onChange={(e) => setFormData(prev => ({ ...prev, condition: e.target.value as 'above' | 'below' }))}
                            className="mr-2 text-yellow-600 focus:ring-yellow-500"
                          />
                          <span>Alert when price goes BELOW target</span>
                        </label>
                      </div>
                    </div>

                    <div className="flex space-x-3">
                      <button
                        type="submit"
                        className="bg-yellow-600 text-white px-4 py-2 rounded-lg hover:bg-yellow-700 transition-colors duration-200 font-medium"
                      >
                        Create Alert
                      </button>
                      <button
                        type="button"
                        onClick={() => setShowForm(false)}
                        className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors duration-200 font-medium"
                      >
                        Cancel
                      </button>
                    </div>
                  </form>
                </div>
              )}

              {/* Alerts List */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900">Your Price Alerts</h3>
                </div>
                
                {alerts.length === 0 ? (
                  <div className="p-8 text-center text-gray-500">
                    <svg className="w-16 h-16 mx-auto mb-4 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    <p>No price alerts created yet.</p>
                    <p className="text-sm mt-2">Click "Create Alert" to set your first price alert.</p>
                  </div>
                ) : (
                  <div className="divide-y divide-gray-200">
                    {alerts.map((alert) => (
                      <div key={alert.id} className="p-6 flex items-center justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3">
                            <div className={`w-3 h-3 rounded-full ${
                              alert.is_active ? 'bg-green-500' : 'bg-gray-400'
                            }`}></div>
                            <div>
                              <div className="font-medium text-gray-900">
                                Alert when price goes {alert.condition.toUpperCase()} {formatCurrency(alert.target_price)}
                              </div>
                              <div className="text-sm text-gray-500">
                                Created: {formatDate(alert.created_at)}
                              </div>
                            </div>
                          </div>
                        </div>
                        
                        <div className="flex items-center space-x-3">
                          <button
                            onClick={() => toggleAlert(alert.id)}
                            className={`px-3 py-1 rounded text-sm font-medium ${
                              alert.is_active
                                ? 'bg-green-100 text-green-800 hover:bg-green-200'
                                : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                            }`}
                          >
                            {alert.is_active ? 'Active' : 'Inactive'}
                          </button>
                          <button
                            onClick={() => deleteAlert(alert.id)}
                            className="text-red-600 hover:text-red-800 p-1"
                            title="Delete alert"
                          >
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
};

export default Alerts;