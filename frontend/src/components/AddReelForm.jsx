import React, { useState, useEffect } from 'react';
import api from '../api';

const AddReelForm = ({ onReelAdded }) => {
  const [formData, setFormData] = useState({
    reelId: '',
    keyword: '',
    message: ''
  });
  const [igReels, setIgReels] = useState([]);
  const [loadingReels, setLoadingReels] = useState(false);

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
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  const handleSelectChange = (e) => {
    const selectedId = e.target.value;
    if (selectedId) {
      setFormData(prev => ({ ...prev, reelId: selectedId }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/api/reels', {
        reel_id: formData.reelId,
        keyword: formData.keyword,
        message: formData.message
      });
      setFormData({ reelId: '', keyword: '', message: '' });
      onReelAdded();
      alert('Reel added successfully!');
    } catch (error) {
      console.error('Error adding reel:', error);
      alert('Failed to add reel');
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
        <label className="form-label">Keyword (optional)</label>
        <input 
          type="text" 
          className="form-input" 
          id="keyword" 
          value={formData.keyword}
          onChange={handleChange}
          placeholder="e.g. link, info, send" 
        />
      </div>
      <div className="form-group">
        <label className="form-label">DM Message</label>
        <textarea 
          className="form-textarea" 
          id="message" 
          value={formData.message}
          onChange={handleChange}
          placeholder="Write your custom message..." 
          required
        ></textarea>
      </div>
      <div className="form-actions">
        <button type="button" className="btn btn-secondary" onClick={() => setFormData({ reelId: '', keyword: '', message: '' })}>
          Clear
        </button>
        <button type="submit" className="btn btn-primary">Save Reel</button>
      </div>
    </form>
  );
};

export default AddReelForm;
