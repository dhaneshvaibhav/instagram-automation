import React from 'react';
import { Link } from 'react-router-dom';
import { Zap, ArrowLeft, FileText, Scale, Shield, AlertTriangle, BarChart3, MessageSquare, CheckCircle2, ArrowDown } from 'lucide-react';

const TermsAndConditions = () => {
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

      {/* Hero Header */}
      <header className="terms-header">
        <div className="container" style={{ maxWidth: '860px' }}>
          <div className="animate-fade-in" style={{ textAlign: 'center' }}>
            <div style={{
              width: '72px', height: '72px', borderRadius: '18px',
              background: 'linear-gradient(135deg, var(--info-bg), var(--success-bg))',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              margin: '0 auto 24px', border: '1px solid var(--border-color)'
            }}>
              <Scale size={32} color="var(--primary)" />
            </div>
            <h1 style={{
              fontFamily: 'var(--font-heading)', fontSize: '2.75rem',
              color: 'var(--text-main)', marginBottom: '16px', letterSpacing: '-0.02em'
            }}>
              Terms & Conditions
            </h1>
            <p className="text-muted" style={{ fontSize: '1.05rem', marginBottom: '20px', lineHeight: 1.6 }}>
              Please read these terms carefully before using the Reelzy platform.
            </p>
            <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}>
              <span className="badge badge-info">Effective: March 22, 2026</span>
              <span className="badge badge-neutral">Last Updated: March 22, 2026</span>
            </div>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="terms-content">
        <div className="container" style={{ maxWidth: '860px' }}>

          {/* Important Notice */}
          <div className="terms-notice animate-slide-up">
            <AlertTriangle size={20} color="var(--warning)" style={{ flexShrink: 0, marginTop: '2px' }} />
            <div>
              <strong style={{ fontSize: '0.95rem' }}>Important Notice</strong>
              <p style={{ margin: '4px 0 0', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                By accessing or using Reelzy, you agree to be bound by these Terms and Conditions. If you do not agree with any part of these terms, you must not use our service.
              </p>
            </div>
          </div>

          {/* Section 1 */}
          <section className="terms-section animate-slide-up delay-1">
            <div className="terms-section-header">
              <span className="terms-section-number">01</span>
              <h2>Acceptance of Terms</h2>
            </div>
            <div className="terms-section-body">
              <p>
                These Terms and Conditions ("Terms") govern your access to and use of the Reelzy platform ("Service"), 
                a product of Adjunct ("Company", "we", "our", or "us"). By creating an account or using any part of 
                the Service, you acknowledge that you have read, understood, and agree to be bound by these Terms.
              </p>
              <p>
                We reserve the right to update or modify these Terms at any time without prior notice. Your continued 
                use of the Service after any changes constitutes acceptance of the modified Terms. We will make 
                reasonable efforts to notify users of significant changes via email or in-app notifications.
              </p>
            </div>
          </section>

          {/* Section 2 */}
          <section className="terms-section animate-slide-up delay-1">
            <div className="terms-section-header">
              <span className="terms-section-number">02</span>
              <h2>Description of Service</h2>
            </div>
            <div className="terms-section-body">
              <p>
                Reelzy is an Instagram automation and engagement platform that enables creators and businesses to:
              </p>
              <ul className="terms-list">
                <li><strong>Automated DM Responses:</strong> Automatically send direct messages to users who comment on your Instagram Reels based on configurable keyword triggers.</li>
                <li><strong>Comment Monitoring:</strong> Real-time monitoring and filtering of comments across your published Reels.</li>
                <li><strong>Analytics & Reporting:</strong> Track engagement metrics, DM delivery statistics, and conversion performance data.</li>
                <li><strong>Media Management:</strong> Browse and manage your published Instagram media library within the platform.</li>
              </ul>
              <p>
                The Service operates through the official Meta Graph API and Instagram Graph API, and all functionalities 
                are subject to the availability and terms of these underlying platform APIs.
              </p>
            </div>
          </section>

          {/* Section 3 - How Reelzy Works (Workflow) */}
          <section className="terms-section animate-slide-up delay-2">
            <div className="terms-section-header">
              <span className="terms-section-number">03</span>
              <h2>How Reelzy Works</h2>
            </div>
            <div className="terms-section-body">
              <p>
                The following outlines the operational workflow of the Reelzy platform. By using the Service, 
                you agree to each step of this process and acknowledge how your data and Instagram account 
                are utilized at every stage.
              </p>

              <div className="terms-workflow">
                {/* Step 1 */}
                <div className="terms-workflow-step">
                  <div className="terms-workflow-icon" style={{ background: 'var(--info-bg)' }}>
                    <Zap size={22} color="var(--info)" />
                  </div>
                  <div className="terms-workflow-body">
                    <div className="terms-workflow-step-label">STEP 01</div>
                    <h3>Connect Your Account</h3>
                    <p>
                      You authorize Reelzy via Meta's secure OAuth 2.0 portal. We request only the permissions 
                      necessary to operate the Service — including <strong>instagram_basic</strong>, <strong>instagram_manage_comments</strong>, 
                      <strong>instagram_manage_messages</strong>, and <strong>pages_messaging</strong>. Your Instagram password is 
                      never stored or accessed by Reelzy.
                    </p>
                  </div>
                </div>

                <div className="terms-workflow-arrow">
                  <ArrowDown size={18} color="var(--text-muted)" />
                </div>

                {/* Step 2 */}
                <div className="terms-workflow-step">
                  <div className="terms-workflow-icon" style={{ background: 'var(--success-bg)' }}>
                    <BarChart3 size={22} color="var(--success)" />
                  </div>
                  <div className="terms-workflow-body">
                    <div className="terms-workflow-step-label">STEP 02</div>
                    <h3>Analyze & Sync Media</h3>
                    <p>
                      Reelzy fetches your published Instagram Reels and associated engagement data 
                      (likes, comments, reach) through the Instagram Graph API. This data is used solely to 
                      power your analytics dashboard and enable comment-based automation triggers. Data is 
                      refreshed periodically and is not shared with third parties.
                    </p>
                  </div>
                </div>

                <div className="terms-workflow-arrow">
                  <ArrowDown size={18} color="var(--text-muted)" />
                </div>

                {/* Step 3 */}
                <div className="terms-workflow-step">
                  <div className="terms-workflow-icon" style={{ background: 'var(--warning-bg)' }}>
                    <MessageSquare size={22} color="var(--warning)" />
                  </div>
                  <div className="terms-workflow-body">
                    <div className="terms-workflow-step-label">STEP 03</div>
                    <h3>Configure Automation Rules</h3>
                    <p>
                      You define trigger keywords (e.g., "price", "link", "info") and craft the DM response 
                      message. When a user comments on one of your Reels with a matching keyword, Reelzy 
                      automatically sends the configured DM on your behalf. You are solely responsible for the 
                      content of these automated messages and must ensure compliance with Instagram's Community 
                      Guidelines and applicable laws.
                    </p>
                  </div>
                </div>

                <div className="terms-workflow-arrow">
                  <ArrowDown size={18} color="var(--text-muted)" />
                </div>

                {/* Step 4 */}
                <div className="terms-workflow-step">
                  <div className="terms-workflow-icon" style={{ background: 'linear-gradient(135deg, var(--info-bg), var(--success-bg))' }}>
                    <CheckCircle2 size={22} color="var(--primary)" />
                  </div>
                  <div className="terms-workflow-body">
                    <div className="terms-workflow-step-label">STEP 04</div>
                    <h3>Automate & Monitor</h3>
                    <p>
                      Once activated, the automation engine runs continuously. You can monitor delivery 
                      logs, track DM success rates, and review engagement analytics through the dashboard in 
                      real-time. You may pause or deactivate automation at any time. Reelzy operates within 
                      Meta's API rate limits and will not exceed the permitted volume of messages.
                    </p>
                  </div>
                </div>
              </div>

              <div className="terms-callout" style={{ marginTop: '24px' }}>
                <Shield size={18} color="var(--primary)" style={{ flexShrink: 0, marginTop: '2px' }} />
                <div>
                  <strong>Your Control</strong>
                  <p style={{ margin: '4px 0 0', fontSize: '0.875rem' }}>
                    You retain full control over the automation at all times. You can modify keywords, update DM 
                    content, pause automation for specific Reels, or disconnect your account entirely — all without 
                    contacting support.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Section 4 */}
          <section className="terms-section animate-slide-up delay-2">
            <div className="terms-section-header">
              <span className="terms-section-number">04</span>
              <h2>Account Requirements</h2>
            </div>
            <div className="terms-section-body">
              <p>To use the Service, you must:</p>
              <ul className="terms-list">
                <li>Be at least 18 years of age or the legal age of majority in your jurisdiction.</li>
                <li>Have a valid Instagram Business or Creator account connected to a Facebook Page.</li>
                <li>Authorize Reelzy to access your Instagram account via Meta's official OAuth 2.0 authentication flow.</li>
                <li>Provide accurate and complete information during the account creation process.</li>
              </ul>
              <p>
                You are solely responsible for maintaining the confidentiality of your account credentials and for 
                all activities that occur under your account. You must notify us immediately of any unauthorized 
                use of your account.
              </p>
            </div>
          </section>

          {/* Section 5 */}
          <section className="terms-section animate-slide-up delay-2">
            <div className="terms-section-header">
              <span className="terms-section-number">05</span>
              <h2>Acceptable Use Policy</h2>
            </div>
            <div className="terms-section-body">
              <p>When using Reelzy, you agree <strong>not</strong> to:</p>
              <ul className="terms-list terms-list-prohibited">
                <li>Use the Service to send spam, unsolicited promotions, or misleading content via automated DMs.</li>
                <li>Engage in any activity that violates Instagram's Community Guidelines, Terms of Use, or Platform Policy.</li>
                <li>Attempt to circumvent rate limits, API restrictions, or any security measures implemented by Meta or Reelzy.</li>
                <li>Use the Service for illegal activities, harassment, defamation, or any content that infringes upon the rights of others.</li>
                <li>Reverse-engineer, decompile, or attempt to extract the source code of the Service.</li>
                <li>Share, sell, or transfer your account access to any third party without written consent.</li>
              </ul>
              <p>
                Violation of this Acceptable Use Policy may result in immediate suspension or termination of your 
                account without prior notice or refund.
              </p>
            </div>
          </section>

          {/* Section 6 */}
          <section className="terms-section animate-slide-up delay-3">
            <div className="terms-section-header">
              <span className="terms-section-number">06</span>
              <h2>Instagram & Meta Compliance</h2>
            </div>
            <div className="terms-section-body">
              <div className="terms-callout">
                <Shield size={18} color="var(--primary)" style={{ flexShrink: 0, marginTop: '2px' }} />
                <div>
                  <strong>Official API Integration</strong>
                  <p style={{ margin: '4px 0 0', fontSize: '0.875rem' }}>
                    Reelzy exclusively uses the official Meta Graph API and Instagram Graph API. We do not use 
                    unofficial methods, browser automation, or data scraping of any kind.
                  </p>
                </div>
              </div>
              <p>
                By using Reelzy, you acknowledge that:
              </p>
              <ul className="terms-list">
                <li>Reelzy is not affiliated with, endorsed by, or sponsored by Meta Platforms, Inc. or Instagram.</li>
                <li>Your use of the Service is also governed by Meta's Platform Terms and Instagram's Terms of Use.</li>
                <li>Meta may revoke API access or change API capabilities at any time, which may affect the availability or functionality of the Service.</li>
                <li>You are responsible for ensuring that your automated messages comply with all applicable Instagram guidelines.</li>
              </ul>
            </div>
          </section>

          {/* Section 7 */}
          <section className="terms-section animate-slide-up delay-3">
            <div className="terms-section-header">
              <span className="terms-section-number">07</span>
              <h2>Intellectual Property</h2>
            </div>
            <div className="terms-section-body">
              <p>
                All intellectual property rights in the Service, including but not limited to the software, design, 
                logos, trademarks, and documentation, are owned by Adjunct or its licensors. These Terms do not 
                grant you any right, title, or interest in the Service except for the limited right to use it in 
                accordance with these Terms.
              </p>
              <p>
                You retain all ownership rights to the content you create, upload, or transmit through the Service. 
                By using the Service, you grant Adjunct a non-exclusive, worldwide, royalty-free license to use 
                your content solely for the purpose of operating and improving the Service.
              </p>
            </div>
          </section>

          {/* Section 8 */}
          <section className="terms-section animate-slide-up">
            <div className="terms-section-header">
              <span className="terms-section-number">08</span>
              <h2>Limitation of Liability</h2>
            </div>
            <div className="terms-section-body">
              <p>
                To the maximum extent permitted by applicable law, Adjunct and its officers, directors, employees, 
                and agents shall not be liable for any indirect, incidental, special, consequential, or punitive 
                damages arising from or related to your use of the Service, including but not limited to:
              </p>
              <ul className="terms-list">
                <li>Loss of profits, revenue, data, or business opportunities.</li>
                <li>Account suspension or restrictions imposed by Instagram or Meta.</li>
                <li>Service interruptions, API downtime, or connectivity issues.</li>
                <li>Actions taken by recipients of automated messages sent through the Service.</li>
              </ul>
              <p>
                The Service is provided on an "AS IS" and "AS AVAILABLE" basis without warranties of any kind, 
                either express or implied. We do not guarantee uninterrupted or error-free service.
              </p>
            </div>
          </section>

          {/* Section 9 */}
          <section className="terms-section animate-slide-up">
            <div className="terms-section-header">
              <span className="terms-section-number">09</span>
              <h2>Termination</h2>
            </div>
            <div className="terms-section-body">
              <p>
                You may terminate your account at any time by disconnecting your Instagram account from the Service 
                and ceasing all use. We may suspend or terminate your access to the Service at our sole discretion 
                if we believe you have violated these Terms or if required by law.
              </p>
              <p>
                Upon termination, all licenses and rights granted to you under these Terms will immediately cease. 
                We may retain certain data as required by law or for legitimate business purposes. Sections relating 
                to Intellectual Property, Limitation of Liability, and Governing Law shall survive termination.
              </p>
            </div>
          </section>

          {/* Section 10 */}
          <section className="terms-section animate-slide-up">
            <div className="terms-section-header">
              <span className="terms-section-number">10</span>
              <h2>Privacy & Data Protection</h2>
            </div>
            <div className="terms-section-body">
              <p>
                Your privacy is important to us. Our collection and use of personal information is governed by our 
                Privacy Policy. By using the Service, you consent to the collection and use of your data as 
                described therein.
              </p>
              <p>
                We access your Instagram data only through officially authorized API permissions that you explicitly 
                grant during the OAuth authentication flow. We do not store your Instagram password, and you can 
                revoke access at any time through your Meta account settings.
              </p>
            </div>
          </section>

          {/* Section 11 */}
          <section className="terms-section animate-slide-up">
            <div className="terms-section-header">
              <span className="terms-section-number">11</span>
              <h2>Governing Law & Dispute Resolution</h2>
            </div>
            <div className="terms-section-body">
              <p>
                These Terms shall be governed by and construed in accordance with the laws of India, 
                without regard to the principles of conflicts of law. Any disputes arising from these Terms or the 
                use of the Service shall be subject to the exclusive jurisdiction of the courts located in India.
              </p>
              <p>
                Before filing any formal legal proceedings, you agree to first attempt to resolve any dispute 
                informally by contacting us. We will make reasonable efforts to resolve disputes within 30 business 
                days of receiving notice.
              </p>
            </div>
          </section>

          {/* Section 12 */}
          <section className="terms-section animate-slide-up">
            <div className="terms-section-header">
              <span className="terms-section-number">12</span>
              <h2>Contact Information</h2>
            </div>
            <div className="terms-section-body">
              <p>
                If you have any questions, concerns, or requests regarding these Terms and Conditions, 
                please contact us:
              </p>
              <div className="terms-contact-card">
                <div className="terms-contact-row">
                  <span className="terms-contact-label">Company</span>
                  <span>Adjunct</span>
                </div>
                <div className="terms-contact-row">
                  <span className="terms-contact-label">Website</span>
                  <a href="https://adjunct.in" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--primary)', textDecoration: 'underline' }}>adjunct.in</a>
                </div>
                <div className="terms-contact-row">
                  <span className="terms-contact-label">Product</span>
                  <span>Reelzy — Instagram Automation Platform</span>
                </div>
              </div>
            </div>
          </section>

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
            <span style={{ fontWeight: 600, color: 'var(--primary)' }}>Terms</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default TermsAndConditions;
