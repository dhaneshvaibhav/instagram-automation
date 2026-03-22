import React from 'react';
import { Link } from 'react-router-dom';
import { Zap, ArrowLeft, Shield, Lock, Eye, Database, Globe, UserCheck, Bell, FileText, Mail } from 'lucide-react';

const PrivacyPolicy = () => {
  return (
    <div className="terms-page" style={{ backgroundColor: 'var(--bg-main)', minHeight: '100vh' }}>
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

      {/* Header */}
      <header className="terms-header">
        <div className="container" style={{ maxWidth: '900px' }}>
          <div className="animate-fade-in" style={{ textAlign: 'center' }}>
            <div className="terms-icon-badge">
              <Shield size={28} />
            </div>
            <h1 style={{
              fontFamily: 'var(--font-heading)', fontSize: '2.75rem',
              color: 'var(--text-main)', marginBottom: '16px', letterSpacing: '-0.02em'
            }}>
              Privacy Policy
            </h1>
            <p className="text-muted" style={{ fontSize: '1rem', maxWidth: '600px', margin: '0 auto 24px', lineHeight: 1.6 }}>
              Your privacy is important to us. This policy explains how Reelzy collects, uses, and protects your personal information.
            </p>
            <div style={{ display: 'flex', justifyContent: 'center', gap: '24px', flexWrap: 'wrap' }}>
              <span className="badge badge-neutral">Effective Date: March 1, 2026</span>
              <span className="badge badge-neutral">Last Updated: March 23, 2026</span>
            </div>
          </div>
        </div>
      </header>

      {/* Content */}
      <main style={{ padding: '48px 20px 80px', backgroundColor: 'var(--bg-subtle)' }}>
        <div className="container" style={{ maxWidth: '900px' }}>

          {/* Section 1 */}
          <section className="terms-section animate-slide-up">
            <div className="terms-section-header">
              <span className="terms-section-number">01</span>
              <h2>Introduction</h2>
            </div>
            <div className="terms-section-body">
              <p>
                Reelzy ("we," "our," or "us"), a product of <strong>Adjunct</strong>, operates the Reelzy platform 
                (the "Service") — an Instagram automation tool that enables automated direct messaging, 
                comment-triggered responses, and engagement analytics.
              </p>
              <p>
                This Privacy Policy describes how we collect, use, store, and share information when you use 
                our Service. By accessing or using Reelzy, you consent to the practices described in this policy.
              </p>
              <div className="terms-callout">
                <Shield size={18} color="var(--primary)" style={{ flexShrink: 0, marginTop: '2px' }} />
                <div>
                  <strong>Our Commitment</strong>
                  <p style={{ margin: '4px 0 0', fontSize: '0.875rem' }}>
                    We are committed to protecting your data. Reelzy uses only official Meta APIs and never stores 
                    your Instagram password.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Section 2 */}
          <section className="terms-section animate-slide-up delay-1">
            <div className="terms-section-header">
              <span className="terms-section-number">02</span>
              <h2>Information We Collect</h2>
            </div>
            <div className="terms-section-body">
              <p>We collect the following categories of information when you use Reelzy:</p>
              
              <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1rem', margin: '20px 0 12px', color: 'var(--text-main)' }}>
                <Lock size={16} style={{ marginRight: '6px', verticalAlign: 'text-bottom' }} />
                Account & Authentication Data
              </h3>
              <ul className="terms-list">
                <li>Instagram account ID and username</li>
                <li>Profile picture URL, biography, and follower/following counts</li>
                <li>OAuth 2.0 access tokens (issued by Meta, not your password)</li>
                <li>Token expiry timestamps</li>
              </ul>

              <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1rem', margin: '20px 0 12px', color: 'var(--text-main)' }}>
                <Database size={16} style={{ marginRight: '6px', verticalAlign: 'text-bottom' }} />
                Content & Engagement Data
              </h3>
              <ul className="terms-list">
                <li>Published Reel metadata (media IDs, captions, timestamps)</li>
                <li>Comment text and commenter identifiers on tracked Reels</li>
                <li>Automation rules you configure (keywords, DM templates, button payloads)</li>
                <li>DM delivery logs and engagement analytics (send counts, success rates)</li>
              </ul>

              <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1rem', margin: '20px 0 12px', color: 'var(--text-main)' }}>
                <Globe size={16} style={{ marginRight: '6px', verticalAlign: 'text-bottom' }} />
                Technical Data
              </h3>
              <ul className="terms-list">
                <li>Browser type, IP address, and device information</li>
                <li>Usage patterns (pages visited, features used, session duration)</li>
                <li>Error logs for debugging and service improvement</li>
              </ul>
            </div>
          </section>

          {/* Section 3 */}
          <section className="terms-section animate-slide-up delay-1">
            <div className="terms-section-header">
              <span className="terms-section-number">03</span>
              <h2>How We Use Your Information</h2>
            </div>
            <div className="terms-section-body">
              <p>We use collected information for the following purposes:</p>
              <ul className="terms-list">
                <li><strong>Service Delivery</strong> — To authenticate your account, fetch your Reels, process webhook events, and send automated DMs on your behalf.</li>
                <li><strong>Analytics & Dashboard</strong> — To display engagement statistics, DM delivery rates, and comment activity in your dashboard.</li>
                <li><strong>Automation Engine</strong> — To match incoming comments against your configured keywords and trigger the appropriate DM responses.</li>
                <li><strong>Token Management</strong> — To refresh and maintain valid access tokens so your automation runs uninterrupted.</li>
                <li><strong>Service Improvement</strong> — To analyze usage patterns, fix bugs, and improve the performance and reliability of Reelzy.</li>
                <li><strong>Communication</strong> — To notify you of important service updates, security alerts, or changes to this policy.</li>
              </ul>
              <div className="terms-callout" style={{ borderLeft: '3px solid var(--info)' }}>
                <Eye size={18} color="var(--info)" style={{ flexShrink: 0, marginTop: '2px' }} />
                <div>
                  <strong>No Selling of Data</strong>
                  <p style={{ margin: '4px 0 0', fontSize: '0.875rem' }}>
                    We do not sell, rent, or trade your personal information or Instagram data to third parties 
                    for marketing or advertising purposes.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Section 4 */}
          <section className="terms-section animate-slide-up delay-2">
            <div className="terms-section-header">
              <span className="terms-section-number">04</span>
              <h2>Data Storage & Security</h2>
            </div>
            <div className="terms-section-body">
              <p>
                We implement industry-standard security measures to protect your data:
              </p>
              <ul className="terms-list">
                <li><strong>Encrypted Storage</strong> — Access tokens and sensitive data are stored securely in our database with appropriate access controls.</li>
                <li><strong>HTTPS Only</strong> — All communication between your browser and our servers is encrypted via TLS/SSL.</li>
                <li><strong>Official API Integration</strong> — We use only Meta's official Graph API and Instagram Graph API, ensuring all interactions comply with Meta's security standards.</li>
                <li><strong>No Password Storage</strong> — We never receive, store, or have access to your Instagram password. Authentication is handled entirely through Meta's OAuth 2.0 flow.</li>
                <li><strong>Minimal Data Retention</strong> — We retain your data only for as long as your account is active or as needed to provide the Service.</li>
              </ul>
            </div>
          </section>

          {/* Section 5 */}
          <section className="terms-section animate-slide-up delay-2">
            <div className="terms-section-header">
              <span className="terms-section-number">05</span>
              <h2>Instagram & Meta Data Practices</h2>
            </div>
            <div className="terms-section-body">
              <p>
                Reelzy integrates with Instagram through Meta's official APIs. Here is specifically how we handle 
                your Instagram data:
              </p>
              <ul className="terms-list">
                <li><strong>API Permissions</strong> — We request <code>instagram_basic</code>, <code>instagram_manage_comments</code>, <code>instagram_manage_messages</code>, and <code>pages_messaging</code> scopes. No additional permissions are requested.</li>
                <li><strong>Data Fetching</strong> — We fetch your published Reels and their engagement metrics through the Instagram Graph API. This data powers your analytics dashboard.</li>
                <li><strong>Webhook Processing</strong> — We receive real-time notifications of new comments via Meta's webhook system. Comment data is processed to match your automation rules.</li>
                <li><strong>Messaging</strong> — Automated DMs are sent through the official Instagram Messaging API. All messages comply with Meta's messaging policies and rate limits.</li>
                <li><strong>Token Refresh</strong> — We automatically refresh your access tokens before expiry to ensure uninterrupted service.</li>
              </ul>
              <div className="terms-callout" style={{ borderLeft: '3px solid var(--success)' }}>
                <UserCheck size={18} color="var(--success)" style={{ flexShrink: 0, marginTop: '2px' }} />
                <div>
                  <strong>Meta Platform Compliance</strong>
                  <p style={{ margin: '4px 0 0', fontSize: '0.875rem' }}>
                    Reelzy fully complies with Meta's Platform Terms and Developer Policies. We undergo Meta's app review 
                    process and adhere to all data handling requirements set by Meta.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Section 6 */}
          <section className="terms-section animate-slide-up delay-3">
            <div className="terms-section-header">
              <span className="terms-section-number">06</span>
              <h2>Data Sharing & Third Parties</h2>
            </div>
            <div className="terms-section-body">
              <p>We may share your information only in the following limited circumstances:</p>
              <ul className="terms-list">
                <li><strong>Meta/Instagram</strong> — To operate the Service, we transmit data to Meta's APIs (message content, recipient IDs) as required to send DMs on your behalf.</li>
                <li><strong>Service Providers</strong> — We may use trusted third-party services for hosting, analytics, and error tracking. These providers are contractually bound to handle your data securely.</li>
                <li><strong>Legal Compliance</strong> — We may disclose information if required by law, regulation, or legal process (e.g., court order, subpoena).</li>
                <li><strong>Business Transfers</strong> — In the event of a merger, acquisition, or sale of assets, your data may be transferred as part of the transaction.</li>
              </ul>
              <p>
                We will <strong>never</strong> sell your personal data or Instagram engagement data to advertisers, 
                data brokers, or any other third parties.
              </p>
            </div>
          </section>

          {/* Section 7 */}
          <section className="terms-section animate-slide-up delay-3">
            <div className="terms-section-header">
              <span className="terms-section-number">07</span>
              <h2>Your Rights & Controls</h2>
            </div>
            <div className="terms-section-body">
              <p>You retain full control over your data and account:</p>
              <ul className="terms-list">
                <li><strong>Disconnect</strong> — You can disconnect your Instagram account from Reelzy at any time through the dashboard. This revokes our API access immediately.</li>
                <li><strong>Data Deletion</strong> — Upon disconnection or account deletion, we will delete your stored tokens, automation rules, and analytics data within 30 days.</li>
                <li><strong>Access & Export</strong> — You may request a copy of the data we hold about you by contacting us at the address below.</li>
                <li><strong>Correction</strong> — You may request correction of any inaccurate personal data we hold.</li>
                <li><strong>Opt-Out</strong> — You can pause or disable any automation at any time without contacting support.</li>
              </ul>
            </div>
          </section>

          {/* Section 8 */}
          <section className="terms-section animate-slide-up">
            <div className="terms-section-header">
              <span className="terms-section-number">08</span>
              <h2>Cookies & Tracking</h2>
            </div>
            <div className="terms-section-body">
              <p>
                Reelzy uses minimal cookies and local storage to maintain your session and preferences:
              </p>
              <ul className="terms-list">
                <li><strong>Session Cookies</strong> — To keep you logged in and maintain your authentication state.</li>
                <li><strong>Preference Cookies</strong> — To remember your dashboard settings and display preferences.</li>
                <li><strong>Analytics</strong> — We may use privacy-respecting analytics to understand how the Service is used. No advertising trackers are used.</li>
              </ul>
              <p>
                We do not use third-party advertising cookies, tracking pixels, or fingerprinting technologies.
              </p>
            </div>
          </section>

          {/* Section 9 */}
          <section className="terms-section animate-slide-up">
            <div className="terms-section-header">
              <span className="terms-section-number">09</span>
              <h2>Children's Privacy</h2>
            </div>
            <div className="terms-section-body">
              <p>
                Reelzy is not intended for use by individuals under the age of 18 (or the legal age of majority 
                in your jurisdiction). We do not knowingly collect personal information from minors. If we learn 
                that we have collected data from a child under 18, we will promptly delete such information.
              </p>
            </div>
          </section>

          {/* Section 10 */}
          <section className="terms-section animate-slide-up">
            <div className="terms-section-header">
              <span className="terms-section-number">10</span>
              <h2>Changes to This Policy</h2>
            </div>
            <div className="terms-section-body">
              <p>
                We may update this Privacy Policy from time to time to reflect changes in our practices, 
                technology, or legal requirements. When we make material changes, we will:
              </p>
              <ul className="terms-list">
                <li>Update the "Last Updated" date at the top of this policy.</li>
                <li>Notify you via email or through a prominent notice on the Service.</li>
                <li>Where required by law, obtain your consent before applying changes.</li>
              </ul>
              <p>
                Your continued use of the Service after any changes to this policy constitutes acceptance of the updated terms.
              </p>
            </div>
          </section>

          {/* Section 11 - Contact */}
          <section className="terms-section animate-slide-up">
            <div className="terms-section-header">
              <span className="terms-section-number">11</span>
              <h2>Contact Us</h2>
            </div>
            <div className="terms-section-body">
              <p>
                If you have any questions, concerns, or requests regarding this Privacy Policy or our data practices, 
                please contact us:
              </p>
              <div className="terms-contact-card">
                <div className="terms-contact-row">
                  <span className="terms-contact-label">Company</span>
                  <span className="terms-contact-value">Adjunct (Reelzy)</span>
                </div>
                <div className="terms-contact-row">
                  <span className="terms-contact-label">Email</span>
                  <span className="terms-contact-value">
                    <a href="mailto:privacy@adjunct.in" style={{ color: 'var(--primary)', textDecoration: 'none' }}>
                      privacy@adjunct.in
                    </a>
                  </span>
                </div>
                <div className="terms-contact-row">
                  <span className="terms-contact-label">Website</span>
                  <span className="terms-contact-value">
                    <a href="https://adjunct.in" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--primary)', textDecoration: 'none' }}>
                      adjunct.in
                    </a>
                  </span>
                </div>
                <div className="terms-contact-row">
                  <span className="terms-contact-label">Data Requests</span>
                  <span className="terms-contact-value">
                    <a href="mailto:data@adjunct.in" style={{ color: 'var(--primary)', textDecoration: 'none' }}>
                      data@adjunct.in
                    </a>
                  </span>
                </div>
              </div>
            </div>
          </section>

        </div>
      </main>

      {/* Footer */}
      <footer style={{ padding: '40px 20px', borderTop: '1px solid var(--border-color)', backgroundColor: 'var(--bg-main)' }}>
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
            <Link to="/pricing" style={{ color: 'inherit', textDecoration: 'none' }}>Pricing</Link>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default PrivacyPolicy;
