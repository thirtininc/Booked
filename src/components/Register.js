// src/components/Register.js
import React, { useState } from 'react';
    import { useAuth } from '../auth/AuthContext';
    import { useNavigate } from 'react-router-dom';

    function Register() {
        const [userData, setUserData] = useState({
            username: '',
            email: '',
            password: '',
            first_name: '',
            last_name: '',
            user_type: 'client', // Or allow selection
        });
        const [error, setError] = useState('');
        const { register } = useAuth(); // Get register function from context
        const navigate = useNavigate();

        const handleChange = (e) => {
            setUserData({ ...userData, [e.target.name]: e.target.value });
        };

        const handleSubmit = async (e) => {
            e.preventDefault();
            try {
                await register(userData);
                navigate('/login'); // Redirect to login after successful registration
            } catch (err) {
                setError('Registration failed. Please check the form and try again.');
            }
        };
      return (
        <div>
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                 <div>
                    <label>Username:</label>
                    <input type="text" name="username" value={userData.username} onChange={handleChange} required />
                </div>
                <div>
                    <label>Email:</label>
                    <input type="email" name="email" value={userData.email} onChange={handleChange} required />
                </div>
                <div>
                    <label>Password:</label>
                    <input type="password" name="password" value={userData.password} onChange={handleChange} required />
                </div>
                <div>
                    <label>First Name:</label>
                    <input type="text" name="first_name" value={userData.first_name} onChange={handleChange} required/>
                </div>
                <div>
                    <label>Last Name:</label>
                    <input type="text" name="last_name" value={userData.last_name} onChange={handleChange} required/>
                </div>
                <div>
                  <label>User Type:</label>
                  <select name="user_type" value={userData.user_type} onChange={handleChange} required>
                    <option value="client">Client</option>
                    <option value="practitioner">Practitioner</option>
                  </select>
                </div>

                <button type="submit">Register</button>
            </form>
              {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
}

export default Register;