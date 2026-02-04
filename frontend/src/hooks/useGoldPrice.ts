import { useState, useEffect } from 'react';
import { goldPriceService } from '../services/api';
import type { GoldPrice } from '../types';

export const useGoldPrice = () => {
  const [goldPrice, setGoldPrice] = useState<GoldPrice | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchLatest = async () => {
    try {
      setIsLoading(true);
      const data = await goldPriceService.getLatest();
      setGoldPrice(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch gold price');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchLatest();
  }, []);

  return {
    goldPrice,
    isLoading,
    error,
    refetch: fetchLatest,
  };
};
