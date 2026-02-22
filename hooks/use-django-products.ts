import { useState, useCallback } from 'react';
import apiClient from '@/lib/api-client';

export interface Product {
  id: number;
  name: string;
  description: string;
  price: string;
  category: string;
  image_url: string;
  stock: number;
  seller: number;
  seller_name: string;
  is_active: boolean;
  created_at: string;
}

export function useDjangoProducts() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getProducts = useCallback(async (page: number = 1) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get('/products/', {
        params: { page },
      });
      setProducts(response.data.results);
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Failed to fetch products';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const searchProducts = useCallback(
    async (query: string, page: number = 1) => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.get('/products/', {
          params: { search: query, page },
        });
        setProducts(response.data.results);
        return response.data;
      } catch (err: any) {
        const errorMessage = err.response?.data?.error || 'Search failed';
        setError(errorMessage);
        throw new Error(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const getProductsByCategory = useCallback(
    async (category: string, page: number = 1) => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.get('/products/', {
          params: { category, page },
        });
        setProducts(response.data.results);
        return response.data;
      } catch (err: any) {
        const errorMessage =
          err.response?.data?.error || 'Failed to fetch products by category';
        setError(errorMessage);
        throw new Error(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const getProductById = useCallback(async (id: number) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get(`/products/${id}/`);
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Failed to fetch product';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const getCategories = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get('/products/categories/');
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Failed to fetch categories';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    products,
    loading,
    error,
    getProducts,
    searchProducts,
    getProductsByCategory,
    getProductById,
    getCategories,
  };
}
