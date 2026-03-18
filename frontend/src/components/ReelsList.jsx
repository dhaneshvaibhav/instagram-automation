import React, { useEffect, useState } from 'react';
import api from '../api';
import { Trash2, Send, MessageSquare, Mail, Bot, Info } from 'lucide-react';

const ReelsList = ({ refreshTrigger, mode = 'dm' }) => {
  const [reels, setReels] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchReels = async () => {
    try {
      const response = await api.get('/api/reels');
      setReels(response.data.reels || []);
    } catch (error) {
      console.error('Error fetching reels:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReels();
  }, [refreshTrigger]);

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to stop tracking this reel?')) return;
    try {
      await api.delete(`/api/reels/${id}`);
      fetchReels();
    } catch (error) {
      console.error('Error deleting reel:', error);
    }
  };

  const handleTest = async (id) => {
    try {
      await api.post('/api/reels/test-dm', {
        user_id: 'me',
        media_id: id
      });
      alert('Test DM triggered! Check your activity logs for success/failure.');
    } catch (error) {
      console.error('Error sending test DM:', error);
      alert('Failed to send test DM. See console for details.');
    }
  };

  if (loading) return <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>Loading reels...</div>;

  if (reels.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)', backgroundColor: 'var(--bg-subtle)', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border-color)' }}>
        <p>No reels yet. Add one to get started.</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'grid', gap: 'var(--spacing-md)' }}>
      {reels.map((reel) => (
        <div key={reel.id} className="reel-card" style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span className="badge badge-neutral" style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>ID: {reel.id}</span>
              {reel.keyword && (
                <span className="badge badge-info">Trigger: {reel.keyword}</span>
              )}
              {mode === 'reply' && reel.ai_enabled && (
                <span className="badge badge-success" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                  <Bot size={12} /> AI Enabled
                </span>
              )}
            </div>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button className="btn btn-secondary btn-small" onClick={() => handleTest(reel.id)} title="Send Test DM">
                <Send size={14} />
              </button>
              <button className="btn btn-danger btn-small" onClick={() => handleDelete(reel.id)} title="Stop Tracking">
                <Trash2 size={14} />
              </button>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '15px' }}>
            {mode === 'dm' && (
              <div style={{ backgroundColor: 'rgba(var(--primary-rgb), 0.05)', padding: '12px', borderRadius: '8px', borderLeft: '3px solid var(--primary)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px', fontWeight: 600, fontSize: '0.85rem', color: 'var(--primary)' }}>
                  <Mail size={14} /> Private DM {reel.ai_enabled && '(Fallback)'}
                </div>
                <div style={{ fontSize: '0.9rem', color: 'var(--text)' }}>{reel.dm_message || 'No DM set'}</div>
              </div>
            )}
            
            {mode === 'reply' && (
              <div style={{ backgroundColor: 'rgba(var(--success-rgb), 0.05)', padding: '12px', borderRadius: '8px', borderLeft: '3px solid var(--success)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px', fontWeight: 600, fontSize: '0.85rem', color: 'var(--success)' }}>
                  <MessageSquare size={14} /> Public Reply {reel.ai_enabled && '(Fallback)'}
                </div>
                <div style={{ fontSize: '0.9rem', color: 'var(--text)' }}>{reel.public_reply || 'No public reply set'}</div>
              </div>
            )}
          </div>

          {mode === 'reply' && reel.ai_enabled && reel.ai_context && (
            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '6px', fontStyle: 'italic', padding: '0 5px' }}>
              <Info size={14} /> AI Context: {reel.ai_context}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default ReelsList;
