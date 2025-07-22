# USSD Account Management System

This is a Django-based USSD application that provides basic account management functionality through Africa's Talking USSD gateway.

## Features

- View account number
- Check account balance
- View phone number

## Technical Stack

- Python 3.10+
- Django
- Django REST Framework
- Africa's Talking USSD Gateway

## Project Structure

```
creditagri-ussd-demo/
├── ussd_app/                # Main USSD application
│   ├── views.py            # USSD menu logic
│   ├── urls.py             # URL routing
│   ├── tests.py            # Unit tests
│   └── models.py           # Data models
├── ussd_demo/              # Project configuration
│   ├── settings.py         # Django settings
│   └── urls.py             # Main URL routing
└── manage.py               # Django management script
```

## USSD Menu Flow

1. Main Menu
   ```
   Welcome to Offline Account Manager
   1. My Account
   2. My Phone Number
   ```

2. Account Menu (Option 1)
   ```
   Account Info
   1. Account Number
   2. Account Balance
   ```

3. Final Screens
   - Account Number: Shows "ACC1001"
   - Account Balance: Shows "KES 10,000"
   - Phone Number: Shows user's phone number

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env`:
   ```
   AT_USERNAME=your_username
   AT_API_KEY=your_api_key
   AT_SHORTCODE=your_shortcode
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Use ngrok to expose your local server:
   ```bash
   ngrok http 8000
   ```

7. Configure your callback URL in Africa's Talking:
   ```
   https://your-ngrok-url/api/ussd/
   ```

## Testing

Run the test suite:
```bash
python manage.py test ussd_app
```

## API Documentation

### USSD Endpoint

- **URL**: `/api/ussd/`
- **Method**: POST
- **Content-Type**: `application/x-www-form-urlencoded`
- **Parameters**:
  - `sessionId`: Unique session identifier
  - `serviceCode`: USSD code
  - `phoneNumber`: User's phone number
  - `text`: User's input

### Response Format

Responses are prefixed with either:
- `CON`: To continue the session
- `END`: To terminate the session

## Error Handling

- Invalid menu selections return an END response
- Server errors return a user-friendly error message
- Detailed error logging for debugging

## Security

- CSRF protection is disabled for the USSD endpoint
- Input validation is implemented
- Logging for security monitoring

## Deployment

For production deployment:
1. Set `DEBUG=False` in settings.py
2. Use a production-grade server (e.g., Gunicorn)
3. Set up proper SSL/TLS
4. Configure proper logging
5. Use environment variables for sensitive data
