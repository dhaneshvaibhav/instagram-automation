import React, { useEffect, useState } from 'react';
import api from '../api';
import { X, Video } from 'lucide-react';

const MediaGallery = ({ onClose, onSelect }) => {
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
    if (onSelect) {
      onSelect(item.id);
      onClose();
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="header" style={{ marginBottom: 'var(--spacing-md)', paddingBottom: 'var(--spacing-sm)' }}>
          <h2 style={{ fontSize: '1.25rem' }}>My Instagram Media</h2>
          <button className="btn btn-ghost btn-small" onClick={onClose}>
            <X size={20} />
          </button>
        </div>
        
        <div className="media-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: 'var(--spacing-md)' }}>
          {loading ? (
            <div style={{ gridColumn: '1/-1', textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>Loading your media...</div>
          ) : media.length === 0 ? (
            <div style={{ gridColumn: '1/-1', textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>No media found.</div>
          ) : (
            media.map(item => (
              <div 
                key={item.id} 
                className="media-item" 
                onClick={() => handleSelect(item)}
                style={{ 
                  border: '1px solid var(--border-color)', 
                  borderRadius: 'var(--radius-md)', 
                  overflow: 'hidden', 
                  cursor: 'pointer', 
                  position: 'relative',
                  transition: 'transform 0.2s',
                  backgroundColor: 'var(--bg-subtle)'
                }}
                onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-4px)'; e.currentTarget.style.borderColor = 'var(--primary)'; }}
                onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.borderColor = 'var(--border-color)'; }}
              >
                {item.media_type === 'IMAGE' || item.thumbnail_url ? (
                  <img 
                    src={item.thumbnail_url || item.media_url} 
                    alt="Thumbnail" 
                    style={{ width: '100%', aspectRatio: '1', objectFit: 'cover' }}
                  />
                ) : (
                  <div style={{ width: '100%', aspectRatio: '1', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#e2e8f0' }}>
                    <Video size={32} color="#94a3b8" />
                  </div>
                )}
                <div style={{ position: 'absolute', top: '8px', right: '8px', background: 'rgba(0,0,0,0.6)', color: 'white', padding: '2px 6px', borderRadius: '4px', fontSize: '0.65rem', textTransform: 'uppercase' }}>
                  {item.media_type}
                </div>
                <div style={{ padding: '8px' }}>
                  <div style={{ 
                    display: '-webkit-box', 
                    WebkitLineClamp: 2, 
                    WebkitBoxOrient: 'vertical', 
                    overflow: 'hidden', 
                    fontSize: '0.8rem', 
                    height: '2.4em', 
                    lineHeight: '1.2',
                    marginBottom: '4px'
                  }}>
                    {item.caption || 'No Caption'}
                  </div>
                  <div className="text-xs text-muted">ID: {item.id}</div>
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
