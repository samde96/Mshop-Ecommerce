import { useState, useCallback } from 'react';
import apiClient from '@/lib/api-client';

export interface Address {
  id: number;
  name: string;
  phone: string;
  street: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  is_default: boolean;
  created_at: string;
}

export function useDjangoAddresses() {
  const [addresses, setAddresses] = useState<Address[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getAddresses = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get('/addresses/');
      setAddresses(response.data.results);
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Failed to fetch addresses';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const createAddress = useCallback(
    async (addressData: Partial<Address>) => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.post('/addresses/', addressData);
        setAddresses((prev) => [...prev, response.data]);
        return response.data;
      } catch (err: any) {
        const errorMessage =
          err.response?.data?.error || 'Failed to create address';
        setError(errorMessage);
        throw new Error(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const updateAddress = useCallback(
    async (id: number, addressData: Partial<Address>) => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.put(`/addresses/${id}/`, addressData);
        setAddresses((prev) =>
          prev.map((addr) => (addr.id === id ? response.data : addr))
        );
        return response.data;
      } catch (err: any) {
        const errorMessage =
          err.response?.data?.error || 'Failed to update address';
        setError(errorMessage);
        throw new Error(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const deleteAddress = useCallback(async (id: number) => {
    setLoading(true);
    setError(null);
    try {
      await apiClient.delete(`/addresses/${id}/`);
      setAddresses((prev) => prev.filter((addr) => addr.id !== id));
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.error || 'Failed to delete address';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    addresses,
    loading,
    error,
    getAddresses,
    createAddress,
    updateAddress,
    deleteAddress,
  };
}
