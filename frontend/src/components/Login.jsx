import React from 'react';
import { Instagram } from 'lucide-react';
import api from '../api';

const Login = () => {
  return (
    <div className="login-screen">
      <div className="login-card">
        <Instagram className="instagram-logo" size={64} />
        <h2>Connect your Instagram</h2>
        <p>Login to start sending automatic DMs to your loyal followers</p>
        <a href="http://localhost:5000/auth/login" className="btn-connect" style={{ display: 'block', textDecoration: 'none', lineHeight: '20px' }}>
          Connect Instagram
        </a>
      </div>
    </div>
  );
};

export default Login;
