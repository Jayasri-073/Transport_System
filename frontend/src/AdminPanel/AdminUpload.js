import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { uploadCSV } from '../services/api';
import './AdminPanel.css';

function AdminUpload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  // Check if logged in
  useEffect(() => {
    const isLoggedIn = localStorage.getItem('adminLoggedIn');
    if (isLoggedIn !== 'true') {
      navigate('/admin');
    }
  }, [navigate]);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setResult(null);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError('Please select a file');
      return;
    }

    if (!file.name.endsWith('.csv')) {
      setError('Please select a CSV file');
      return;
    }

    setUploading(true);
    setError(null);
    setResult(null);

    try {
      const response = await uploadCSV(file);

      if (response.success) {
        setResult({
          message: response.message,
          rows: response.rows,
          columns: response.columns
        });
        setFile(null);
        // Reset file input
        document.querySelector('input[type="file"]').value = '';
      } else {
        setError(response.error || 'Upload failed');
      }
    } catch (err) {
      setError('Failed to upload file. Is the backend running?');
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="admin-container">
      <h2 className="admin-header">📁 Upload CSV Data</h2>

      <div className="admin-upload">
        <form onSubmit={handleSubmit}>
          <div className="upload-section">
            <label className="file-label">
              <span>📄 Select CSV file:</span>
              <input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                disabled={uploading}
              />
            </label>

            {file && (
              <div className="file-info">
                <p>📎 Selected: <strong>{file.name}</strong></p>
                <p>Size: {(file.size / 1024).toFixed(2)} KB</p>
              </div>
            )}
          </div>

          <div className="required-columns">
            <p><strong>Required columns:</strong></p>
            <code>vehicle_id, route, speed_kmph, timestamp</code>
          </div>

          <button
            className="admin-button upload-btn"
            type="submit"
            disabled={!file || uploading}
          >
            {uploading ? '⏳ Uploading...' : '🚀 Upload CSV'}
          </button>
        </form>

        {error && (
          <div className="upload-error">
            ❌ {error}
          </div>
        )}

        {result && (
          <div className="upload-success">
            <p>✅ {result.message}</p>
            <p>📊 Rows: <strong>{result.rows.toLocaleString()}</strong></p>
            <p>📋 Columns: {result.columns.join(', ')}</p>
            <a href="/powerbi" className="view-dashboard-link">
              📊 View Power BI Dashboard →
            </a>
          </div>
        )}

        <a className="admin-link" href="/admin/dashboard">← Back to Dashboard</a>
      </div>
    </div>
  );
}

export default AdminUpload;