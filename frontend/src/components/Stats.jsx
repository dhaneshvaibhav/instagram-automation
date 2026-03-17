import React, { useEffect, useState } from 'react';
import api from '../api';

const Stats = ({ user, refreshTrigger }) => {
  const [stats, setStats] = useState({ dms_sent_today: 0 });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get('/api/stats');
        setStats(response.data);
      } catch (error) {
        console.error('Error fetching stats:', error);
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, 30000);
    return () => clearInterval(interval);
  }, [refreshTrigger]);

  return (
    <div className="stats-row">
      <div className="stat-card" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        {user.profile_picture_url && (
          <img 
            src={user.profile_picture_url} 
            alt="Profile" 
            style={{ width: '60px', height: '60px', borderRadius: '50%', objectFit: 'cover' }} 
          />
        )}
        <div style={{ flex: 1 }}>
          <div className="stat-label">Connected Account</div>
          <div className="stat-value" style={{ fontSize: '18px' }}>@{user.username || 'unknown'}</div>
          <div style={{ fontSize: '13px', color: '#555', marginTop: '2px' }}>Name: {user.name}</div>
          <div style={{ fontSize: '11px', color: '#888', marginTop: '4px' }}>ID: {user.ig_account_id}</div>
        </div>
      </div>
      
      <div className="stat-card">
        <div className="stat-label">DMs Sent Today</div>
        <div className="stat-value">{stats.dms_sent_today}</div>
        <div style={{ fontSize: '11px', color: '#888', marginTop: '4px' }}>Tracked across all reels</div>
      </div>

      <div className="stat-card">
        <div className="stat-label">Profile Stats</div>
        <div style={{ display: 'flex', gap: '24px', marginTop: '8px' }}>
          <div>
            <div className="stat-value" style={{ fontSize: '20px' }}>{user.followers_count?.toLocaleString() || 0}</div>
            <div style={{ fontSize: '11px', color: '#888', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Followers</div>
          </div>
          <div>
            <div className="stat-value" style={{ fontSize: '20px' }}>{user.follows_count?.toLocaleString() || 0}</div>
            <div style={{ fontSize: '11px', color: '#888', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Following</div>
          </div>
          <div>
            <div className="stat-value" style={{ fontSize: '20px' }}>{user.media_count?.toLocaleString() || 0}</div>
            <div style={{ fontSize: '11px', color: '#888', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Posts</div>
          </div>
        </div>
        <div style={{ fontSize: '11px', color: '#888', marginTop: '8px', fontWeight: 500 }}>
          Account: {user.account_type || 'Professional'}
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-label">Connection Expiry</div>
        <div className="stat-value" style={{ fontSize: '18px', color: (user.days_left || 0) < 1 ? '#d32f2f' : '#2e7d32' }}>
          {(user.days_left || 0) < 1 ? 'Expired' : `${user.days_left}d left`}
        </div>
        <div style={{ fontSize: '11px', color: '#888', marginTop: '4px' }}>
          Date: {user.expires_at ? new Date(user.expires_at).toLocaleTimeString() : 'N/A'}
        </div>
      </div>
    </div>
  );
};

export default Stats;
