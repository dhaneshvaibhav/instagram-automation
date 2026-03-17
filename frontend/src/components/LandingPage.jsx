import React, { useState, useEffect } from 'react';
import { 
  Instagram, 
  Zap, 
  ShieldCheck, 
  BarChart3, 
  MessageSquare, 
  ArrowRight,
  CheckCircle2
} from 'lucide-react';

const LandingPage = ({ onLoginClick }) => {
  const [typedText, setTypedText] = useState('');
  const fullText = "Automatically.";
  
  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      setTypedText(fullText.slice(0, i + 1));
      i++;
      if (i >= fullText.length) clearInterval(interval);
    }, 150);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="landing-page" style={{ backgroundColor: 'var(--bg-main)' }}>
      {/* Navbar */}
      <nav style={{ 
        display: 'flex', justifyContent: 'space-between', alignItems: 'center', 
        padding: '20px 40px', position: 'sticky', top: 0, backgroundColor: 'rgba(255,255,255,0.8)',
        backdropFilter: 'blur(10px)', zIndex: 100, borderBottom: '1px solid var(--border-color)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Zap size={24} fill="var(--primary)" color="var(--primary)" />
          <span style={{ fontFamily: 'var(--font-heading)', fontSize: '1.25rem', fontWeight: 700, color: 'var(--primary)' }}>Reelzy</span>
        </div>
        <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
          <a href="#features" className="text-muted" style={{ textDecoration: 'none', fontSize: '0.9rem' }}>Features</a>
          <button onClick={onLoginClick} className="btn btn-primary btn-small">
            Get Started
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <header style={{ 
        padding: '80px 20px 120px 20px', textAlign: 'center', 
        backgroundImage: 'radial-gradient(circle at top right, var(--info-bg), transparent), radial-gradient(circle at bottom left, var(--success-bg), transparent)',
        overflow: 'hidden'
      }}>
        <div className="container" style={{ maxWidth: '850px' }}>
          <div className="badge badge-info animate-fade-in" style={{ marginBottom: '24px' }}>
            New: Smart Keyword Filtering is Live
          </div>
          <h1 className="animate-slide-up" style={{ fontSize: '4.5rem', marginBottom: '24px', lineHeight: 1.1, letterSpacing: '-0.02em', minHeight: '135px' }}>
            Stop Chasing Leads. Let Your Reels Do the Work <br />
            <span style={{ color: 'var(--primary)', fontStyle: 'italic' }}>
              {typedText}
              <span style={{ borderRight: '3px solid var(--primary)', marginLeft: '4px', animation: 'fadeIn 0.8s infinite' }}></span>
            </span>
          </h1>
          <p className="text-muted animate-slide-up delay-1" style={{ fontSize: '1.25rem', marginBottom: '40px', lineHeight: 1.6, maxWidth: '750px', marginInline: 'auto' }}>
            The all-in-one engagement engine for Instagram creators. Convert every comment into a conversation, 
            a lead, or a sale—instantly and securely.
          </p>
          <div className="animate-slide-up delay-2" style={{ display: 'flex', gap: '16px', justifyContent: 'center', marginBottom: '60px' }}>
            <button onClick={onLoginClick} className="btn btn-primary" style={{ padding: '16px 36px', fontSize: '1rem' }}>
              Connect Instagram Now <ArrowRight size={18} />
            </button>
            <button className="btn btn-secondary" style={{ padding: '16px 36px', fontSize: '1rem' }}>
              Watch Demo
            </button>
          </div>
          
          {/* Mock Social Proof */}
          <div className="animate-slide-up delay-3" style={{ display: 'flex', justifyContent: 'center', gap: '48px', opacity: 0.7 }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <span style={{ fontSize: '1.75rem', fontWeight: 800 }}>50k+</span>
              <span className="text-xs text-muted" style={{ textTransform: 'uppercase', letterSpacing: '0.05em' }}>DMs Sent</span>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <span style={{ fontSize: '1.75rem', fontWeight: 800 }}>2k+</span>
              <span className="text-xs text-muted" style={{ textTransform: 'uppercase', letterSpacing: '0.05em' }}>Creators</span>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <span style={{ fontSize: '1.75rem', fontWeight: 800 }}>4.9/5</span>
              <span className="text-xs text-muted" style={{ textTransform: 'uppercase', letterSpacing: '0.05em' }}>User Rating</span>
            </div>
          </div>
        </div>
      </header>

      {/* Bento Grid Features */}
      <section id="features" style={{ padding: '120px 20px', backgroundColor: 'var(--bg-subtle)' }}>
        <div className="container">
          <div style={{ textAlign: 'center', marginBottom: '80px' }}>
            <h2 style={{ fontSize: '3rem', marginBottom: '16px' }}>Powerful Features</h2>
            <p className="text-muted" style={{ fontSize: '1.1rem' }}>Engineered for creators who value their time and community.</p>
          </div>
          
          <div className="bento-grid">
            {/* Main Feature - Large Box */}
            <div className="bento-item" style={{ gridColumn: 'span 2', gridRow: 'span 2', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
              <div>
                <div style={{ marginBottom: '24px', width: '56px', height: '56px', borderRadius: '16px', backgroundColor: 'var(--success-bg)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Zap className="text-success" size={28} />
                </div>
                <h3 style={{ fontSize: '1.75rem', marginBottom: '16px' }}>Real-time Response Engine</h3>
                <p className="text-muted" style={{ fontSize: '1rem', lineHeight: '1.6' }}>
                  Our advanced engine processes comments within milliseconds. Whether it's 2 AM or mid-launch, 
                  Reelzy ensures every lead gets the attention they deserve instantly.
                </p>
              </div>
              <div style={{ marginTop: '24px', padding: '16px', borderRadius: '12px', background: 'var(--bg-subtle)', border: '1px solid var(--border-color)', fontSize: '0.85rem' }}>
                <span className="badge badge-success" style={{ marginBottom: '8px' }}>Active</span>
                <div style={{ fontFamily: 'monospace' }}>Processing: IG_REEL_9821... Success</div>
              </div>
            </div>

            {/* Keyword Filtering */}
            <div className="bento-item" style={{ gridColumn: 'span 2' }}>
              <div style={{ display: 'flex', gap: '24px', height: '100%' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ marginBottom: '16px', width: '40px', height: '40px', borderRadius: '10px', backgroundColor: 'var(--info-bg)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <MessageSquare className="text-info" size={20} />
                  </div>
                  <h3 style={{ marginBottom: '8px' }}>Smart Keyword Filtering</h3>
                  <p className="text-muted" style={{ fontSize: '0.9rem' }}>Filter high-intent buyers by setting custom trigger words like 'price' or 'link'.</p>
                </div>
                <div style={{ width: '120px', display: 'flex', flexWrap: 'wrap', gap: '4px', alignContent: 'center' }}>
                  <span className="badge badge-neutral">link</span>
                  <span className="badge badge-neutral">info</span>
                  <span className="badge badge-neutral">price</span>
                </div>
              </div>
            </div>

            {/* Security */}
            <div className="bento-item">
              <div style={{ marginBottom: '16px', width: '40px', height: '40px', borderRadius: '10px', backgroundColor: 'var(--danger-bg)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <ShieldCheck className="text-danger" size={20} />
              </div>
              <h3 style={{ marginBottom: '8px', fontSize: '1.1rem' }}>Secure Login</h3>
              <p className="text-muted" style={{ fontSize: '0.85rem' }}>Official Meta Graph API integration keeps your credentials safe.</p>
            </div>

            {/* Stats */}
            <div className="bento-item">
              <div style={{ marginBottom: '16px', width: '40px', height: '40px', borderRadius: '10px', backgroundColor: 'var(--warning-bg)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <BarChart3 className="text-warning" size={20} />
              </div>
              <h3 style={{ marginBottom: '8px', fontSize: '1.1rem' }}>Analytics</h3>
              <p className="text-muted" style={{ fontSize: '0.85rem' }}>Monitor performance and growth with built-in tracking.</p>
            </div>
          </div>
        </div>
      </section>

      {/* How it Works - Redesigned */}
      <section style={{ padding: '120px 20px', backgroundColor: 'var(--bg-main)' }}>
        <div className="container">
          <div style={{ textAlign: 'center', marginBottom: '80px' }}>
            <span className="badge badge-info" style={{ marginBottom: '16px' }}>The Workflow</span>
            <h2 style={{ fontSize: '3rem', marginBottom: '16px' }}>From Setup to Scale in Minutes</h2>
            <p className="text-muted" style={{ fontSize: '1.1rem', maxWidth: '600px', marginInline: 'auto' }}>
              We've simplified the complexity of the Instagram API into a four-step professional workflow.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '24px', position: 'relative' }}>
            {/* Connecting Line (Desktop) */}
            <div style={{ 
              position: 'absolute', top: '40px', left: '100px', right: '100px', height: '1px', 
              background: 'linear-gradient(to right, transparent, var(--border-color), transparent)',
              zIndex: 0,
              display: window.innerWidth > 1024 ? 'block' : 'none'
            }}></div>

            {[
              { 
                icon: <Zap size={24} className="text-primary" />, 
                step: "01", 
                title: "Connect", 
                desc: "Link your Business account via Meta's secure OAuth portal." 
              },
              { 
                icon: <BarChart3 size={24} className="text-primary" />, 
                step: "02", 
                title: "Analyze", 
                desc: "Reelzy syncs your latest media and engagement stats automatically." 
              },
              { 
                icon: <MessageSquare size={24} className="text-primary" />, 
                step: "03", 
                title: "Configure", 
                desc: "Define your trigger keywords and craft your personalized DM responses." 
              },
              { 
                icon: <CheckCircle2 size={24} className="text-primary" />, 
                step: "04", 
                title: "Automate", 
                desc: "Switch on the engine and watch your Reels convert 24/7." 
              }
            ].map((s, i) => (
              <div key={i} className="animate-slide-up" style={{ 
                animationDelay: `${0.2 * i}s`,
                background: 'var(--bg-subtle)',
                padding: '32px',
                borderRadius: 'var(--radius-lg)',
                border: '1px solid var(--border-color)',
                textAlign: 'center',
                zIndex: 1,
                position: 'relative'
              }}>
                <div style={{ 
                  width: '64px', height: '64px', borderRadius: 'var(--radius-full)', 
                  backgroundColor: 'var(--bg-main)', border: '1px solid var(--border-color)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  margin: '0 auto 24px',
                  boxShadow: 'var(--shadow-sm)'
                }}>
                  {s.icon}
                </div>
                <div style={{ 
                  fontSize: '0.75rem', fontWeight: 800, color: 'var(--primary)', 
                  letterSpacing: '0.1em', marginBottom: '12px' 
                }}>
                  STEP {s.step}
                </div>
                <h3 style={{ marginBottom: '12px', fontSize: '1.25rem' }}>{s.title}</h3>
                <p className="text-muted" style={{ fontSize: '0.9rem', lineHeight: '1.5' }}>{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Simple Footer */}
      <footer style={{ padding: '40px 20px', borderTop: '1px solid var(--border-color)', backgroundColor: 'var(--bg-subtle)' }}>
        <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', opacity: 0.6 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Zap size={18} fill="var(--primary)" color="var(--primary)" />
            <span style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--text-main)', fontFamily: 'var(--font-heading)' }}>Reelzy</span>
          </div>
          <p style={{ fontSize: '0.8rem', margin: 0 }}>
            An <a href="https://adjunct.in" target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'underline', color: 'inherit' }}>Adjunct Product</a>. © 2026.
          </p>
          <div style={{ display: 'flex', gap: '16px', fontSize: '0.8rem' }}>
            <button onClick={onLoginClick} style={{ background: 'none', border: 'none', padding: 0, fontSize: 'inherit', cursor: 'pointer', color: 'inherit' }}>Login</button>
            <span>Privacy</span>
            <span>Terms</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
