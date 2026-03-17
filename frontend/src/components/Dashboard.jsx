import React, { useEffect, useState } from 'react';
import api from '../api';
import { RefreshCw, Power } from 'lucide-react';
import Stats from './Stats';
import ReelsList from './ReelsList';
import AddReelForm from './AddReelForm';
import LogViewer from './LogViewer';
import MediaGallery from './MediaGallery';

const Dashboard = ({ user, onLogout }) => {
  const [showMediaGallery, setShowMediaGallery] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleRefresh = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  const handleRefreshToken = async () => {
    try {
      await api.get('/auth/refresh-token');
      window.location.reload();
    } catch (error) {
      console.error('Failed to refresh token', error);
      alert('Failed to refresh token');
    }
  };

  // Calculate days left
  const daysLeft = user.days_left || 0;
  const showWarning = daysLeft < 10;

  return (
    <div className="container">
      {/* Header */}
      <div className="header">
        <h1>Reel DM Bot</h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span className="badge">● Connected</span>
          {user.expires_at && (
            <span style={{ fontSize: '12px', color: '#666666' }}>
               Expires in {daysLeft} days
            </span>
          )}
          <button className="disconnect-link" onClick={onLogout}>
            Disconnect
          </button>
        </div>
      </div>

      {/* Warning Banner */}
      {showWarning && (
        <div className="warning-banner">
          <span className="warning-text">
            Your token expires in {daysLeft} day{daysLeft !== 1 ? 's' : ''}. Refresh now
          </span>
          <button className="btn btn-primary btn-small" onClick={handleRefreshToken}>
            Refresh Token
          </button>
        </div>
      )}

      {/* Stats Row */}
      <Stats user={user} refreshTrigger={refreshTrigger} />

      {/* Reel Messages Section */}
      <div className="section-header">
        <h2 className="section-title">Reel Messages</h2>
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
        <MediaGallery onClose={() => setShowMediaGallery(false)} />
      )}

      {/* Reels List */}
      <ReelsList refreshTrigger={refreshTrigger} />

      {/* Add New Reel Form */}
      <div id="addReelForm" className="form-section">
        <h3 className="section-title" style={{ marginBottom: '20px' }}>Add New Reel</h3>
        <AddReelForm onReelAdded={handleRefresh} />
      </div>

      {/* Live Logs Section */}
      <LogViewer />
    </div>
  );
};

export default Dashboard;
