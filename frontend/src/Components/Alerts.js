import React, { useState, useEffect } from 'react';
import { getAlerts, getRealtimeSimulation } from '../services/api';
import './Alerts.css';

export default function Alerts() {
  const [alertsData, setAlertsData] = useState(null);
  const [realtimeData, setRealtimeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [alerts, realtime] = await Promise.all([
          getAlerts(),
          getRealtimeSimulation()
        ]);
        setAlertsData(alerts.data);
        setRealtimeData(realtime.data);
      } catch (err) {
        console.error('Failed to fetch alerts:', err);
      } finally {
        setLoading(false);
      }
    }

    fetchData();

    let interval;
    if (autoRefresh) {
      interval = setInterval(fetchData, 5000); // Refresh every 5 seconds
    }

    return () => clearInterval(interval);
  }, [autoRefresh]);

  if (loading) {
    return (
      <div className="alerts-page loading">
        <div className="loader"></div>
        <p>Loading alerts...</p>
      </div>
    );
  }

  return (
    <div className="alerts-page">
      <header className="page-header">
        <h1>🚨 Live Traffic Alerts</h1>
        <div className="refresh-toggle">
          <label>
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
            />
            Auto-refresh (5s)
          </label>
          <span className={`status-dot ${autoRefresh ? 'active' : ''}`}></span>
        </div>
      </header>

      {/* Alert Summary */}
      <section className="alert-summary">
        <div className="summary-card total">
          <span className="count">{alertsData?.total_alerts || 0}</span>
          <span className="label">Total Alerts</span>
        </div>
        <div className="summary-card high">
          <span className="count">{alertsData?.high_severity || 0}</span>
          <span className="label">High Severity</span>
        </div>
        <div className="summary-card time">
          <span className="count">{new Date().toLocaleTimeString()}</span>
          <span className="label">Last Updated</span>
        </div>
      </section>

      {/* Active Alerts */}
      <section className="alerts-section">
        <h2>⚠️ Active Alerts</h2>
        <div className="alerts-list">
          {alertsData?.alerts?.length === 0 ? (
            <div className="no-alerts">
              <span>✅</span>
              <p>No active alerts. All routes operating normally.</p>
            </div>
          ) : (
            alertsData?.alerts?.map((alert, idx) => (
              <div key={idx} className={`alert-card ${alert.severity}`}>
                <div className="alert-icon">
                  {alert.severity === 'high' ? '🔴' : '🟡'}
                </div>
                <div className="alert-content">
                  <h4>{alert.type.replace('_', ' ').toUpperCase()}</h4>
                  <p>{alert.message}</p>
                  {alert.route && <span className="route-tag">{alert.route}</span>}
                </div>
                <div className="alert-time">
                  {new Date(alert.timestamp).toLocaleTimeString()}
                </div>
              </div>
            ))
          )}
        </div>
      </section>

      {/* Real-time Traffic Simulation */}
      <section className="realtime-section">
        <h2>📡 Real-time Traffic Feed</h2>
        <div className="realtime-header">
          <span className={`congestion-status ${realtimeData?.current_congestion?.toLowerCase()}`}>
            Current Congestion: {realtimeData?.current_congestion}
          </span>
          <span className="simulation-badge">SIMULATION</span>
        </div>

        <div className="vehicle-feed">
          <table>
            <thead>
              <tr>
                <th>Vehicle ID</th>
                <th>Route</th>
                <th>Speed</th>
                <th>Location</th>
              </tr>
            </thead>
            <tbody>
              {realtimeData?.vehicles?.slice(0, 10).map((vehicle, idx) => (
                <tr key={idx} className={vehicle.speed_kmph < 30 ? 'slow' : ''}>
                  <td>{vehicle.vehicle_id}</td>
                  <td>{vehicle.route}</td>
                  <td>
                    <span className={`speed ${vehicle.speed_kmph < 30 ? 'slow' : vehicle.speed_kmph > 60 ? 'fast' : ''}`}>
                      {vehicle.speed_kmph} km/h
                    </span>
                  </td>
                  <td>{vehicle.latitude.toFixed(4)}°, {vehicle.longitude.toFixed(4)}°</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
