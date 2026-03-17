import React, { useEffect, useState } from 'react';
import api from '../api';
import { Trash2, Send } from 'lucide-react';

const ReelsList = ({ refreshTrigger }) => {
  const [reels, setReels] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchReels = async () => {
    try {
      const response = await api.get('/api/reels');
      // Backend returns { reels: [...] }
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

  if (loading) return <div className="empty-state">Loading reels...</div>;

  if (reels.length === 0) {
    return (
      <div className="reels-container">
        <div className="empty-state">
          <p>No reels yet. Add one to get started.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="reels-container">
      {reels.map((reel) => (
        <div key={reel.id} className="reel-card">
          <div className="reel-content">
            <span className="reel-id">ID: {reel.id}</span>
            <div className="reel-message">{reel.message}</div>
            <div className="reel-meta">
              {reel.keyword && (
                <span className="keyword-badge">Keyword: {reel.keyword}</span>
              )}
            </div>
          </div>
          <div className="reel-actions">
            <button className="btn-test" onClick={() => handleTest(reel.id)} title="Send Test DM">
              <Send size={16} /> Test
            </button>
            <button className="btn-delete" onClick={() => handleDelete(reel.id)} title="Stop Tracking">
              <Trash2 size={16} /> Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ReelsList;
