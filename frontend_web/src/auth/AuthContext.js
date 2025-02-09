// src/auth/AuthContext.js
import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true); // Add a loading state

    useEffect(() => {
        // Check for existing token on app load
        const token = localStorage.getItem('token');
        if (token) {
            axios.defaults.headers.common['Authorization'] = `Token ${token}`;
            axios.get('/api/users/me/')
                .then(response => {
                    setUser(response.data);
                })
                .catch(error => {
                    console.error("Error fetching user:", error);
                    localStorage.removeItem('token'); // Remove invalid token
                })
                .finally(() => setLoading(false)); // Set loading to false
        } else {
          setLoading(false);
        }
    }, []);

    const login = async (username, password) => {
        try {
            const response = await axios.post('/api-auth/login/', { username, password });
            const token = response.data.token;
            localStorage.setItem('token', token);
            axios.defaults.headers.common['Authorization'] = `Token ${token}`;
            const userResponse = await axios.get('/api/users/me/');
            setUser(userResponse.data);
            return true;
        } catch (error) {
            console.error("Login failed:", error);
            throw error; // Re-throw the error to be handled by the caller
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        delete axios.defaults.headers.common['Authorization'];
        setUser(null);
    };
  const register = async (userData) => {
        try{
            const response = await axios.post('/api/users/', userData);
            //Dont auto log in on register.
            return response;
        } catch (error){
            console.error("Registration Failed: ", error);
            throw error;
        }
    }

    return (
        <AuthContext.Provider value={{ user, login, logout, register, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);