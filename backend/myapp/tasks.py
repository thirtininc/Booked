# myapp/tasks.py
from celery import shared_task
from .utils import send_appointment_reminder_sms
from .models import Appointment
from django.utils import timezone

@shared_task
def send_sms_reminder(appointment_id):
    try:
      appointment = Appointment.objects.get(pk=appointment_id)
      # Check if the appointment is still valid (not canceled)
      if appointment.status == 'scheduled' or appointment.status == "confirmed":
          send_appointment_reminder_sms(appointment)

    except Appointment.DoesNotExist:
      print(f"Appointment with id {appointment_id} no longer exists.")

     
from celery import shared_task
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from .models import Practitioner

@shared_task
def process_profile_picture(practitioner_id):
    try:
        practitioner = Practitioner.objects.get(pk=practitioner_id)
        if practitioner.profile_picture:
            image = Image.open(practitioner.profile_picture)

            # Resize the image (example)
            image.thumbnail((200, 200))

            # Optimize the image (example)
            buffer = BytesIO()
            image.save(buffer, format='JPEG', quality=85) #Adjust as necessary

            # Save the optimized image
            filename = f"optimized_{practitioner.profile_picture.name.split('/')[-1]}"
            practitioner.profile_picture.save(filename, ContentFile(buffer.getvalue()), save=False)
            practitioner.save()


    except Practitioner.DoesNotExist:
        print("Practitioner does not exist")
    except Exception as e:
        print(f"Error processing image {e}")