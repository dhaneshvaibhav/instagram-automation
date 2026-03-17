import React from 'react';
import { Instagram, Zap, MessageSquare, BarChart3, CheckCircle2 } from 'lucide-react';

const Login = ({ onBack }) => {
  return (
    <div className="split-screen">
      {/* Left Side: Login Form */}
      <div className="split-left">
        <div style={{ maxWidth: '400px', width: '100%' }}>
          <button 
            onClick={onBack}
            className="btn btn-ghost btn-small" 
            style={{ padding: 0, marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '4px' }}
          >
            ← Back to Home
          </button>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '40px' }}>
            <Zap size={24} fill="var(--primary)" color="var(--primary)" />
            <span style={{ fontFamily: 'var(--font-heading)', fontSize: '1.25rem', fontWeight: 700, color: 'var(--primary)' }}>
              Reelzy
            </span>
          </div>
          
          <h1 style={{ fontSize: '2.25rem', marginBottom: '16px' }}>Welcome back.</h1>
          <p className="text-muted" style={{ marginBottom: '40px' }}>
            Reconnect to your audience and continue scaling your engagement with Reelzy.
          </p>
          
          <a 
            href={`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/auth/login`} 
            className="btn btn-primary" 
            style={{ 
              display: 'flex', width: '100%', padding: '16px', fontSize: '1rem',
              gap: '12px'
            }}
          >
            <Instagram size={20} />
            Login with Instagram
          </a>
          
          <p style={{ marginTop: '32px', fontSize: '0.85rem', color: 'var(--text-muted)', textAlign: 'center' }}>
            By continuing, you agree to our Terms of Service and Privacy Policy.
          </p>
        </div>
      </div>

      {/* Right Side: Features/Branding */}
      <div className="split-right">
        <div style={{ maxWidth: '500px' }}>
          <h2 style={{ color: 'white', fontSize: '2.5rem', marginBottom: '40px' }}>
            Scale your reach, <br />
            not your workload.
          </h2>

          <div className="animate-slide-up delay-1">
            <div className="feature-tag">
              <Zap size={24} color="var(--primary)" />
              <div>
                <strong style={{ display: 'block' }}>Real-time Responses</strong>
                <span className="text-xs" style={{ opacity: 0.7 }}>Instant DM delivery on every comment.</span>
              </div>
            </div>
          </div>

          <div className="animate-slide-up delay-2">
            <div className="feature-tag">
              <MessageSquare size={24} color="var(--primary)" />
              <div>
                <strong style={{ display: 'block' }}>Smart Filtering</strong>
                <span className="text-xs" style={{ opacity: 0.7 }}>Filter leads with powerful keyword triggers.</span>
              </div>
            </div>
          </div>

          <div className="animate-slide-up delay-3">
            <div className="feature-tag">
              <BarChart3 size={24} color="var(--primary)" />
              <div>
                <strong style={{ display: 'block' }}>Growth Analytics</strong>
                <span className="text-xs" style={{ opacity: 0.7 }}>Track performance and conversion in real-time.</span>
              </div>
            </div>
          </div>

          <div style={{ marginTop: '60px', padding: '24px', borderRadius: 'var(--radius-lg)', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.1)' }}>
            <p style={{ fontStyle: 'italic', opacity: 0.8, fontSize: '1rem', lineHeight: '1.6', marginBottom: '16px' }}>
              "Reelzy saved me over 15 hours a week in manual DMs. My engagement has never been higher."
            </p>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'var(--primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', fontWeight: 800 }}>SK</div>
              <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>Sarah K. • Content Creator</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
