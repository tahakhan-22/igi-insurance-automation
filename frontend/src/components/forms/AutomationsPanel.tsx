import React, { useState } from 'react';
import { remindersApi, gmailApi } from '../../api';

const AutomationsPanel: React.FC = () => {
  const [loading, setLoading] = useState<{ reminders: boolean; gmail: boolean }>({
    reminders: false,
    gmail: false,
  });
  const [success, setSuccess] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<{ reminders?: any; gmail?: any }>({});

  const handleTriggerReminders = async () => {
    setLoading({ ...loading, reminders: true });
    setError(null);
    setSuccess(null);
    
    try {
      const response = await remindersApi.trigger();
      setSuccess('✅ CSV Payment Reminders triggered successfully!');
      setResults({ ...results, reminders: response.data });
      console.log('Reminders result:', response.data);
    } catch (err: any) {
      setError(`❌ Error triggering reminders: ${err.response?.data?.detail || err.message}`);
      console.error('Reminders error:', err);
    } finally {
      setLoading({ ...loading, reminders: false });
    }
  };

  const handleTriggerGmail = async () => {
    setLoading({ ...loading, gmail: true });
    setError(null);
    setSuccess(null);
    
    try {
      const response = await gmailApi.poll();
      setSuccess('✅ Gmail polling triggered successfully!');
      setResults({ ...results, gmail: response.data });
      console.log('Gmail result:', response.data);
    } catch (err: any) {
      setError(`❌ Error polling Gmail: ${err.response?.data?.detail || err.message}`);
      console.error('Gmail error:', err);
    } finally {
      setLoading({ ...loading, gmail: false });
    }
  };

  return (
    <div className="automations-panel">
      <div className="page-header">
        <h1>🤖 Automations Control Panel</h1>
        <p className="subtitle">Manually trigger automated tasks</p>
      </div>

      {success && (
        <div className="alert alert-success">
          <span>{success}</span>
          <button className="alert-close" onClick={() => setSuccess(null)}>×</button>
        </div>
      )}

      {error && (
        <div className="alert alert-error">
          <span>{error}</span>
          <button className="alert-close" onClick={() => setError(null)}>×</button>
        </div>
      )}

      <div className="automations-grid">
        {/* CSV Payment Reminders */}
        <div className="automation-card">
          <div className="automation-icon">📧</div>
          <h2>CSV Payment Reminders</h2>
          <p className="automation-description">
            Reads <code>due_payments.csv</code> and sends email/SMS reminders to clients with upcoming payments (30-day window).
          </p>
          
          <div className="automation-info">
            <div className="info-row">
              <span className="label">Schedule:</span>
              <span className="value">Automatic daily at 8:00 AM</span>
            </div>
            <div className="info-row">
              <span className="label">CSV File:</span>
              <span className="value">backend/app/data/due_payments.csv</span>
            </div>
            <div className="info-row">
              <span className="label">Status:</span>
              <span className="status-badge status-active">🟢 Active</span>
            </div>
          </div>

          <button
            className="btn btn-primary btn-large"
            onClick={handleTriggerReminders}
            disabled={loading.reminders}
          >
            {loading.reminders ? (
              <>⏳ Processing...</>
            ) : (
              <>▶️ Trigger Reminders Now</>
            )}
          </button>

          {results.reminders && (
            <div className="result-box">
              <strong>Last Run Result:</strong>
              <pre>{JSON.stringify(results.reminders, null, 2)}</pre>
            </div>
          )}
        </div>

        {/* Gmail Policy Creation */}
        <div className="automation-card">
          <div className="automation-icon">📬</div>
          <h2>Gmail Policy Creation</h2>
          <p className="automation-description">
            Polls Gmail inbox, detects car insurance emails, extracts client/vehicle data, and creates draft policies automatically.
          </p>
          
          <div className="automation-info">
            <div className="info-row">
              <span className="label">Schedule:</span>
              <span className="value">Automatic every 5 minutes</span>
            </div>
            <div className="info-row">
              <span className="label">Keywords:</span>
              <span className="value">car insurance, motor policy, vehicle</span>
            </div>
            <div className="info-row">
              <span className="label">Status:</span>
              <span className="status-badge status-active">🟢 Active</span>
            </div>
          </div>

          <button
            className="btn btn-primary btn-large"
            onClick={handleTriggerGmail}
            disabled={loading.gmail}
          >
            {loading.gmail ? (
              <>⏳ Polling...</>
            ) : (
              <>▶️ Poll Gmail Now</>
            )}
          </button>

          {results.gmail && (
            <div className="result-box">
              <strong>Last Run Result:</strong>
              <pre>{JSON.stringify(results.gmail, null, 2)}</pre>
            </div>
          )}
        </div>
      </div>

      <div className="automation-notes">
        <h3>ℹ️ Important Notes</h3>
        <ul>
          <li><strong>Automatic Scheduling:</strong> Both automations run automatically in the background via APScheduler. These buttons are for manual testing.</li>
          <li><strong>CSV Reminders:</strong> Make sure <code>due_payments.csv</code> has valid data with client_name, email, phone, due_amount, and due_date columns.</li>
          <li><strong>Gmail:</strong> OAuth 2.0 authentication must be completed first. See <code>GMAIL_SETUP_GUIDE.md</code> for setup instructions.</li>
          <li><strong>Logs:</strong> Check backend console logs for detailed execution information.</li>
        </ul>
      </div>

      <div className="automation-help">
        <h3>📚 Documentation</h3>
        <div className="help-links">
          <a href="#" className="help-link" onClick={(e) => { e.preventDefault(); alert('See PROJECT_OVERVIEW.md for details'); }}>
            📖 How Automations Work
          </a>
          <a href="#" className="help-link" onClick={(e) => { e.preventDefault(); alert('See GMAIL_SETUP_GUIDE.md for setup'); }}>
            🔧 Gmail Setup Guide
          </a>
          <a href="#" className="help-link" onClick={(e) => { e.preventDefault(); alert('Check backend/app/data/due_payments.csv'); }}>
            📄 CSV Format Example
          </a>
        </div>
      </div>
    </div>
  );
};

export default AutomationsPanel;
