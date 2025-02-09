# views.py (example)
from .utils import send_appointment_confirmation_email, send_appointment_reminder_sms

class AppointmentViewSet(viewsets.ModelViewSet):
    # ... (rest of your viewset) ...
    def perform_create(self, serializer):
        appointment = serializer.save()
        send_appointment_confirmation_email(appointment)  # Send email
        # Schedule a task to send an SMS reminder closer to the appointment time
        # (using Celery or similar task queue is highly recommended)
        # send_appointment_reminder_sms(appointment) #Don't send immediately, schedule this.

        # Example of scheduling with Celery (you'll need to set up Celery)
        from .tasks import send_sms_reminder
        reminder_time = appointment.start_time - timezone.timedelta(hours=24)  # 24 hours before
        send_sms_reminder.apply_async((appointment.pk,), eta=reminder_time)