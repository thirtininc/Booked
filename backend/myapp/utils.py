# myapp/utils.py
from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client  # Install twilio: pip install twilio
# from nylas import Client  # Install nylas: pip install nylas  (If using Nylas)

# --- Email (using Django's built-in email capabilities - simpler than Nylas for basic use) ---
def send_appointment_confirmation_email(appointment):
    subject = 'Appointment Confirmation'
    message = f"""
    Your appointment with {appointment.practitioner.user.first_name} {appointment.practitioner.user.last_name}
    for {appointment.service.name} on {appointment.start_time.strftime('%Y-%m-%d %H:%M')} has been confirmed.
    """
    from_email = settings.DEFAULT_FROM_EMAIL  # Set this in your settings.py
    recipient_list = [appointment.client.user.email]
    send_mail(subject, message, from_email, recipient_list)

# --- Email (using Nylas - more advanced features) ---
# def send_nylas_email(to_email, subject, body):
#     nylas = Client(
#         settings.NYLAS_APP_ID,
#         settings.NYLAS_APP_SECRET,
#         settings.NYLAS_ACCESS_TOKEN,
#     )
#     draft = nylas.drafts.create()
#     draft.subject = subject
#     draft.body = body
#     draft.to = [{'email': to_email}]
#     draft.send()

# --- SMS (using Twilio) ---
def send_appointment_reminder_sms(appointment):
    account_sid = settings.TWILIO_ACCOUNT_SID  # Set these in settings.py
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=appointment.client.user.phone_number,
        from_=twilio_phone_number,
        body=f"Reminder: Your appointment for {appointment.service.name} is on {appointment.start_time.strftime('%Y-%m-%d %H:%M')}.",
    )
    # You might want to store the message.sid for tracking

# --- Call Integration (Conceptual - Requires a service like Twilio Voice) ---
#  You would typically use a service like Twilio Voice for this.
#  The process would involve:
#  1.  User initiates a call request (e.g., clicks a "Call" button).
#  2.  Your backend receives the request.
#  3.  Your backend uses the Twilio Voice API to initiate a call
#      between the client and the practitioner (or a proxy number).
#  This is more complex and requires a separate Twilio setup.  I'll provide a *very* basic
#  example, but you'll need to consult Twilio's documentation for full implementation.
def initiate_call(practitioner_phone, client_phone):

    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER # Your Twilio number

    client = Client(account_sid, auth_token)
    try:
        call = client.calls.create(
            to=client_phone,  #  Client's phone number
            from_=twilio_phone_number,
            url='http://demo.twilio.com/docs/voice.xml'  #  URL to TwiML instructions (see Twilio docs)
            #  In a real app, you'd dynamically generate the TwiML to connect to the practitioner.
        )
        print(call.sid) # Log call SID for tracking
        return call.sid # Return the call SID
    except Exception as e:
        print(f"Error initiating call: {e}")
        return None