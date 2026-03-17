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
    
    const interval = setInterval(() => {
      // Only poll if the tab is actually visible
      if (document.visibilityState === 'visible') {
        fetchLogs();
      }
    }, 3000);

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
      if (level === 'INFO') color = '#60a5fa'; // Blue-400
      if (level === 'ERROR') color = '#f87171'; // Red-400
      if (level === 'WARN') color = '#fbbf24';  // Amber-400
      
      return (
        <>
          <span style={{ color: '#9ca3af' }}>[{time}]</span>{' '}
          <span style={{ color, fontWeight: 500 }}>[{level}]</span>{' '}
          {msg}
        </>
      );
    }
    return log;
  };

  return (
    <div className="log-section" style={{ marginTop: 'var(--spacing-xl)', borderRadius: 'var(--radius-lg)', border: '1px solid #334155', backgroundColor: '#0f172a', color: '#e2e8f0', fontFamily: 'monospace', fontSize: '0.85rem' }}>
      <div className="log-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 16px', borderBottom: '1px solid #334155', backgroundColor: '#1e293b', borderTopLeftRadius: 'var(--radius-lg)', borderTopRightRadius: 'var(--radius-lg)' }}>
        <div className="log-title" style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 600 }}>
          <Terminal size={16} />
          Live Activity Logs
        </div>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>● Polling...</span>
          <button 
            className="btn btn-ghost btn-small" 
            style={{ padding: '2px 8px', fontSize: '0.75rem', color: '#94a3b8' }}
            onClick={() => setLogs([])}
          >
            <Eraser size={12} style={{ marginRight: '4px' }}/> Clear UI
          </button>
        </div>
      </div>
      <div id="logContainer" ref={logContainerRef} style={{ height: '300px', overflowY: 'auto', padding: '16px' }}>
        {logs.length === 0 ? (
          <div style={{ color: '#64748b', fontStyle: 'italic' }}>Waiting for activity...</div>
        ) : (
          logs.map((log, index) => (
            <div key={index} style={{ marginBottom: '4px', lineHeight: '1.5', whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>
              {parseLog(log)}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default LogViewer;
