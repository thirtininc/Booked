// React Frontend (Example - using socket.io-client)
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

function AppointmentDetail({ appointmentId }) {
    const [messages, setMessages] = useState([]);
    const [socket, setSocket] = useState(null);

    useEffect(() => {
        const newSocket = io(`ws://your-backend-url/ws/appointments/${appointmentId}/`); // Replace with your URL
        setSocket(newSocket);

        newSocket.on('connect', () => {
            console.log('Connected to WebSocket');
        });

        newSocket.on('appointment_message', (data) => {
            setMessages(prevMessages => [...prevMessages, data.message]);
        });

        return () => newSocket.close(); // Clean up on unmount
    }, [appointmentId]);

    const sendMessage = (message) => {
        if (socket) {
            socket.emit('message', { message });
        }
    };
    //... rest of component for display
}