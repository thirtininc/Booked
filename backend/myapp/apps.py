// src/App.js (Main App Structure)
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import CalendarView from './components/CalendarView';
import Clients from './components/Clients';
import Services from './components/Services';
import Settings from './components/Settings';
import Login from './components/Login';
import Register from './components/Register';
import { AuthProvider, useAuth } from './auth/AuthContext'; // Context for authentication


function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}

function AppContent() {
    const { user, logout } = useAuth();

    return (
        <div>
          <nav>
            <ul>
              {user ? (
                <>
                  <li><Link to="/">Dashboard</Link></li>
                  <li><Link to="/calendar">Calendar</Link></li>
                  <li><Link to="/clients">Clients</Link></li>
                  <li><Link to="/services">Services</Link></li>
                  <li><Link to="/settings">Settings</Link></li>
                  <li><button onClick={logout}>Logout</button></li>
                </>
              ) : (
                <>
                  <li><Link to="/login">Login</Link></li>
                  <li><Link to="/register">Register</Link></li>
                </>
              )}
            </ul>
          </nav>

            <Routes>
                <Route path="/" element={user ? <Dashboard /> : <Login />} />
                <Route path="/calendar" element={user ? <CalendarView /> : <Login />} />
                <Route path="/clients" element={user ? <Clients /> : <Login />} />
                <Route path="/services" element={user ? <Services /> : <Login />} />
                <Route path="/settings" element={user ? <Settings /> : <Login />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
            </Routes>
        </div>
    );
}
 export default App;