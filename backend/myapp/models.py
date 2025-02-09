# models.py (myapp/models.py)
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('practitioner', 'Practitioner'),
        ('client', 'Client'),
        ('admin', 'Admin'), # Added admin user type
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='client')
    phone_number = models.CharField(max_length=20, blank=True)
    # Add address, other common fields

class Practitioner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='practitioner_profile')
    specialty = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='practitioner_profiles/', blank=True, null=True)
    # Add location (e.g., using GeoDjango for geospatial data)

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    date_of_birth = models.DateField(blank=True, null=True)
    # Add other client-specific fields, potentially including medical history (with appropriate privacy considerations)

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Service Categories"

class Service(models.Model):
    practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.IntegerField()  # Duration in minutes
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)

class Appointment(models.Model):
    practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE, related_name='appointments')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
        ('no_show', 'No Show'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True) # Notes about the appointment

    def __str__(self):
        return f"{self.client.user.username} - {self.service.name} - {self.start_time}"

class Availability(models.Model):
    practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)])  # 0=Monday, 1=Tuesday, ..., 6=Sunday
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name_plural = "Availability"
        unique_together = ('practitioner', 'day_of_week', 'start_time') # Prevent overlapping availability

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    billing_frequency = models.CharField(max_length=20, choices=(('monthly', 'Monthly'), ('annually', 'Annually')))
    # Add features associated with the plan (e.g., number of appointments, access to features)

class ClientSubscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateField()
    renewal_date = models.DateField()
    is_active = models.BooleanField(default=True)
    # Add payment details (consider using a payment gateway integration like Stripe)

class Review(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)