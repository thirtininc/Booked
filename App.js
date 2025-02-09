// App.js (React Native - Main App)
import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import HomeScreen from './screens/HomeScreen';
import SearchScreen from './screens/SearchScreen';
import AppointmentsScreen from './screens/AppointmentsScreen';
import ProfileScreen from './screens/ProfileScreen';
import LoginScreen from './screens/LoginScreen';
import RegisterScreen from './screens/RegisterScreen';
import PractitionerDetailScreen from './screens/PractitionerDetailScreen'; //Detail page
import BookingScreen from './screens/BookingScreen';
import { AuthContext, AuthProvider } from './auth/AuthContext'; // Similar to web app
import axios from 'axios';
import { View, Text } from 'react-native';


const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function App() {

  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>

  )
}


function AppContent () {
  const { user, loading } = React.useContext(AuthContext);

    if (loading) {
      return (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
          <Text>Loading...</Text>
        </View>
      );
    }
    return (
    <NavigationContainer>
      {user ? (
        <Tab.Navigator>
          <Tab.Screen name="Home" component={HomeStack} />
          <Tab.Screen name="Appointments" component={AppointmentsScreen} />
          <Tab.Screen name="Profile" component={ProfileScreen} />
        </Tab.Navigator>
      ) : (
        <Stack.Navigator>
          <Stack.Screen name="Login" component={LoginScreen} />
          <Stack.Screen name="Register" component={RegisterScreen} />
        </Stack.Navigator>
      )}
    </NavigationContainer>
  );
}

// Nested stack navigator for the Home tab (to handle search and details)
function HomeStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Search" component={SearchScreen} />
      <Stack.Screen name="PractitionerDetail" component={PractitionerDetailScreen} />
      <Stack.Screen name="Booking" component={BookingScreen}/>
    </Stack.Navigator>
  );
}

export default App;