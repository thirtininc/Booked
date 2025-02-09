# Booked: The All-in-One Appointment Scheduling and Practice Growth Platform for Healthcare

## Overview

Booked is a comprehensive platform designed to streamline appointment scheduling, enhance client communication, and empower healthcare professionals to grow their practices. It offers a suite of applications for web, iOS, and Android, providing a seamless experience for both practitioners and clients.

## Features

### For Practitioners (Web Application):

*   **Dashboard:** Key performance indicators (KPIs), recent activity, quick links.
*   **Calendar:** Day, week, month, and agenda views; drag-and-drop scheduling; appointment management; availability management.
*   **Clients:** Client list, profiles, in-app messaging.
*   **Services & Pricing:** Service management, pricing settings, packages.
*   **Demand Forecasting:** AI-powered predictions and pricing recommendations (using BigQuery and Vertex AI).
*   **Subscription Management:** Plan creation and subscriber management.
*   **Reports & Analytics:** Customizable reports, integration with BigQuery and Vertex AI.
*   **Settings:** Account settings, booking rules, integrations (Nylas, Google Healthcare Cloud, payment gateways).
*   **Website Booking Plugin:** Embeddable widget for practitioner websites.
*   **Admin Panel:** (Django Admin) for overall site and user management.

### For Clients (iOS and Android Apps):

*   **Search and Discovery:** Search for practitioners by specialty, location, etc.
*   **Booking:** Select services, appointment times, and handle payments.
*   **Appointments:** View upcoming/past appointments, reschedule/cancel, receive reminders.
*   **Subscriptions:** Manage subscriptions and payment information.
*   **Communication:** In-app messaging, notifications.
*   **Profile:** Manage personal information and appointment history.

### AI-Powered Phone Bookings (Conceptual):

*   Voice assistant for answering calls, booking appointments, and managing client interactions (using Google Cloud Speech-to-Text and Dialogflow).

## Technology Stack

*   **Frontend (Web):** React, Redux/Zustand, Material-UI/Ant Design, Axios
*   **Frontend (Mobile):** React Native, React Navigation, Redux/Zustand
*   **Backend:** Python/Django, Django REST Framework (DRF)
*   **Database:** PostgreSQL (Cloud SQL on Google Cloud)
*   **Cloud Platform:** Google Cloud Platform (GCP)
    *   Google Healthcare Cloud
    *   BigQuery
    *   Vertex AI
    *   Cloud Run/App Engine
    *   Cloud Storage
    *   Cloud Functions
    *   Cloud Pub/Sub
*   **APIs & Integrations:**
    *   Nylas (Email)
    *   Telnyx (SMS, Voice - *Conceptual for Calls*)
    *   Stripe/PayPal (Payment Gateway)
    *   Google Cloud Speech-to-Text & Dialogflow (AI Phone Bookings - *Conceptual*)
    *   FHIR (for potential EHR integration - *Conceptual*)
* **Containerization**: Docker, Kubernetes
* **CI/CD**: Gitlab CI/CD

## Directory Structure
