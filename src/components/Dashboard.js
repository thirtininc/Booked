// src/components/Dashboard.js 
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../auth/AuthContext';


function Dashboard() {
    const [appointments, setAppointments] = useState([]);
    const {user} = useAuth();

    useEffect(() => {
      if (user && user.user_type === 'practitioner'){
        axios.get('/api/appointments/') // Replace with your appointments endpoint
            .then(response => setAppointments(response.data))
            .catch(error => console.error("Error fetching appointments:", error));
      }
    }, [user]);

    return (
        <div>
            <h2>Dashboard</h2>
            {/* Display KPIs, recent activity, etc. */}
            <h3>Upcoming Appointments</h3>
            <ul>
                {appointments.map(appointment => (
                    <li key={appointment.id}>
                        {appointment.service.name} with {appointment.client.user.first_name} on {appointment.start_time}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Dashboard;