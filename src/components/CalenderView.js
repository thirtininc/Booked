// src/components/CalendarView.js (Example - using react-big-calendar)
import React, { useState, useEffect } from 'react';
import { Calendar, momentLocalizer } from 'react-big-calendar';
import moment from 'moment';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from 'axios';
import { useAuth } from '../auth/AuthContext';

const localizer = momentLocalizer(moment);

function CalendarView() {
    const [events, setEvents] = useState([]);
    const {user} = useAuth();

      useEffect(() => {
        if(user && user.user_type === "practitioner"){
            axios.get('/api/appointments/') // Fetch appointments
                .then(response => {
                    const formattedEvents = response.data.map(appointment => ({
                        title: `${appointment.service.name} with ${appointment.client.user.first_name} ${appointment.client.user.last_name}`,
                        start: new Date(appointment.start_time),
                        end: new Date(appointment.end_time),
                        allDay: false, // Or based on your data
                        resource: appointment, // Store the full appointment data
                    }));
                    setEvents(formattedEvents);
                })
                .catch(error => console.error("Error fetching appointments:", error));
          }
    }, [user]);



    return (
        <div>
            <h2>Calendar</h2>
            <Calendar
                localizer={localizer}
                events={events}
                startAccessor="start"
                endAccessor="end"
                style={{ height: 500 }}
                // Add event handling (onSelectEvent, etc.)
            />
        </div>
    );
}

export default CalendarView;