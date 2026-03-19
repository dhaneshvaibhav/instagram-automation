import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import LandingPage from './components/LandingPage';
import Login from './components/Login';
import api from './api';
import { Zap } from 'lucide-react';

const AppContent = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await api.get('/auth/status');
      if (response.data.connected) {
        setUser(response.data);
      } else {
        setUser(null);
      }
    } catch (error) {
      console.error('Error checking auth status:', error);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await api.get('/auth/logout');
      setUser(null);
      navigate('/login');
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        background: 'var(--bg-subtle)'
      }}>
        <div className="animate-fade-in" style={{ 
          display: 'flex', 
          flexDirection: 'column', 
          alignItems: 'center', 
          gap: '16px' 
        }}>
          <div className="float-animation">
            <Zap size={48} color="var(--primary)" fill="var(--primary)" />
          </div>
          <div style={{ fontSize: '1.2rem', color: 'var(--primary)', fontWeight: 600 }}>
            Initializing Reelzy...
          </div>
        </div>
      </div>
    );
  }

  return (
    <Routes>
      <Route 
        path="/" 
        element={
          <LandingPage 
            user={user} 
            onLoginClick={() => navigate(user ? '/dashboard' : '/login')} 
          />
        } 
      />
      <Route 
        path="/dashboard" 
        element={
          user ? <Dashboard user={user} onLogout={handleLogout} /> : <Navigate to="/" replace />
        } 
      />
      <Route 
        path="/login" 
        element={
          user ? <Navigate to="/dashboard" replace /> : <Login onBack={() => navigate('/')} />
        } 
      />
      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
