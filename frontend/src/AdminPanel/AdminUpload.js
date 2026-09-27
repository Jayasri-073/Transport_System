import React, { useEffect, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { uploadCSV } from '../services/api';
import './AdminPanel.css';

function AdminUpload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInput = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!localStorage.getItem('adminToken')) navigate('/admin');
  }, [navigate]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) return setError('Select a CSV file before uploading.');
    setUploading(true);
    setError(null);
    setResult(null);
    try {
      const response = await uploadCSV(file, localStorage.getItem('adminToken'));
      setResult(response);
      setFile(null);
      if (fileInput.current) fileInput.current.value = '';
    } catch (requestError) {
      if (requestError.message.includes('session has expired') || requestError.message.includes('Authentication required')) {
        localStorage.removeItem('adminToken');
        navigate('/admin');
        return;
      }
      setError(requestError.message || 'Failed to upload the CSV file.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="admin-container">
      <h2 className="admin-header">Upload CSV Data</h2>
      <div className="admin-upload">
        <form onSubmit={handleSubmit}>
          <div className="upload-section">
            <label className="file-label" htmlFor="dataset-file">Select CSV file</label>
            <input id="dataset-file" ref={fileInput} type="file" accept=".csv,text/csv" onChange={(event) => { setFile(event.target.files[0] || null); setResult(null); setError(null); }} disabled={uploading} />
            {file && <div className="file-info"><p>Selected: <strong>{file.name}</strong></p><p>Size: {(file.size / 1024).toFixed(2)} KB</p></div>}
          </div>
          <div className="required-columns"><p><strong>Required columns</strong></p><code>vehicle_id, route, speed_kmph, timestamp, latitude, longitude</code></div>
          <button className="admin-button upload-btn" type="submit" disabled={!file || uploading}>{uploading ? 'Uploading...' : 'Upload CSV'}</button>
        </form>
        {error && <div className="upload-error" role="alert">{error}</div>}
        {result && <div className="upload-success"><p>{result.message}</p><p>Rows: <strong>{result.rows.toLocaleString()}</strong></p><p>Columns: {result.columns.join(', ')}</p><Link to="/powerbi" className="view-dashboard-link">View Analytics Dashboard</Link></div>}
        <Link className="admin-link" to="/admin/dashboard">Back to Dashboard</Link>
      </div>
    </div>
  );
}

export default AdminUpload;
