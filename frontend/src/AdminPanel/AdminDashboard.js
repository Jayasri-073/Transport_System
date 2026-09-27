import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './AdminDashboard.css';

function AdminDashboard() {
  const navigate = useNavigate();

  useEffect(() => {
    if (!localStorage.getItem('adminToken')) navigate('/admin');
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('adminToken');
    navigate('/admin');
  };

  return (
    <div className="admin-dashboard-container">
      <div className="admin-header-row">
        <h2 className="admin-dashboard-header">Admin Dashboard</h2>
        <button className="logout-button" onClick={handleLogout}>Logout</button>
      </div>
      <p className="admin-dashboard-welcome">Manage the active transport dataset and review the public analysis views.</p>
      <ul className="admin-dashboard-menu">
        <li className="admin-dashboard-item"><Link className="admin-dashboard-link" to="/admin/upload">Upload Data</Link></li>
        <li className="admin-dashboard-item"><Link className="admin-dashboard-link" to="/powerbi">Analytics Dashboard</Link></li>
        <li className="admin-dashboard-item"><Link className="admin-dashboard-link" to="/dashboard">View Public Dashboard</Link></li>
        <li className="admin-dashboard-item"><Link className="admin-dashboard-link" to="/reports">View Reports</Link></li>
        <li className="admin-dashboard-item"><Link className="admin-dashboard-link" to="/">Back to Home</Link></li>
      </ul>
    </div>
  );
}

export default AdminDashboard;
