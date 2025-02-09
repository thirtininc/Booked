# myapp/admin.py
from django.contrib import admin
from .models import User, Practitioner, Client, Service, Appointment, Availability, SubscriptionPlan, ClientSubscription, ServiceCategory, Review

admin.site.register(User)
admin.site.register(Practitioner)
admin.site.register(Client)
admin.site.register(Service)
admin.site.register(Appointment)
admin.site.register(Availability)
admin.site.register(SubscriptionPlan)
admin.site.register(ClientSubscription)
admin.site.register(ServiceCategory)
admin.site.register(Review)


# myapp/admin.py (Example)
from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'practitioner', 'service', 'start_time', 'status')
    search_fields = ('client__user__username', 'practitioner__user__username', 'service__name')
    list_filter = ('status', 'start_time')
    readonly_fields = ('end_time',)

    # Example custom action
    actions = ['send_reminder_emails']

    def send_reminder_emails(self, request, queryset):
        for appointment in queryset:
            # Call your email sending function here
            # send_appointment_reminder_email(appointment)  # Assuming you have this function
            pass  # Replace with actual email sending
    send_reminder_emails.short_description = "Send reminder emails to selected appointments"

    #further cuztomization

    #myapp/admin.py

from django.contrib import admin
from .models import User, Practitioner, Client, Service, Appointment, Availability, SubscriptionPlan, ClientSubscription, ServiceCategory, Review

class AvailabilityInline(admin.TabularInline): # Or StackedInline
    model = Availability
    extra = 1 # Number of extra forms to display

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1

@admin.register(Practitioner)
class PractitionerAdmin(admin.ModelAdmin):
    inlines = [AvailabilityInline, ServiceInline]
    list_display = ('user', 'specialty', 'license_number')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'practitioner', 'service', 'start_time', 'status')
    search_fields = ('client__user__username', 'practitioner__user__username', 'service__name')
    list_filter = ('status', 'start_time')
    readonly_fields = ('end_time',)

admin.site.register(Appointment, AppointmentAdmin)

# Register other models similarly.