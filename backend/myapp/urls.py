# urls.py (myapp/urls.py)
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'service-categories', views.ServiceCategoryViewSet)
router.register(r'services', views.ServiceViewSet)
router.register(r'appointments', views.AppointmentViewSet)
router.register(r'availability', views.AvailabilityViewSet)
router.register(r'subscription-plans', views.SubscriptionPlanViewSet)
router.register(r'client-subscriptions', views.ClientSubscriptionViewSet)
router.register(r'reviews', views.ReviewViewSet)


urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs
    path('users/', views.UserListCreate.as_view(), name='user-list-create'),
    path('users/me/', views.UserRetrieveUpdateDestroy.as_view(), name='user-detail'),
    path('practitioners/', views.PractitionerListCreate.as_view(), name='practitioner-list-create'),
    path('practitioners/me/', views.PractitionerDetail.as_view(), name='practitioner-detail'),
    path('clients/', views.ClientListCreate.as_view(), name='client-list-create'), #Admin only
    path('clients/me/', views.ClientDetail.as_view(), name='client-me'),
    path('available-slots/', views.get_available_slots, name='get-available-slots'),
]

# urls.py (project-level urls.py) - Remains the same, just ensure myapp.urls is included