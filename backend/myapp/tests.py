# myapp/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Practitioner

class PractitionerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', user_type='practitioner')
        self.client.force_authenticate(user=self.user) #Login the test user.

        # Create a practitioner associated with the user
        self.practitioner = Practitioner.objects.create(user=self.user, specialty="Test Specialty")


    def test_create_practitioner(self):
        url = reverse('practitioner-list-create') #Use named URL
        data = {'user':{'username': 'newuser', 'password': 'newpassword', 'email':'new@email.com', 'first_name':'first', 'last_name':'last', 'user_type':'practitioner'}, 'specialty': 'Cardiology'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Practitioner.objects.count(), 2) # Check if a new practitioner was created
        self.assertEqual(User.objects.count(), 2) # Check user

    def test_get_practitioner_list(self):
        url = reverse('practitioner-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming one practitioner was created in setUp

    def test_get_practitioner_detail(self):
      url = reverse('practitioner-detail')
      response = self.client.get(url)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data['specialty'], "Test Specialty")

    def test_update_practitioner(self):
        url = reverse('practitioner-detail')
        data = {'specialty': 'New Specialty'}
        response = self.client.patch(url, data, format='json') #Use patch for partial update
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.practitioner.refresh_from_db() #Reload data
        self.assertEqual(self.practitioner.specialty, 'New Specialty')

    def test_delete_practitioner(self):
      url = reverse('practitioner-detail')
      response = self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
      self.assertEqual(Practitioner.objects.count(),0)

    def test_unauthenticated_access(self):
        self.client.logout() #Log out
        url = reverse('practitioner-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) #Should be 403 Forbidden