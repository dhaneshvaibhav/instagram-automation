import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Zap, ArrowLeft, Check, X, Crown, Rocket, Star, 
  MessageSquare, Send, Bot, Shield, Clock, Sparkles,
  ArrowRight, Gift, Loader2, AlertTriangle, CheckCircle2
} from 'lucide-react';
import api from '../api';

const Pricing = () => {
  const [isFirstTime, setIsFirstTime] = useState(true);
  const [currentPlan, setCurrentPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [upgrading, setUpgrading] = useState(null); // plan id being upgraded
  const [toast, setToast] = useState(null); // { type: 'success' | 'error', message }
  const navigate = useNavigate();

  // Fetch current subscription on mount
  useEffect(() => {
    fetchSubscription();
  }, []);

  const fetchSubscription = async () => {
    try {
      const res = await api.get('/api/subscription');
      setCurrentPlan(res.data);
      if (res.data.is_first_time !== undefined) {
        setIsFirstTime(res.data.is_first_time);
      }
    } catch (err) {
      console.error('Failed to fetch subscription:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectPlan = async (planId) => {
    // If already on this plan, do nothing
    if (currentPlan?.plan === planId) return;

    setUpgrading(planId);
    setToast(null);
    
    try {
      const res = await api.post('/api/subscription', { plan: planId });
      setCurrentPlan(res.data);
      setToast({ 
        type: 'success', 
        message: `Successfully ${currentPlan?.plan ? 'switched' : 'subscribed'} to ${res.data.plan.charAt(0).toUpperCase() + res.data.plan.slice(1)} plan!` 
      });
      // Refresh subscription data
      await fetchSubscription();
    } catch (err) {
      const detail = err.response?.data?.detail || 'Failed to update plan. Please connect your Instagram account first.';
      setToast({ type: 'error', message: detail });
    } finally {
      setUpgrading(null);
      // Auto-dismiss toast after 5s
      setTimeout(() => setToast(null), 5000);
    }
  };

  const plans = [
    {
      id: 'starter',
      name: 'Starter',
      icon: <Zap size={28} />,
      price: 100,
      period: '/month',
      billing: 'Billed monthly',
      color: 'var(--info)',
      colorBg: 'var(--info-bg)',
      badge: null,
      features: [
        { text: 'Auto Comment Detection', included: true },
        { text: 'Keyword-based Triggers', included: true },
        { text: 'Automated DM Sending', included: true },
        { text: 'Basic Analytics Dashboard', included: true },
        { text: 'Up to 3 Active Reels', included: true },
        { text: 'Auto-reply to Incoming DMs', included: false },
        { text: 'Priority Support', included: false },
        { text: 'Early Access to New Features', included: false },
      ],
      cta: 'Get Started',
    },
    {
      id: 'pro',
      name: 'Professional',
      icon: <Crown size={28} />,
      price: 499,
      period: '/5 months',
      billing: isFirstTime ? '5 months + 1 month FREE' : 'Billed every 5 months',
      color: 'var(--primary)',
      colorBg: 'var(--success-bg)',
      badge: 'Most Popular',
      features: [
        { text: 'Auto Comment Detection', included: true },
        { text: 'Keyword-based Triggers', included: true },
        { text: 'Automated DM Sending', included: true },
        { text: 'Full Analytics Dashboard', included: true },
        { text: 'Unlimited Active Reels', included: true },
        { text: 'Auto-reply to Incoming DMs', included: true },
        { text: 'Priority Support', included: true },
        { text: 'Early Access to New Features', included: false },
      ],
      cta: 'Upgrade to Pro',
    },
    {
      id: 'business',
      name: 'Business',
      icon: <Rocket size={28} />,
      price: 1149,
      period: '/10 months',
      billing: isFirstTime ? '10 months + 2 months FREE' : 'Billed every 10 months',
      color: 'var(--accent)',
      colorBg: 'var(--warning-bg)',
      badge: 'Best Value',
      features: [
        { text: 'Auto Comment Detection', included: true },
        { text: 'Keyword-based Triggers', included: true },
        { text: 'Automated DM Sending', included: true },
        { text: 'Advanced Analytics & Reports', included: true },
        { text: 'Unlimited Active Reels', included: true },
        { text: 'Auto-reply to Incoming DMs', included: true },
        { text: 'Priority Support', included: true },
        { text: 'Early Access to New Features', included: true },
      ],
      cta: 'Go Business',
    },
  ];

  const getCtaText = (plan) => {
    if (upgrading === plan.id) return 'Processing...';
    if (currentPlan?.plan === plan.id) return 'Current Plan';
    return plan.cta;
  };

  const isCurrentPlan = (planId) => currentPlan?.plan === planId;

  return (
    <div className="pricing-page" style={{ backgroundColor: 'var(--bg-main)', minHeight: '100vh' }}>
      {/* Toast notification */}
      {toast && (
        <div style={{
          position: 'fixed', top: '20px', right: '20px', zIndex: 1000,
          padding: '14px 24px', borderRadius: '12px', display: 'flex', alignItems: 'center', gap: '10px',
          background: toast.type === 'success' ? 'var(--success)' : 'var(--danger)',
          color: 'white', fontWeight: 500, fontSize: '0.9rem',
          boxShadow: '0 8px 30px rgba(0,0,0,0.15)',
          animation: 'slideDown 0.3s ease',
        }}>
          {toast.type === 'success' ? <CheckCircle2 size={18} /> : <AlertTriangle size={18} />}
          {toast.message}
        </div>
      )}

      {/* Navbar */}
      <nav className="navbar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Zap size={24} fill="var(--primary)" color="var(--primary)" />
          <Link to="/" style={{ fontFamily: 'var(--font-heading)', fontSize: '1.25rem', fontWeight: 700, color: 'var(--primary)', textDecoration: 'none' }}>
            Reelzy
          </Link>
        </div>
        <Link to="/" className="btn btn-secondary btn-small">
          <ArrowLeft size={16} /> Back to Home
        </Link>
      </nav>

      {/* Hero */}
      <header className="pricing-header">
        <div className="container" style={{ maxWidth: '1100px' }}>
          <div className="animate-fade-in" style={{ textAlign: 'center' }}>
            <span className="badge badge-success" style={{ marginBottom: '20px' }}>
              <Sparkles size={12} style={{ marginRight: '4px' }} /> Simple, Transparent Pricing
            </span>
            <h1 style={{
              fontFamily: 'var(--font-heading)', fontSize: '3rem',
              color: 'var(--text-main)', marginBottom: '16px', letterSpacing: '-0.02em'
            }}>
              Choose Your Growth Plan
            </h1>
            <p className="text-muted" style={{ fontSize: '1.1rem', maxWidth: '600px', margin: '0 auto 32px', lineHeight: 1.6 }}>
              Start automating your Instagram engagement today. No hidden fees, cancel anytime.
            </p>

            {/* Current plan indicator */}
            {!loading && currentPlan?.plan && (
              <div style={{
                display: 'inline-flex', alignItems: 'center', gap: '8px',
                padding: '8px 16px', borderRadius: 'var(--radius-full)',
                background: 'var(--bg-main)', border: '1px solid var(--primary)',
                fontSize: '0.85rem', fontWeight: 600, color: 'var(--primary)',
                marginBottom: '24px',
              }}>
                <CheckCircle2 size={14} />
                Current Plan: {currentPlan.plan.charAt(0).toUpperCase() + currentPlan.plan.slice(1)}
                {currentPlan.is_trial && <span style={{ color: 'var(--warning)', fontSize: '0.75rem' }}>(Trial)</span>}
              </div>
            )}

            {/* First-time user toggle */}
            <div className="pricing-toggle animate-slide-up delay-1">
              <button
                className={`pricing-toggle-btn ${isFirstTime ? 'active' : ''}`}
                onClick={() => setIsFirstTime(true)}
              >
                <Gift size={16} /> First-time User
              </button>
              <button
                className={`pricing-toggle-btn ${!isFirstTime ? 'active' : ''}`}
                onClick={() => setIsFirstTime(false)}
              >
                Returning User
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Pricing Cards */}
      <main className="pricing-content">
        <div className="container" style={{ maxWidth: '1100px' }}>
          <div className="pricing-grid">
            {plans.map((plan, index) => (
              <div
                key={plan.id}
                className={`pricing-card animate-slide-up ${plan.badge === 'Most Popular' ? 'pricing-card-featured' : ''} ${isCurrentPlan(plan.id) ? 'pricing-card-current' : ''}`}
                style={{ animationDelay: `${0.15 * index}s` }}
              >
                {/* Badge */}
                {plan.badge && (
                  <div className="pricing-badge" style={{
                    background: plan.badge === 'Most Popular' ? 'var(--primary)' : 'var(--accent)',
                    color: 'white'
                  }}>
                    <Star size={12} /> {plan.badge}
                  </div>
                )}

                {/* Current plan label */}
                {isCurrentPlan(plan.id) && (
                  <div style={{
                    position: 'absolute', top: '12px', left: '16px',
                    display: 'flex', alignItems: 'center', gap: '4px',
                    fontSize: '0.7rem', fontWeight: 700,
                    color: 'var(--success)', textTransform: 'uppercase', letterSpacing: '0.05em',
                  }}>
                    <CheckCircle2 size={12} /> Active
                  </div>
                )}

                {/* Header */}
                <div className="pricing-card-header">
                  <div className="pricing-icon" style={{ background: plan.colorBg, color: plan.color }}>
                    {plan.icon}
                  </div>
                  <h3 className="pricing-plan-name">{plan.name}</h3>
                  <div className="pricing-price">
                    <span className="pricing-currency">₹</span>
                    <span className="pricing-amount">{plan.price}</span>
                    <span className="pricing-period">{plan.period}</span>
                  </div>
                  <div className="pricing-billing">
                    {isFirstTime && plan.id !== 'starter' && (
                      <Gift size={14} color="var(--success)" style={{ marginRight: '4px' }} />
                    )}
                    {plan.billing}
                  </div>
                </div>

                {/* Features */}
                <div className="pricing-features">
                  {plan.features.map((feature, i) => (
                    <div
                      key={i}
                      className={`pricing-feature ${!feature.included ? 'pricing-feature-disabled' : ''}`}
                    >
                      {feature.included ? (
                        <Check size={16} color="var(--success)" strokeWidth={3} />
                      ) : (
                        <X size={16} color="var(--border-color)" strokeWidth={2} />
                      )}
                      <span>{feature.text}</span>
                    </div>
                  ))}
                </div>

                {/* CTA */}
                <button
                  className={`btn ${isCurrentPlan(plan.id) ? 'btn-secondary' : plan.badge === 'Most Popular' ? 'btn-primary' : 'btn-secondary'} pricing-cta`}
                  style={{ padding: '14px 28px', fontSize: '0.95rem' }}
                  onClick={() => handleSelectPlan(plan.id)}
                  disabled={isCurrentPlan(plan.id) || upgrading !== null}
                >
                  {upgrading === plan.id && <Loader2 size={16} className="animate-spin" style={{ animation: 'spin 1s linear infinite' }} />}
                  {getCtaText(plan)} {!isCurrentPlan(plan.id) && upgrading !== plan.id && <ArrowRight size={16} />}
                </button>
              </div>
            ))}
          </div>

          {/* Usage Info */}
          {!loading && currentPlan?.usage && (
            <div className="pricing-trust animate-slide-up delay-2" style={{ marginBottom: '32px' }}>
              <div className="pricing-trust-item" style={{ flex: 1 }}>
                <Zap size={20} color="var(--primary)" />
                <div>
                  <strong>Reels Used</strong>
                  <p className="text-muted text-small">
                    {currentPlan.usage.reels_used} / {currentPlan.usage.reels_limit === -1 ? '∞' : currentPlan.usage.reels_limit} active reels
                  </p>
                </div>
              </div>
              <div className="pricing-trust-item" style={{ flex: 1 }}>
                <Shield size={20} color={currentPlan.limits?.auto_reply ? 'var(--success)' : 'var(--text-muted)'} />
                <div>
                  <strong>Auto-Reply</strong>
                  <p className="text-muted text-small">
                    {currentPlan.limits?.auto_reply ? '✅ Enabled' : '❌ Not available on your plan'}
                  </p>
                </div>
              </div>
              <div className="pricing-trust-item" style={{ flex: 1 }}>
                <Clock size={20} color="var(--primary)" />
                <div>
                  <strong>Expires</strong>
                  <p className="text-muted text-small">
                    {currentPlan.expires_at ? new Date(currentPlan.expires_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) : 'N/A'}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Trust Section */}
          <div className="pricing-trust animate-slide-up delay-3">
            <div className="pricing-trust-item">
              <Shield size={20} color="var(--primary)" />
              <div>
                <strong>Secure Payments</strong>
                <p className="text-muted text-small">All payments processed securely via encrypted channels</p>
              </div>
            </div>
            <div className="pricing-trust-item">
              <Clock size={20} color="var(--primary)" />
              <div>
                <strong>Cancel Anytime</strong>
                <p className="text-muted text-small">No lock-in contracts, cancel your plan anytime</p>
              </div>
            </div>
            <div className="pricing-trust-item">
              <Bot size={20} color="var(--primary)" />
              <div>
                <strong>Official Meta API</strong>
                <p className="text-muted text-small">100% compliant with Instagram's platform policies</p>
              </div>
            </div>
          </div>

          {/* FAQ-like comparison */}
          <div className="pricing-comparison animate-slide-up">
            <h2 style={{ fontFamily: 'var(--font-heading)', textAlign: 'center', marginBottom: '32px', fontSize: '1.5rem' }}>
              What's Included in Each Plan
            </h2>
            <div className="pricing-compare-table">
              <div className="pricing-compare-row pricing-compare-header">
                <div className="pricing-compare-feature">Feature</div>
                <div className="pricing-compare-plan">Starter</div>
                <div className="pricing-compare-plan">Pro</div>
                <div className="pricing-compare-plan">Business</div>
              </div>
              {[
                { feature: 'Auto Comment Detection', starter: true, pro: true, business: true },
                { feature: 'Keyword Triggers', starter: true, pro: true, business: true },
                { feature: 'Automated DM Sending', starter: true, pro: true, business: true },
                { feature: 'Active Reels Limit', starter: '7 days free trial', pro: 'Unlimited', business: 'Unlimited' },
                { feature: 'Auto-reply to DMs', starter: false, pro: true, business: true },
                { feature: 'Analytics Dashboard', starter: 'Basic', pro: 'Full', business: 'Advanced' },
                { feature: 'Priority Support', starter: false, pro: true, business: true },
                { feature: 'New Features Early Access', starter: false, pro: false, business: true },
                { feature: 'First-time Bonus', starter: '—', pro: '+1 Month Free', business: '+2 Months Free' },
              ].map((row, i) => (
                <div key={i} className="pricing-compare-row">
                  <div className="pricing-compare-feature">{row.feature}</div>
                  {['starter', 'pro', 'business'].map((plan) => (
                    <div key={plan} className="pricing-compare-plan">
                      {typeof row[plan] === 'boolean' ? (
                        row[plan] ? <Check size={16} color="var(--success)" strokeWidth={3} /> : <X size={16} color="#d6d3d1" />
                      ) : (
                        <span className={row[plan] === '—' ? 'text-muted' : ''} style={{ fontSize: '0.85rem', fontWeight: row[plan].includes('Free') || row[plan] === 'Unlimited' ? 600 : 400 }}>
                          {row[plan]}
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
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
            <Link to="/" style={{ color: 'inherit', textDecoration: 'none' }}>Home</Link>
            <Link to="/terms" style={{ color: 'inherit', textDecoration: 'none' }}>Terms</Link>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Pricing;
