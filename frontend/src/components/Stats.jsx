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
    <div className="stats-grid">
      <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        {user.profile_picture_url && (
          <img 
            src={user.profile_picture_url} 
            alt="Profile" 
            style={{ width: '60px', height: '60px', borderRadius: '50%', objectFit: 'cover' }} 
          />
        )}
        <div style={{ flex: 1 }}>
          <div className="text-small text-muted" style={{ marginBottom: '4px' }}>Connected Account</div>
          <div style={{ fontSize: '1.1rem', fontWeight: 600 }}>@{user.username || 'unknown'}</div>
          <div className="text-small text-muted">ID: {user.ig_account_id}</div>
        </div>
      </div>
      
      <div className="card">
        <div className="text-small text-muted" style={{ marginBottom: '8px' }}>DMs Sent Today</div>
        <div style={{ fontSize: '1.75rem', fontWeight: 700 }}>{stats.dms_sent_today}</div>
        <div className="text-xs text-muted" style={{ marginTop: '4px' }}>Tracked across all reels</div>
      </div>

      <div className="card">
        <div className="text-small text-muted" style={{ marginBottom: '8px' }}>Profile Stats</div>
        <div style={{ display: 'flex', gap: '24px' }}>
          <div>
            <div style={{ fontSize: '1.25rem', fontWeight: 600 }}>{user.followers_count?.toLocaleString() || 0}</div>
            <div className="text-xs text-muted" style={{ textTransform: 'uppercase', letterSpacing: '0.5px' }}>Followers</div>
          </div>
          <div>
            <div style={{ fontSize: '1.25rem', fontWeight: 600 }}>{user.follows_count?.toLocaleString() || 0}</div>
            <div className="text-xs text-muted" style={{ textTransform: 'uppercase', letterSpacing: '0.5px' }}>Following</div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="text-small text-muted" style={{ marginBottom: '8px' }}>Connection Expiry</div>
        <div style={{ fontSize: '1.25rem', fontWeight: 600, color: (user.days_left || 0) < 1 ? 'var(--danger)' : 'var(--success)' }}>
          {(user.days_left || 0) < 1 ? 'Expired' : `${user.days_left}d left`}
        </div>
        <div className="text-xs text-muted" style={{ marginTop: '4px' }}>
          Date: {user.expires_at ? new Date(user.expires_at).toLocaleTimeString() : 'N/A'}
        </div>
      </div>
    </div>
  );
};

export default Stats;
