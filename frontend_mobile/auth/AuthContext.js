// auth/AuthContext.js (React Native) - Very similar to web version
import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage'; // Use AsyncStorage

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check for existing token on app load
        const loadUser = async () => {
          try {
              const token = await AsyncStorage.getItem('token');
              if (token) {
                  axios.defaults.headers.common['Authorization'] = `Token ${token}`;
                  const response = await axios.get('/api/users/me/'); // Your API endpoint
                  setUser(response.data);
              }
          } catch (error) {
              console.error("Error loading user:", error);
              await AsyncStorage.removeItem('token'); // Remove invalid token
          } finally {
              setLoading(false);
          }
      };
      loadUser();
    }, []);

    const login = async (username, password) => {
      try {
          const response = await axios.post('/api-auth/login/', { username, password });
          const token = response.data.token;
          await AsyncStorage.setItem('token', token);
          axios.defaults.headers.common['Authorization'] = `Token ${token}`;

          // Fetch user data after successful login
          const userResponse = await axios.get('/api/users/me/');
          setUser(userResponse.data);

          return true; // Indicate successful login
      } catch (error) {
          console.error("Login failed:", error);
          throw error; // Re-throw for handling in component
      }
    };

    const logout = async () => {
      try {
          await AsyncStorage.removeItem('token');
          delete axios.defaults.headers.common['Authorization'];
          setUser(null);
      } catch (error) {
          console.error("Logout failed:", error);
      }
    };

    const register = async (userData) => {
        try {
          const response = await axios.post('/api/users/', userData);
          //Consider automatically logging in the user here, or redirect to login.
          return response;
        } catch (error){
            console.error("Registration failed: ", error);
            throw error; //re-throw for handling in component.
        }
    }

    return (
        <AuthContext.Provider value={{ user, login, logout, register, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);