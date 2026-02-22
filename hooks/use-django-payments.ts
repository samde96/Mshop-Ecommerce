import { useState, useCallback } from 'react';
import apiClient from '@/lib/api-client';

export interface MpesaResponse {
  success: boolean;
  message: string;
  data?: any;
}

export function useDjangoPayments() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const initiateMpesaPayment = useCallback(
    async (
      phoneNumber: string,
      amount: number,
      orderId: number
    ): Promise<MpesaResponse> => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.post<MpesaResponse>(
          '/payments/mpesa/stkpush/',
          {
            phone_number: phoneNumber,
            amount,
            order_id: orderId,
          }
        );
        return response.data;
      } catch (err: any) {
        const errorMessage =
          err.response?.data?.message ||
          err.response?.data?.error ||
          'Failed to initiate M-Pesa payment';
        setError(errorMessage);
        throw new Error(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const checkMpesaStatus = useCallback(
    async (checkoutRequestId: string) => {
      setLoading(true);
      setError(null);
      try {
        const response = await apiClient.post('/payments/mpesa/query/', {
          checkout_request_id: checkoutRequestId,
        });
        return response.data;
      } catch (err: any) {
        const errorMessage =
          err.response?.data?.error ||
          'Failed to check M-Pesa status';
        setError(errorMessage);
        throw new Error(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const handleMpesaCallback = useCallback(
    (callbackData: any) => {
      console.log('M-Pesa Callback received:', callbackData);
      return true;
    },
    []
  );

  return {
    loading,
    error,
    initiateMpesaPayment,
    checkMpesaStatus,
    handleMpesaCallback,
  };
}
