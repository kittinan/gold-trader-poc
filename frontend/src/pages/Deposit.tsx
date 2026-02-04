import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { ProtectedRoute } from '../components/common/ProtectedRoute';

interface DepositItem {
  id: number;
  amount: number;
  payment_method: string;
  payment_method_display: string;
  status: string;
  status_display: string;
  transaction_reference: string;
  notes: string;
  created_at: string;
  completed_at: string;
}

interface ApiResponse<T> {
  count?: number;
  next?: string;
  previous?: string;
  results?: T[];
}

const Deposit: React.FC = () => {
  const { user, getAuthHeaders } = useAuth();
  const [deposits, setDeposits] = useState<DepositItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [showDepositForm, setShowDepositForm] = useState(false);
  const [amount, setAmount] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('BANK_TRANSFER');
  const [notes, setNotes] = useState('');
  const [message, setMessage] = useState({ type: '', text: '' });

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api';

  const fetchDeposits = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/wallet/deposits/`, {
        headers: getAuthHeaders(),
      });
      
      if (response.ok) {
        const data = await response.json();
        setDeposits(Array.isArray(data) ? data : (data.results || []));
      } else {
        console.error('Failed to fetch deposits');
      }
    } catch (error) {
      console.error('Error fetching deposits:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDeposits();
  }, []);

  const handleDeposit = async (e: React.FormEvent) => {
    e.preventDefault();
    setProcessing(true);
    setMessage({ type: '', text: '' });

    try {
      const response = await fetch(`${API_BASE_URL}/wallet/deposit/create/`, {
        method: 'POST',
        headers: {
          ...getAuthHeaders(),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          amount: parseFloat(amount),
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Automatically complete mock deposit
        await fetch(`${API_BASE_URL}/wallet/deposit/complete/`, {
          method: 'POST',
          headers: {
            ...getAuthHeaders(),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            deposit_id: data.deposit.id,
            reference: data.deposit.reference,
          }),
        });

        setMessage({ type: 'success', text: 'Deposit processed successfully!' });
        setAmount('');
        setNotes('');
        setShowDepositForm(false);
        fetchDeposits();
        
        setTimeout(() => {
          setMessage({ type: '', text: '' });
        }, 5000);
      } else {
        setMessage({ type: 'error', text: data.error || 'Failed to process deposit' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Network error. Please try again.' });
      console.error('Deposit error:', error);
    } finally {
      setProcessing(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'COMPLETED':
        return 'bg-green-100 text-green-800';
      case 'PENDING':
        return 'bg-yellow-100 text-yellow-800';
      case 'FAILED':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
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
                  <a href="/dashboard" className="text-gray-500 hover:text-gray-700 px-1 pt-1 text-sm font-medium">Dashboard</a>
                  <a href="/trade" className="text-gray-500 hover:text-gray-700 px-1 pt-1 text-sm font-medium">Trading</a>
                  <a href="/deposit" className="border-yellow-500 text-gray-900 border-b-2 px-1 pt-1 text-sm font-medium">Deposit</a>
                  <a href="/profile" className="text-gray-500 hover:text-gray-700 px-1 pt-1 text-sm font-medium">Profile</a>
                </nav>
              </div>
              <div className="flex items-center space-x-4">
                <div className="bg-yellow-50 rounded-full px-3 py-1 border border-yellow-200">
                  <span className="text-sm font-medium text-yellow-800">Welcome, {user?.username}</span>
                </div>
                <div className="bg-green-50 rounded-full px-3 py-1 border border-green-200">
                  <span className="text-sm font-medium text-green-800">Balance: ฿{(user?.balance || 0).toLocaleString()}</span>
                </div>
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto py-8 sm:px-6 lg:px-8">
          <div className="px-4 sm:px-0">
            <div className="mb-8 flex justify-between items-center">
              <div>
                <h2 className="text-3xl font-bold text-gray-900 mb-2">Deposit Funds</h2>
                <p className="text-gray-600">Add funds to your account for gold trading</p>
              </div>
              <button
                onClick={() => setShowDepositForm(!showDepositForm)}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors duration-200 font-medium flex items-center"
              >
                New Deposit
              </button>
            </div>

            {message.text && (
              <div className={`mb-6 p-4 rounded-lg ${message.type === 'success' ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                <p className={`text-sm font-medium ${message.type === 'success' ? 'text-green-800' : 'text-red-800'}`}>{message.text}</p>
              </div>
            )}

            {showDepositForm && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
                <form onSubmit={handleDeposit} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Amount (THB)</label>
                    <input
                      type="number"
                      value={amount}
                      onChange={(e) => setAmount(e.target.value)}
                      required
                      className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    />
                  </div>
                  <div className="flex justify-end space-x-3">
                    <button type="button" onClick={() => setShowDepositForm(false)} className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700">Cancel</button>
                    <button type="submit" disabled={processing} className="px-6 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50">
                      {processing ? 'Processing...' : 'Process Deposit'}
                    </button>
                  </div>
                </form>
              </div>
            )}

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">Transaction History</h3>
              </div>
              <ul className="divide-y divide-gray-200">
                {deposits.map((deposit) => (
                  <li key={deposit.id} className="px-6 py-4 flex items-center justify-between">
                    <div>
                      <div className="text-sm font-medium text-gray-900">Deposit</div>
                      <div className="text-sm text-gray-500">Ref: {deposit.transaction_reference}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-gray-900">+฿{deposit.amount.toLocaleString()}</div>
                      <div className={`text-xs ${getStatusColor(deposit.status)} px-2 py-1 rounded-full inline-block mt-1`}>{deposit.status}</div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
};

export default Deposit;
