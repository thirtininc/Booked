# views.py
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from .models import User, Practitioner, Client, Service, Appointment, Availability, SubscriptionPlan, ClientSubscription, ServiceCategory, Review
from .serializers import UserSerializer, PractitionerSerializer, ClientSerializer, ServiceSerializer, AppointmentSerializer, AvailabilitySerializer, SubscriptionPlanSerializer, ClientSubscriptionSerializer, ServiceCategorySerializer, ReviewSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.utils import timezone

# --- User Views ---
class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

# --- Practitioner Views ---
class PractitionerListCreate(generics.ListCreateAPIView):
    queryset = Practitioner.objects.all()
    serializer_class = PractitionerSerializer
    permission_classes = [permissions.IsAdminUser | (permissions.IsAuthenticated & IsPractitionerUser)]

    def perform_create(self, serializer):
        # Automatically associate the user with the practitioner profile
        serializer.save(user=self.request.user)

class PractitionerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Practitioner.objects.all()
    serializer_class = PractitionerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
      #Gets practitioner associated with current user.
      return get_object_or_404(Practitioner, user=self.request.user)

# -- Custom Permission --
class IsPractitionerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'practitioner'

# --- Client Views ---
class ClientListCreate(generics.ListCreateAPIView):
  queryset = Client.objects.all()
  serializer_class = ClientSerializer
  permission_classes = [permissions.IsAdminUser] #Only admins can create clients this way, clients create themselves via User

class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Get the client profile associated with the current user
        return get_object_or_404(Client, user=self.request.user)

# --- Service Category Views ---
class ServiceCategoryViewSet(viewsets.ModelViewSet): #Use ViewSet for full CRUD
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.IsAdminUser] #Only admins can manage categories

# --- Service Views ---
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated & IsPractitionerUser]

    def get_queryset(self):
        # Practitioners see only their services
        return Service.objects.filter(practitioner__user=self.request.user)

    def perform_create(self, serializer):
      serializer.save(practitioner=self.request.user.practitioner_profile)

# --- Appointment Views ---
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
      user = self.request.user
      if user.user_type == 'practitioner':
            return Appointment.objects.filter(practitioner__user=user)
      else:
            return Appointment.objects.filter(client__user=user)
    def perform_create(self, serializer):
        serializer.save()

# --- Availability Views ---
class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated & IsPractitionerUser]

    def get_queryset(self):
         return Availability.objects.filter(practitioner__user = self.request.user)
    def perform_create(self, serializer):
        serializer.save(practitioner=self.request.user.practitioner_profile)

# --- Subscription Plan Views ---
class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAdminUser]

# --- Client Subscription Views ---
class ClientSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = ClientSubscription.objects.all()
    serializer_class = ClientSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated] # Adjust as needed

# --- Review Views ---
class ReviewViewSet(viewsets.ModelViewSet):
  queryset = Review.objects.all()
  serializer_class = ReviewSerializer
  permission_classes = [permissions.IsAuthenticated]

# --- Available Slots (Custom View) ---
# (Keep the get_available_slots view from the previous example,
#  but update it to use the Client model and Practitioner model)
@api_view(['GET'])
@permission_classes([permissions.AllowAny]) # Anyone can check for available slots
def get_available_slots(request):
    practitioner_id = request.query_params.get('practitioner_id')
    date_str = request.query_params.get('date')
    service_id = request.query_params.get('service_id')

    if not practitioner_id or not date_str or not service_id:
        return Response({"error": "practitioner_id, date, and service_id are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        practitioner = Practitioner.objects.get(pk=practitioner_id)
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        service = Service.objects.get(pk=service_id)
        day_of_week = date.weekday()

        availability_records = Availability.objects.filter(practitioner=practitioner, day_of_week=day_of_week)
        if not availability_records.exists():
             return Response({"available_slots": []})

        appointments = Appointment.objects.filter(
            practitioner=practitioner,
            start_time__date=date
        )
        available_slots = []
# views.py (continued from previous response)
        for availability in availability_records:
            start_time = timezone.datetime.combine(date, availability.start_time).astimezone(timezone.utc)
            end_time = timezone.datetime.combine(date, availability.end_time).astimezone(timezone.utc)
            current_time = start_time

            while current_time + timezone.timedelta(minutes=service.duration) <= end_time:
                slot_end_time = current_time + timezone.timedelta(minutes=service.duration)
                is_available = True

                for appointment in appointments:
                    if current_time < appointment.end_time and slot_end_time > appointment.start_time:
                        is_available = False
                        break

                if is_available:
                    available_slots.append({
                        "start_time": current_time.isoformat(),
                        "end_time": slot_end_time.isoformat(),
                    })

                current_time += timezone.timedelta(minutes=30) # Check every 30 minutes

        return Response({"available_slots": available_slots})

    except Practitioner.DoesNotExist:
        return Response({"error": "Practitioner not found"}, status=status.HTTP_404_NOT_FOUND)
    except Service.DoesNotExist:
        return Response({"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
        for availability in availability_records:
            start_time = timezone.datetime.combine(date, availability.start_time).astimezone(timezone.utc)
            end_time = timezone.datetime.combine(date, availability.end_time).astimezone(timezone.utc)
            current_time = start_time

            while current_time + timezone.timedelta(minutes=service.duration) <= end_time:
                slot_end_time = current_time + timezone.timedelta(minutes=service.duration)
                is_available = True

                for appointment in appointments:
                    if current_time < appointment.end_time and slot_end_time > appointment.start_time:
                        is_available = False
                        break

                if is_available:
                    available_slots.append({
                        "start_time": current_time.isoformat(),
                        "end_time": slot_end_time.isoformat(),
                    })

                current_time += timezone.timedelta(minutes=30) # Check every 30 minutes

        return Response({"available_slots": available_slots})

    except Practitioner.DoesNotExist:
        return Response({"error": "Practitioner not found"}, status=status.HTTP_404_NOT_FOUND)
    except Service.DoesNotExist:
        return Response({"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)