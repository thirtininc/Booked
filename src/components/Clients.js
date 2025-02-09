// src/components/Clients.js (Example)
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Clients() {
    const [clients, setClients] = useState([]);

    useEffect(() => {
        axios.get('/api/clients/') // Replace with your clients endpoint
            .then(response => setClients(response.data))
            .catch(error => console.error("Error fetching clients:", error));
    }, []);

    return (
        <div>
            <h2>Clients</h2>
            <ul>
                {clients.map(client => (
                    <li key={client.id}>
                      {client.user.first_name} {client.user.last_name} - {client.user.email}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Clients;