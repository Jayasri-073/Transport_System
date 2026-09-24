import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './AdminDashboard.css';

function AdminDashboard() {
  const navigate = useNavigate();

  // Check if logged in
  useEffect(() => {
    const isLoggedIn = localStorage.getItem('adminLoggedIn');
    if (isLoggedIn !== 'true') {
      navigate('/admin');
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('adminLoggedIn');
    navigate('/admin');
  };

  return (
    <div className="admin-dashboard-container">
      <div className="admin-header-row">
        <h2 className="admin-dashboard-header">👤 Admin Dashboard</h2>
        <button className="logout-button" onClick={handleLogout}>🚪 Logout</button>
      </div>
      <p className="admin-dashboard-welcome">Welcome to the admin dashboard. Manage your transport system data here.</p>

      <ul className="admin-dashboard-menu">
        <li className="admin-dashboard-item">
          <a className="admin-dashboard-link" href="/admin/upload">📁 Upload Data</a>
        </li>
        <li className="admin-dashboard-item">
          <a className="admin-dashboard-link" href="/powerbi">📊 Power BI Dashboard</a>
        </li>
        <li className="admin-dashboard-item">
          <a className="admin-dashboard-link" href="/dashboard">📈 View Public Dashboard</a>
        </li>
        <li className="admin-dashboard-item">
          <a className="admin-dashboard-link" href="/reports">📋 Generate Reports</a>
        </li>
        <li className="admin-dashboard-item">
          <a className="admin-dashboard-link" href="/">🏠 Back to Home</a>
        </li>
      </ul>

      <div className="admin-dashboard-stats">
        <div className="admin-stat-card">
          <div className="admin-stat-number">1,234</div>
          <div className="admin-stat-label">Total Vehicles</div>
        </div>
        <div className="admin-stat-card">
          <div className="admin-stat-number">567</div>
          <div className="admin-stat-label">Active Routes</div>
        </div>
        <div className="admin-stat-card">
          <div className="admin-stat-number">89%</div>
          <div className="admin-stat-label">System Efficiency</div>
        </div>
        <div className="admin-stat-card">
          <div className="admin-stat-number">12</div>
          <div className="admin-stat-label">Alerts Today</div>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;