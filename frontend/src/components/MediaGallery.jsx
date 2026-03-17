import React, { useEffect, useState } from 'react';
import api from '../api';
import { X, Image, Video } from 'lucide-react';

const MediaGallery = ({ onClose }) => {
  const [media, setMedia] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMedia = async () => {
      try {
        const response = await api.get('/api/reels/instagram');
        setMedia(response.data.reels || []);
      } catch (error) {
        console.error('Error fetching media:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchMedia();
  }, []);

  const handleSelect = (item) => {
    // Populate form if it exists
    const reelIdInput = document.getElementById('reelId');
    if (reelIdInput) {
      // React specific way to trigger change event on external components is tricky
      // Better to use a context or callback, but for now we'll just close and let user copy ID
      // Or better: dispatch a custom event or just alert the ID
      alert(`Selected ID: ${item.id}. Please paste this into the Reel ID field.`);
      onClose();
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="section-title">My Instagram Media</h2>
          <button className="btn btn-secondary" onClick={onClose}>
            <X size={16} /> Close
          </button>
        </div>
        
        <div className="media-grid">
          {loading ? (
            <div className="empty-state">Loading your media...</div>
          ) : media.length === 0 ? (
            <div className="empty-state">No media found.</div>
          ) : (
            media.map(item => (
              <div key={item.id} className="media-item" onClick={() => handleSelect(item)}>
                {item.media_type === 'IMAGE' || item.thumbnail_url ? (
                  <img 
                    src={item.thumbnail_url || item.media_url} 
                    alt="Thumbnail" 
                    className="media-thumb" 
                  />
                ) : (
                  <div className="media-thumb" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Video size={32} color="#ccc" />
                  </div>
                )}
                <div className="media-type-icon">{item.media_type}</div>
                <div className="media-info">
                  <div className="media-caption">{item.caption || 'No Caption'}</div>
                  <div style={{ marginTop: '4px', color: '#888' }}>ID: {item.id}</div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default MediaGallery;
