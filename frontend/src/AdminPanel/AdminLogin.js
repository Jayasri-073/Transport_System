import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginAdmin } from '../services/api';
import './AdminPanel.css';

function AdminLogin() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (localStorage.getItem('adminToken')) navigate('/admin/dashboard');
  }, [navigate]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    setError('');
    try {
      const response = await loginAdmin(username, password);
      localStorage.setItem('adminToken', response.token);
      navigate('/admin/dashboard');
    } catch (requestError) {
      setError(requestError.message || 'Unable to sign in.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="admin-container">
      <h2 className="admin-header">Admin Login</h2>
      <form className="admin-form" onSubmit={handleSubmit}>
        <div>
          <label htmlFor="admin-username">Username</label>
          <input id="admin-username" type="text" value={username} onChange={(event) => setUsername(event.target.value)} autoComplete="username" required />
        </div>
        <div>
          <label htmlFor="admin-password">Password</label>
          <input id="admin-password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} autoComplete="current-password" required />
        </div>
        {error && <p className="upload-error" role="alert">{error}</p>}
        <button className="admin-button" type="submit" disabled={submitting}>{submitting ? 'Signing in...' : 'Login'}</button>
      </form>
    </div>
  );
}

export default AdminLogin;
