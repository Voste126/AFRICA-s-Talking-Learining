from django.test import TestCase, Client
from django.urls import reverse
from .views import UssdCallbackView

class UssdTests(TestCase):
    def setUp(self):
        # Set up test client
        self.client = Client()
        self.ussd_url = reverse('ussd-callback')
        
        # Sample USSD data
        self.base_data = {
            'sessionId': '12345',
            'serviceCode': '*384*13978',
            'phoneNumber': '+254700000000',
        }

    def test_initial_menu(self):
        """Test the initial USSD menu"""
        data = {**self.base_data, 'text': ''}
        response = self.client.post(self.ussd_url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to Offline Account Manager', response.content.decode())
        self.assertIn('1. My Account', response.content.decode())
        self.assertIn('2. My Phone Number', response.content.decode())

    def test_account_submenu(self):
        """Test the account submenu"""
        data = {**self.base_data, 'text': '1'}
        response = self.client.post(self.ussd_url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Account Info', response.content.decode())
        self.assertIn('1. Account Number', response.content.decode())
        self.assertIn('2. Account Balance', response.content.decode())

    def test_account_number(self):
        """Test viewing account number"""
        data = {**self.base_data, 'text': '1*1'}
        response = self.client.post(self.ussd_url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Your account number is ACC1001', response.content.decode())

    def test_account_balance(self):
        """Test viewing account balance"""
        data = {**self.base_data, 'text': '1*2'}
        response = self.client.post(self.ussd_url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Your balance is KES 10,000', response.content.decode())

    def test_phone_number(self):
        """Test viewing phone number"""
        phone = '+254700000000'
        data = {**self.base_data, 'text': '2', 'phoneNumber': phone}
        response = self.client.post(self.ussd_url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'Your phone number is {phone}', response.content.decode())

    def test_invalid_option(self):
        """Test invalid menu option"""
        data = {**self.base_data, 'text': '9'}
        response = self.client.post(self.ussd_url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid choice', response.content.decode())

    def test_con_prefix_for_menus(self):
        """Test that menus have CON prefix"""
        # Test main menu
        data = {**self.base_data, 'text': ''}
        response = self.client.post(self.ussd_url, data)
        self.assertTrue(response.content.decode().startswith('CON'))
        
        # Test account submenu
        data['text'] = '1'
        response = self.client.post(self.ussd_url, data)
        self.assertTrue(response.content.decode().startswith('CON'))

    def test_end_prefix_for_final_responses(self):
        """Test that final responses have END prefix"""
        # Test account number response
        data = {**self.base_data, 'text': '1*1'}
        response = self.client.post(self.ussd_url, data)
        self.assertTrue(response.content.decode().startswith('END'))
        
        # Test phone number response
        data['text'] = '2'
        response = self.client.post(self.ussd_url, data)
        self.assertTrue(response.content.decode().startswith('END'))

    def test_get_request_rejected(self):
        """Test that GET requests are rejected"""
        response = self.client.get(self.ussd_url)
        self.assertEqual(response.status_code, 400)
