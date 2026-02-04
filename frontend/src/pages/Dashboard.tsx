import { useAuth } from '../hooks/useAuth';
import { ProtectedRoute } from '../components/common/ProtectedRoute';

export const Dashboard = () => {
  const { user } = useAuth();

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <h1 className="text-xl font-bold text-gray-900">Gold Trader</h1>
                </div>
                <nav className="ml-6 flex space-x-8">
                  <a
                    href="/dashboard"
                    className="border-blue-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Dashboard
                  </a>
                  <a
                    href="/profile"
                    className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Profile
                  </a>
                </nav>
              </div>
              <div className="flex items-center">
                <span className="text-sm text-gray-700">
                  Welcome, {user?.username}
                </span>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main>
          <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <div className="px-4 py-6 sm:px-0">
              <div className="border-4 border-dashed border-gray-200 rounded-lg p-8">
                <div className="text-center">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">
                    Welcome to your Dashboard
                  </h2>
                  <p className="text-gray-600 mb-8">
                    This is your personal dashboard where you can manage your gold trading activities.
                  </p>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-white overflow-hidden shadow rounded-lg">
                      <div className="px-4 py-5 sm:p-6">
                        <div className="text-3xl font-bold text-blue-600">Dashboard</div>
                        <div className="mt-2">
                          <p className="text-sm text-gray-500">
                            View your trading overview and recent activities.
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="bg-white overflow-hidden shadow rounded-lg">
                      <div className="px-4 py-5 sm:p-6">
                        <div className="text-3xl font-bold text-green-600">Trading</div>
                        <div className="mt-2">
                          <p className="text-sm text-gray-500">
                            Buy and sell gold with real-time pricing.
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="bg-white overflow-hidden shadow rounded-lg">
                      <div className="px-4 py-5 sm:p-6">
                        <div className="text-3xl font-bold text-purple-600">Wallet</div>
                        <div className="mt-2">
                          <p className="text-sm text-gray-500">
                            Manage your funds and gold holdings.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
};