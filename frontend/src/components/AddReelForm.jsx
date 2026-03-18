import React, { useState, useEffect } from 'react';
import api from '../api';

const AddReelForm = ({ onReelAdded, externalReelId, mode = 'dm' }) => {
  const [formData, setFormData] = useState({
    reelId: '',
    keyword: '',
    dm_message: '',
    public_reply: '',
    ai_enabled: false,
    ai_context: ''
  });
  const [igReels, setIgReels] = useState([]);
  const [loadingReels, setLoadingReels] = useState(false);

  // Sync external selection from Gallery
  useEffect(() => {
    if (externalReelId) {
      setFormData(prev => ({ ...prev, reelId: externalReelId }));
    }
  }, [externalReelId]);

  useEffect(() => {
    const fetchIgReels = async () => {
      setLoadingReels(true);
      try {
        const response = await api.get('/api/reels/instagram');
        setIgReels(response.data.reels || []);
      } catch (error) {
        console.error('Error fetching IG reels:', error);
      } finally {
        setLoadingReels(false);
      }
    };
    fetchIgReels();
  }, []);

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData({ ...formData, [e.target.id]: value });
  };

  const handleSelectChange = async (e) => {
    const selectedId = e.target.value;
    if (selectedId) {
      setFormData(prev => ({ ...prev, reelId: selectedId }));
      
      // Try to fetch existing automation data for this reel
      try {
        const response = await api.get(`/api/reels/${selectedId}`);
        if (response.data) {
          const { dm_message, public_reply, keyword, ai_enabled, ai_context } = response.data;
          setFormData(prev => ({
            ...prev,
            dm_message: dm_message || '',
            public_reply: public_reply || '',
            keyword: keyword || '',
            ai_enabled: !!ai_enabled,
            ai_context: ai_context || ''
          }));
        }
      } catch (error) {
        // If 404, it's a new reel, which is fine
        if (error.response && error.response.status !== 404) {
          console.error('Error fetching reel data:', error);
        }
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Check if reel already exists to decide between POST and PUT
      let exists = false;
      try {
        await api.get(`/api/reels/${formData.reelId}`);
        exists = true;
      } catch (err) {}

      const payload = {
        reel_id: formData.reelId,
        mode: mode,
        keyword: formData.keyword,
        dm_message: formData.dm_message,
        public_reply: formData.public_reply,
        ai_enabled: formData.ai_enabled,
        ai_context: formData.ai_context
      };

      if (exists) {
        await api.put(`/api/reels/${formData.reelId}`, payload);
      } else {
        await api.post('/api/reels', payload);
      }

      setFormData({ 
        reelId: '', 
        keyword: '', 
        dm_message: '', 
        public_reply: '',
        ai_enabled: false,
        ai_context: ''
      });
      onReelAdded();
    } catch (error) {
      console.error('Error saving reel:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label className="form-label">Select Reel</label>
        <select 
          className="form-select" 
          onChange={handleSelectChange}
          value={formData.reelId}
        >
          <option value="">{loadingReels ? '-- Fetching Reels... --' : '-- Select a Reel to auto-fill --'}</option>
          {igReels.map(reel => (
            <option key={reel.id} value={reel.id}>
              {reel.id} - {reel.caption ? reel.caption.substring(0, 30) + '...' : 'No caption'}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label className="form-label">Reel ID</label>
        <input 
          type="text" 
          className="form-input" 
          id="reelId" 
          value={formData.reelId}
          onChange={handleChange}
          placeholder="e.g. 17841234567890" 
          required 
        />
      </div>

      <div className="form-group">
        <label className="form-label">Keyword (Trigger)</label>
        <input 
          type="text" 
          className="form-input" 
          id="keyword" 
          value={formData.keyword}
          onChange={handleChange}
          placeholder="e.g. info, link, yes"
        />
      </div>

      <hr style={{ margin: '20px 0', border: '0', borderTop: '1px solid var(--border)' }} />
      
      {mode === 'dm' && (
        <div className="form-group">
          <label className="form-label">Private DM Message</label>
          <textarea 
            className="form-input" 
            id="dm_message" 
            value={formData.dm_message}
            onChange={handleChange}
            placeholder="Message to send as a DM..."
            rows="3"
            required
          />
        </div>
      )}

      {mode === 'reply' && (
        <>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '15px' }}>
            <input 
              type="checkbox" 
              id="ai_enabled" 
              checked={formData.ai_enabled}
              onChange={handleChange}
              style={{ width: '18px', height: '18px' }}
            />
            <label htmlFor="ai_enabled" style={{ fontWeight: 600, color: 'var(--primary)' }}>Enable AI Personalization (Gemini)</label>
          </div>

          {formData.ai_enabled && (
            <div className="form-group">
              <label className="form-label">AI Context / Instructions</label>
              <textarea 
                className="form-input" 
                id="ai_context" 
                value={formData.ai_context}
                onChange={handleChange}
                placeholder="Tell AI about your product/service to help it generate better replies..."
                rows="3"
              />
            </div>
          )}

          <div className="form-group">
            <label className="form-label">Public Reply Message {formData.ai_enabled && '(Fallback)'}</label>
            <textarea 
              className="form-input" 
              id="public_reply" 
              value={formData.public_reply}
              onChange={handleChange}
              placeholder="Message to post as a public reply..."
              rows="2"
              required={!formData.ai_enabled}
            />
          </div>
        </>
      )}

      <button type="submit" className="btn btn-primary btn-block" style={{ marginTop: '10px' }}>
        Start {mode === 'dm' ? 'DM Automation' : 'Reply Automation'}
      </button>
    </form>
  );
};

export default AddReelForm;
