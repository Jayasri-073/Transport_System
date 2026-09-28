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
      const loginErrors = {
        401: 'Incorrect username or password.',
        403: 'Your account is not permitted to access the admin area.',
        404: 'Admin login is unavailable because the API endpoint was not found.',
        405: 'Admin login is incorrectly configured: the API does not accept POST at this endpoint.',
        500: 'The server could not complete the login. Please try again shortly.',
        0: 'Unable to connect to the transport server. Check your connection and try again.',
      };
      setError(loginErrors[requestError.status] || requestError.message || 'Unable to sign in.');
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
