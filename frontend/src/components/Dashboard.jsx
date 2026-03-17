import React, { useEffect, useState } from 'react';
import api from '../api';
import Stats from './Stats';
import ReelsList from './ReelsList';
import AddReelForm from './AddReelForm';
import LogViewer from './LogViewer';
import MediaGallery from './MediaGallery';
import { Instagram, Zap } from 'lucide-react';

const Dashboard = ({ user, onLogout }) => {
  const [showMediaGallery, setShowMediaGallery] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [selectedReelId, setSelectedReelId] = useState('');
  const [notification, setNotification] = useState(null);

  const showToast = (message, type = 'success') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  const handleRefresh = () => {
    setRefreshTrigger(prev => prev + 1);
    showToast('Dashboard updated');
  };

  const handleRefreshToken = async () => {
    try {
      await api.get('/auth/refresh-token');
      showToast('Token refreshed! Reloading...');
      setTimeout(() => window.location.reload(), 1000);
    } catch (error) {
      console.error('Failed to refresh token', error);
      showToast('Failed to refresh token', 'danger');
    }
  };

  const handleMediaSelect = (id) => {
    setSelectedReelId(id);
    document.getElementById('addReelForm').scrollIntoView({ behavior: 'smooth' });
    showToast(`Selected Reel: ${id}`);
  };

  // Calculate days left
  const daysLeft = user.days_left || 0;
  const showWarning = daysLeft < 10;

  return (
    <div className="container">
      {/* Header */}
      <div className="header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Zap size={32} fill="var(--primary)" color="var(--primary)" />
          <h1 className="header-title" style={{ margin: 0 }}>Reelzy</h1>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span className="badge badge-success">● Connected</span>
          {user.expires_at && (
            <span className="text-small text-muted">
               Expires in {daysLeft} days
            </span>
          )}
          <button className="btn btn-ghost btn-small" onClick={onLogout}>
            Disconnect
          </button>
        </div>
      </div>

      {/* Warning Banner */}
      {showWarning && (
        <div className="card" style={{ backgroundColor: 'var(--warning-bg)', borderColor: 'var(--warning)', marginBottom: 'var(--spacing-lg)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ color: 'var(--warning)', fontWeight: 500 }}>
            Your token expires in {daysLeft} day{daysLeft !== 1 ? 's' : ''}. Refresh now
          </span>
          <button className="btn btn-primary btn-small" onClick={handleRefreshToken}>
            Refresh Token
          </button>
        </div>
      )}

      {/* Stats Row */}
      <Stats user={user} refreshTrigger={refreshTrigger} />

      {/* Toast Notification */}
      {notification && (
        <div style={{
          position: 'fixed', bottom: '24px', right: '24px', zIndex: 100,
          animation: 'modalSlideIn 0.3s ease'
        }}>
          <div className={`badge badge-${notification.type}`} style={{ padding: '12px 20px', boxShadow: 'var(--shadow-lg)', fontSize: '0.9rem' }}>
            {notification.message}
          </div>
        </div>
      )}

      {/* Reel Messages Section */}
      <div className="header" style={{ marginBottom: 'var(--spacing-md)', paddingBottom: 'var(--spacing-md)', borderBottom: 'none' }}>
        <h2 style={{ fontSize: '1.25rem' }}>Reel Messages</h2>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button 
            className="btn btn-secondary btn-small" 
            onClick={() => setShowMediaGallery(true)}
          >
            View My Media
          </button>
          <button 
            className="btn btn-primary btn-small"
            onClick={() => document.getElementById('addReelForm').scrollIntoView({ behavior: 'smooth' })}
          >
            + Add reel
          </button>
        </div>
      </div>

      {/* Media Gallery Modal */}
      {showMediaGallery && (
        <MediaGallery 
          onClose={() => setShowMediaGallery(false)} 
          onSelect={handleMediaSelect}
        />
      )}

      {/* Reels List */}
      <ReelsList refreshTrigger={refreshTrigger} />

      {/* Add New Reel Form */}
      <div id="addReelForm" className="card" style={{ marginTop: 'var(--spacing-xl)' }}>
        <h3 style={{ marginBottom: 'var(--spacing-md)', fontSize: '1.1rem' }}>Add New Reel</h3>
        <AddReelForm 
          onReelAdded={handleRefresh} 
          externalReelId={selectedReelId}
        />
      </div>

      {/* Live Logs Section */}
      <LogViewer />
    </div>
  );
};

export default Dashboard;
