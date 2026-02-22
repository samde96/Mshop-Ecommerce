import { useState, useCallback } from 'react';
import apiClient from '@/lib/api-client';

export interface OrderItem {
  id: number;
  product: any;
  quantity: number;
  unit_price: string;
  total_price: string;
}

export interface Order {
  id: number;
  order_id: string;
  user: number;
  total_amount: string;
  tax_amount: string;
  shipping_amount: string;
  order_status: string;
  payment_status: string;
  payment_method: string;
  items: OrderItem[];
  created_at: string;
}

export function useDjangoOrders() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [currentOrder, setCurrentOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getOrders = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get('/orders/');
      setOrders(response.data.results);
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Failed to fetch orders';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const getOrderById = useCallback(async (id: number) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.get(`/orders/${id}/`);
      setCurrentOrder(response.data);
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Failed to fetch order';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  const createOrder = useCallback(
    async (
      items: Array<{ product_id: number; quantity: number }>,
      shippingAddressId: number,
      totalAmount: number,
      paymentMethod: string = 'mpesa'
    ) => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.post('/orders/', {
          items,
          shipping_address_id: shippingAddressId,
          payment_method: paymentMethod,
          total_amount: totalAmount,
        });
        setCurrentOrder(response.data);
        return response.data;
      } catch (err: any) {
        const errorMessage = err.response?.data?.error || 'Failed to create order';
        setError(errorMessage);
        throw new Error(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const cancelOrder = useCallback(async (id: number) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.post(`/orders/${id}/cancel/`);
      setCurrentOrder(response.data);
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.error || 'Failed to cancel order';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    orders,
    currentOrder,
    loading,
    error,
    getOrders,
    getOrderById,
    createOrder,
    cancelOrder,
  };
}
