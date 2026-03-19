import React, { useState, useEffect } from 'react';
import api from '../api';
import { Plus, Trash2 } from 'lucide-react';

const AddReelForm = ({ onReelAdded, externalReelId }) => {
  const [formData, setFormData] = useState({
    reelId: '',
    keyword: '',
    message: ''
  });
  const [buttons, setButtons] = useState([]);
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
    setFormData({ ...formData, [e.target.id]: e.target.value });
  };

  const handleSelectChange = (e) => {
    const selectedId = e.target.value;
    if (selectedId) {
      setFormData(prev => ({ ...prev, reelId: selectedId }));
    }
  };

  const handleAddButton = () => {
    if (buttons.length >= 3) return;
    setButtons([...buttons, { type: 'web_url', title: '', url: '', payload: '' }]);
  };

  const handleRemoveButton = (index) => {
    setButtons(buttons.filter((_, i) => i !== index));
  };

  const handleButtonChange = (index, field, value) => {
    const newButtons = [...buttons];
    newButtons[index][field] = value;
    setButtons(newButtons);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Filter out invalid buttons before sending
      const validButtons = buttons.map(btn => {
        const cleanBtn = { type: btn.type, title: btn.title };
        if (btn.type === 'web_url') cleanBtn.url = btn.url;
        if (btn.type === 'postback') cleanBtn.payload = btn.payload;
        return cleanBtn;
      }).filter(btn => btn.title && (btn.url || btn.payload));

      await api.post('/api/reels', {
        reel_id: formData.reelId,
        keyword: formData.keyword,
        message: formData.message,
        buttons: validButtons.length > 0 ? validButtons : null
      });
      setFormData({ reelId: '', keyword: '', message: '' });
      setButtons([]);
      onReelAdded();
      // Use simple UI feedback instead of blocking alert
    } catch (error) {
      console.error('Error adding reel:', error);
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
        <p className="text-xs text-muted" style={{ marginTop: '4px' }}>
          Tip: You can also use the "View My Media" gallery above.
        </p>
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
          placeholder="e.g. 'price' or 'info'" 
        />
      </div>
      <div className="form-group">
        <label className="form-label">Message Template</label>
        <textarea 
          className="form-input" 
          id="message" 
          rows="4" 
          value={formData.message}
          onChange={handleChange}
          placeholder="Enter the DM message here..." 
          required
        ></textarea>
      </div>

      <div className="form-group" style={{ marginTop: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
          <label className="form-label" style={{ marginBottom: 0 }}>Buttons (Max 3)</label>
          {buttons.length < 3 && (
            <button type="button" className="btn btn-secondary btn-xs" onClick={handleAddButton}>
              <Plus size={14} style={{ marginRight: '4px' }} /> Add Button
            </button>
          )}
        </div>
        
        {buttons.map((btn, index) => (
          <div key={index} style={{ 
            backgroundColor: 'var(--bg-subtle)', 
            padding: '12px', 
            borderRadius: 'var(--radius-md)', 
            marginBottom: '12px',
            border: '1px solid var(--border-color)',
            position: 'relative'
          }}>
            <button 
              type="button" 
              style={{ position: 'absolute', top: '8px', right: '8px', color: 'var(--danger)', background: 'none', border: 'none', cursor: 'pointer' }}
              onClick={() => handleRemoveButton(index)}
            >
              <Trash2 size={14} />
            </button>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '8px', marginBottom: '8px' }}>
              <div>
                <label className="text-xs text-muted">Type</label>
                <select 
                  className="form-select form-select-sm" 
                  value={btn.type}
                  onChange={(e) => handleButtonChange(index, 'type', e.target.value)}
                >
                  <option value="web_url">URL Button</option>
                  <option value="postback">Postback Button</option>
                </select>
              </div>
              <div>
                <label className="text-xs text-muted">Button Title</label>
                <input 
                  type="text" 
                  className="form-input form-input-sm" 
                  value={btn.title}
                  onChange={(e) => handleButtonChange(index, 'title', e.target.value)}
                  placeholder="e.g. Visit Website"
                />
              </div>
            </div>
            
            {btn.type === 'web_url' ? (
              <div>
                <label className="text-xs text-muted">URL</label>
                <input 
                  type="url" 
                  className="form-input form-input-sm" 
                  value={btn.url}
                  onChange={(e) => handleButtonChange(index, 'url', e.target.value)}
                  placeholder="https://example.com"
                />
              </div>
            ) : (
              <div>
                <label className="text-xs text-muted">Payload (sent to your webhook)</label>
                <input 
                  type="text" 
                  className="form-input form-input-sm" 
                  value={btn.payload}
                  onChange={(e) => handleButtonChange(index, 'payload', e.target.value)}
                  placeholder="e.g. user_clicked_more_info"
                />
              </div>
            )}
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
        <button 
          type="button" 
          className="btn btn-secondary" 
          style={{ flex: 1 }}
          onClick={() => {
            setFormData({ reelId: '', keyword: '', message: '' });
            setButtons([]);
          }}
        >
          Clear
        </button>
        <button type="submit" className="btn btn-primary" style={{ flex: 2 }}>
          Save Automation Rule
        </button>
      </div>
    </form>
  );
};

export default AddReelForm;
