# serializers.py
from rest_framework import serializers
from .models import User, Practitioner, Client, Service, Appointment, Availability, SubscriptionPlan, ClientSubscription, ServiceCategory, Review
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'user_type', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class PractitionerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Practitioner
        fields = ('id', 'user', 'specialty', 'bio', 'license_number', 'profile_picture')
        read_only_fields = ('id', 'user')  # Prevent updating user through practitioner

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Client
        fields = ('id', 'user', 'date_of_birth')
        read_only_fields = ('id', 'user')


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(), source='category', write_only=True, allow_null=True
    )
    practitioner = PractitionerSerializer(read_only=True) #Read only, set via URL
    class Meta:
        model = Service
        fields = '__all__'



class AppointmentSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), write_only=True)
    practitioner = PractitionerSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('end_time',)

    def validate(self, data):
      # Validation logic as before
      start_time = data.get('start_time')
      service = data.get('service_id') #Use service_id now
      practitioner = self.context['request'].user.practitioner_profile #Get practitioner from request

      if start_time and service and practitioner:
            end_time = start_time + timezone.timedelta(minutes=service.duration)
            data['end_time'] = end_time

            overlapping_appointments = Appointment.objects.filter(
                practitioner=practitioner,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(pk=self.instance.pk if self.instance else None)

            if overlapping_appointments.exists():
                raise serializers.ValidationError("This appointment overlaps with another appointment.")

            data['service'] = service #Set the service object

      return data

    def create(self, validated_data):
        validated_data['practitioner'] = self.context['request'].user.practitioner_profile #Set the practitioner
        validated_data['client'] = Client.objects.get(user=self.context['request'].user) #Set client
        return super().create(validated_data)

class AvailabilitySerializer(serializers.ModelSerializer):
    practitioner = serializers.PrimaryKeyRelatedField(read_only=True) #Read only, set via URL

    class Meta:
        model = Availability
        fields = '__all__'

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class ClientSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientSubscription
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


        #modified serializers.py

        #myapp/serializers.py
from .tasks import process_profile_picture
#...
class PractitionerSerializer(serializers.ModelSerializer):
    #...
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)
        practitioner = Practitioner.objects.create(user=user, **validated_data)
        #After save, process image asynchronously.
        if practitioner.profile_picture:
            process_profile_picture.delay(practitioner.id)
        return practitioner

    def update(self, instance, validated_data):
        # Handle user data update if necessary
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        if 'profile_picture' in validated_data:
            process_profile_picture.delay(instance.id)
        return instance