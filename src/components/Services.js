// src/components/Services.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../auth/AuthContext';

function Services() {
    const [services, setServices] = useState([]);
    const [newService, setNewService] = useState({ name: '', description: '', duration: '', price: '' });
    const {user} = useAuth();

    useEffect(() => {
      if (user && user.user_type === "practitioner"){
        axios.get('/api/services/')
            .then(response => setServices(response.data))
            .catch(error => console.error("Error fetching services:", error));
      }
    }, [user]);

    const handleInputChange = (e) => {
        setNewService({ ...newService, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('/api/services/', newService)
            .then(response => {
                setServices([...services, response.data]);
                setNewService({ name: '', description: '', duration: '', price: '' }); // Clear form
            })
            .catch(error => console.error("Error creating service:", error));
    };

    return (
        <div>
            <h2>Services</h2>
            {/* Display existing services */}
            <ul>
                {services.map(service => (
                    <li key={service.id}>{service.name} - {service.price}</li>
                ))}
            </ul>