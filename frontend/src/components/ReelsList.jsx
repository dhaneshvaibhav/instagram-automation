import React, { useEffect, useState } from 'react';
import api from '../api';
import { Trash2, Send } from 'lucide-react';

const ReelsList = ({ refreshTrigger }) => {
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
      alert('Failed to delete reel');
    }
  };

  const handleTest = async (id) => {
    try {
      await api.post(`/api/reels/${id}/test`);
      alert('Test DM sent! Check your logs.');
    } catch (error) {
      console.error('Error sending test DM:', error);
      alert('Failed to send test DM');
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
        <div key={reel.id} className="reel-card" style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div>
              <span className="badge badge-neutral" style={{ fontFamily: 'monospace' }}>{reel.id}</span>
            </div>
            <div style={{ fontSize: '0.95rem', lineHeight: '1.4', maxWidth: '600px' }}>{reel.message}</div>
            <div>
              {reel.keyword && (
                <span className="badge badge-info">Keyword: {reel.keyword}</span>
              )}
            </div>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button className="btn btn-secondary btn-small" onClick={() => handleTest(reel.id)} title="Send Test DM">
              <Send size={14} style={{ marginRight: '4px' }} /> Test
            </button>
            <button className="btn btn-danger btn-small" onClick={() => handleDelete(reel.id)} title="Stop Tracking">
              <Trash2 size={14} style={{ marginRight: '4px' }} /> Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ReelsList;
