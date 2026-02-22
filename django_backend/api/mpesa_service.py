import requests
import os
from base64 import b64encode
from datetime import datetime


class MPesaService:
    def __init__(self):
        self.base_url = "https://sandbox.safaricom.co.ke" if os.environ.get('MPESA_ENVIRONMENT') == 'sandbox' else "https://api.safaricom.co.ke"
        self.consumer_key = os.environ.get('MPESA_CONSUMER_KEY')
        self.consumer_secret = os.environ.get('MPESA_CONSUMER_SECRET')
        self.shortcode = os.environ.get('MPESA_SHORTCODE')
        self.passkey = os.environ.get('MPESA_PASSKEY')
        self.callback_url = os.environ.get('MPESA_CALLBACK_URL')

    def get_access_token(self):
        """Get M-Pesa access token"""
        try:
            auth = b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
            response = requests.get(
                f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials",
                headers={'Authorization': f'Basic {auth}'}
            )
            return response.json().get('access_token')
        except Exception as e:
            print(f"Token generation error: {str(e)}")
            return None

    def initiate_stk_push(self, phone_number, amount, order_id):
        """Initiate STK push for payment"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return {'success': False, 'message': 'Failed to get access token'}

            date = datetime.now()
            timestamp = date.strftime('%Y%m%d%H%M%S')
            password = b64encode(
                f"{self.shortcode}{self.passkey}{timestamp}".encode()
            ).decode()

            formatted_phone = f"254{phone_number[-9:]}"

            response = requests.post(
                f"{self.base_url}/mpesa/stkpush/v1/processrequest",
                json={
                    "BusinessShortCode": self.shortcode,
                    "Password": password,
                    "Timestamp": timestamp,
                    "TransactionType": "CustomerPayBillOnline",
                    "Amount": int(amount),
                    "PartyA": formatted_phone,
                    "PartyB": self.shortcode,
                    "PhoneNumber": formatted_phone,
                    "CallBackURL": self.callback_url,
                    "AccountReference": order_id,
                    "TransactionDesc": "M-Shop Payment"
                },
                headers={'Authorization': f'Bearer {access_token}'}
            )

            result = response.json()
            if result.get('ResponseCode') == '0':
                return {
                    'success': True,
                    'message': 'STK push initiated successfully',
                    'data': result
                }
            return {
                'success': False,
                'message': result.get('ResponseDescription', 'STK push failed'),
                'data': result
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }

    def check_transaction_status(self, checkout_request_id):
        """Check status of a transaction"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return {'success': False, 'message': 'Failed to get access token'}

            date = datetime.now()
            timestamp = date.strftime('%Y%m%d%H%M%S')
            password = b64encode(
                f"{self.shortcode}{self.passkey}{timestamp}".encode()
            ).decode()

            response = requests.post(
                f"{self.base_url}/mpesa/stkpushquery/v1/query",
                json={
                    "BusinessShortCode": self.shortcode,
                    "CheckoutRequestID": checkout_request_id,
                    "Password": password,
                    "Timestamp": timestamp
                },
                headers={'Authorization': f'Bearer {access_token}'}
            )

            result = response.json()
            return {
                'success': result.get('ResponseCode') == '0',
                'data': result
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
