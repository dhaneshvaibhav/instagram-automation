import React, { useEffect, useState, useRef } from 'react';
import api from '../api';
import { Terminal, Eraser } from 'lucide-react';

const LogViewer = () => {
  const [logs, setLogs] = useState([]);
  const logContainerRef = useRef(null);

  const fetchLogs = async () => {
    try {
      const response = await api.get('/api/logs');
      setLogs(response.data.logs || []);
    } catch (error) {
      console.error('Error fetching logs:', error);
    }
  };

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(fetchLogs, 3000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // Auto-scroll to bottom
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs]);

  const parseLog = (log) => {
    const match = log.match(/^\[(.*?)\] \[(.*?)\] (.*)$/);
    if (match) {
      const [_, time, level, msg] = match;
      let color = '#d4d4d4';
      if (level === 'INFO') color = '#4fc3f7';
      if (level === 'ERROR') color = '#f44336';
      if (level === 'WARN') color = '#ffb74d';
      
      return (
        <>
          <span className="log-time">[{time}]</span>{' '}
          <span style={{ color }}>[{level}]</span>{' '}
          {msg}
        </>
      );
    }
    return log;
  };

  return (
    <div className="log-section" ref={logContainerRef}>
      <div className="log-header" style={{ position: 'sticky', top: 0, backgroundColor: '#1e1e1e', zIndex: 10 }}>
        <div className="log-title">
          <Terminal size={16} />
          Live Activity Logs
        </div>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <span style={{ fontSize: '11px', color: '#888' }}>● Polling...</span>
          <button 
            className="btn btn-secondary btn-small" 
            style={{ padding: '2px 8px', fontSize: '11px', background: 'transparent', color: '#888', borderColor: '#444' }}
            onClick={() => setLogs([])}
          >
            <Eraser size={12} style={{ marginRight: '4px' }}/> Clear UI
          </button>
        </div>
      </div>
      <div id="logContainer">
        {logs.length === 0 ? (
          <div className="log-entry" style={{ color: '#888' }}>Waiting for activity...</div>
        ) : (
          logs.map((log, index) => (
            <div key={index} className="log-entry">
              {parseLog(log)}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default LogViewer;
