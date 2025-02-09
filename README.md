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

## Getting Started

### Prerequisites

*   **Backend:**
    *   Python 3.9+
    *   pip
    *   PostgreSQL (or Cloud SQL for PostgreSQL)
    *   Redis (for Celery - optional, but highly recommended)
*   **Frontend (Web):**
    *   Node.js (LTS version recommended)
    *   npm or yarn
*   **Frontend (Mobile):**
    *   Node.js
    *   npm or yarn
    *   React Native CLI
    *   Android Studio (for Android development)
    *   Xcode (for iOS development)
*   **Google Cloud Account:**  Required for using GCP services.
*   **API Keys:**  You'll need API keys for Nylas, Twilio, your chosen payment gateway, and Google Cloud services.

### Setup Instructions

1.  **Backend (Django):**

    ```bash
    # 1. Clone the repository (replace with your actual repo URL)
    git clone <your-backend-repo-url>
    cd backend

    # 2. Create a virtual environment (recommended)
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # 3. Install dependencies
    pip install -r requirements.txt

    # 4. Set up environment variables (create a .env file or set them directly)
    #    Example .env file:
    #    DJANGO_SECRET_KEY=your_secret_key
    #    DATABASE_URL=postgres://user:password@host:port/database
    #    NYLAS_APP_ID=...
    #    TWILIO_ACCOUNT_SID=...
    #    ... other API keys ...
    # Use a library like python-dotenv to load these: pip install python-dotenv
    # Add to myproject/settings.py:
    # from dotenv import load_dotenv
    # load_dotenv()

    # 5. Run migrations
    python manage.py migrate

    # 6. Create a superuser (for the Django admin)
    python manage.py createsuperuser

    # 7. Run the development server
    python manage.py runserver

    # 8. (Optional) Start Celery worker (if using Celery)
    celery -A myproject worker -l info
    #    And Redis: redis-server
    ```

2.  **Frontend (Web - React):**

    ```bash
    # 1. Navigate to the frontend_web directory
    cd ../frontend_web

    # 2. Install dependencies
    npm install  # or yarn install

    # 3. Set up environment variables (create a .env file or set them directly)
    #    Example .env file:
    #    REACT_APP_API_BASE_URL=http://localhost:8000/api  # Your backend API URL

    # 4. Start the development server
    npm start  # or yarn start
    ```

3.  **Frontend (Mobile - React Native):**

    ```bash
    # 1. Navigate to the frontend_mobile directory
    cd ../frontend_mobile

    # 2. Install dependencies
    npm install  # or yarn install

    # 3.  Set up environment variables.  Use a library like `react-native-config`.

    # 4. Start the development server (for iOS)
    npx react-native run-ios
    #    OR (for Android)
    npx react-native run-android
    #    You may need to start the Android emulator or connect a physical device first.
    #    You may need: npx react-native start
    ```

4. **Run dockerized:**
   * Make sure Docker is installed and running.
   * Create a `Dockerfile` in the `backend` folder.
   * Create a `docker-compose.yml` file in the root (`booked`) folder.
   * Run: `docker compose up --build`

## API Documentation

The API documentation is available through the browsable API provided by Django REST Framework. Once the backend server is running, you can access it at `http://localhost:8000/api/`.

## Deployment

*   **Backend:** Deploy to Google Cloud Run (recommended), App Engine, or Compute Engine. Use Cloud SQL for PostgreSQL.
*   **Frontend (Web):** Deploy to Netlify, Vercel, or Google Cloud Storage.
*   **Frontend (Mobile):** Build and submit to the Apple App Store and Google Play Store.

## Testing
* Run Backend tests
```bash
python manage.py test

