# settings.py
# ... other settings ...

# Email Settings (for basic Django email)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Or 'django.core.mail.backends.console.EmailBackend' for testing
EMAIL_HOST = 'smtp.example.com'  # Your email provider's SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@example.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
DEFAULT_FROM_EMAIL = 'noreply@example.com'

# Nylas API Keys (if using Nylas)
NYLAS_APP_ID = 'YOUR_NYLAS_APP_ID'
NYLAS_APP_SECRET = 'YOUR_NYLAS_APP_SECRET'
NYLAS_ACCESS_TOKEN = 'YOUR_NYLAS_ACCESS_TOKEN'

# Twilio API Keys
TWILIO_ACCOUNT_SID = 'YOUR_TWILIO_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'YOUR_TWILIO_AUTH_TOKEN'
TWILIO_PHONE_NUMBER = '+15551234567'  # Your Twilio phone number



# settings.py
# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Or your Redis URL
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC' #Or your timezone