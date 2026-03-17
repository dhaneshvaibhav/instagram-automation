import React from 'react';
import { Instagram } from 'lucide-react';

const Login = () => {
  return (
    <div className="login-screen">
      <div className="login-card">
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 'var(--spacing-lg)' }}>
          <div style={{ padding: '16px', borderRadius: '50%', backgroundColor: 'var(--bg-subtle)' }}>
            <Instagram size={48} color="var(--primary)" />
          </div>
        </div>
        <h2 style={{ fontSize: '1.5rem', marginBottom: 'var(--spacing-sm)' }}>Connect your Instagram</h2>
        <p className="text-muted" style={{ marginBottom: 'var(--spacing-xl)' }}>
          Login to start sending automatic DMs to your loyal followers
        </p>
        <a 
          href="http://localhost:5000/auth/login" 
          className="btn btn-primary" 
          style={{ display: 'flex', textDecoration: 'none', width: '100%', padding: '12px' }}
        >
          Connect Instagram
        </a>
      </div>
    </div>
  );
};

export default Login;
