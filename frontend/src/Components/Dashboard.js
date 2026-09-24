import React, { useState, useEffect } from 'react';
import { getDashboardData, getPeakHours, getCongestionData, getWeeklyTrends } from '../services/api';
import './Dashboard.css';

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [peakHours, setPeakHours] = useState(null);
  const [congestion, setCongestion] = useState(null);
  const [weeklyTrends, setWeeklyTrends] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const [dashboard, peaks, congestionData, weekly] = await Promise.all([
          getDashboardData(),
          getPeakHours(),
          getCongestionData(),
          getWeeklyTrends()
        ]);

        setDashboardData(dashboard.data);
        setPeakHours(peaks.data);
        setCongestion(congestionData.data);
        setWeeklyTrends(weekly.data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch data. Make sure the backend is running on port 5000.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
    // Refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="dashboard loading">
        <div className="loader"></div>
        <p>Loading dashboard data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard error">
        <div className="error-icon">⚠️</div>
        <h2>Connection Error</h2>
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>Retry</button>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>🚗 Smart City Transport Dashboard</h1>
        <p className="subtitle">Real-time Traffic Monitoring & Analysis</p>
      </header>

      {/* Key Metrics Cards */}
      <section className="metrics-grid">
        <div className="metric-card total-vehicles">
          <div className="metric-icon">🚌</div>
          <div className="metric-content">
            <h3>Total Vehicles</h3>
            <span className="metric-value">{dashboardData?.total_vehicles?.toLocaleString()}</span>
          </div>
        </div>

        <div className="metric-card total-trips">
          <div className="metric-icon">📍</div>
          <div className="metric-content">
            <h3>Total Trips</h3>
            <span className="metric-value">{dashboardData?.total_trips?.toLocaleString()}</span>
          </div>
        </div>

        <div className="metric-card avg-speed">
          <div className="metric-icon">⚡</div>
          <div className="metric-content">
            <h3>Average Speed</h3>
            <span className="metric-value">{dashboardData?.average_speed} <small>km/h</small></span>
          </div>
        </div>

        <div className={`metric-card congestion-level ${dashboardData?.congestion_level?.toLowerCase()}`}>
          <div className="metric-icon">🚦</div>
          <div className="metric-content">
            <h3>Congestion Level</h3>
            <span className="metric-value">{dashboardData?.congestion_level}</span>
          </div>
        </div>
      </section>

      {/* Peak Hours Section */}
      <section className="chart-section">
        <h2>⏰ Peak Traffic Hours</h2>
        <div className="peak-hours-grid">
          <div className="peak-card morning">
            <h4>Morning Peak</h4>
            <span className="peak-time">{peakHours?.morning_peak?.hour}:00</span>
            <span className="peak-count">{peakHours?.morning_peak?.vehicle_count} vehicles</span>
          </div>
          <div className="peak-card evening">
            <h4>Evening Peak</h4>
            <span className="peak-time">{peakHours?.evening_peak?.hour}:00</span>
            <span className="peak-count">{peakHours?.evening_peak?.vehicle_count} vehicles</span>
          </div>
        </div>

        {/* Hourly Bar Chart */}
        <div className="hourly-chart">
          {peakHours?.hourly_data?.map((hour) => (
            <div key={hour.hour} className="hour-bar">
              <div
                className="bar-fill"
                style={{ height: `${(hour.vehicle_count / Math.max(...peakHours.hourly_data.map(h => h.vehicle_count))) * 100}%` }}
                title={`${hour.hour}:00 - ${hour.vehicle_count} vehicles, ${hour.avg_speed} km/h`}
              ></div>
              <span className="hour-label">{hour.hour}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Route Congestion Section */}
      <section className="chart-section">
        <h2>🛣️ Route Congestion Status</h2>
        <div className="routes-grid">
          {congestion?.routes?.map((route) => (
            <div key={route.route} className={`route-card ${route.severity}`}>
              <h4>{route.route}</h4>
              <div className="route-stats">
                <span className="speed">{route.avg_speed} km/h</span>
                <span className={`severity-badge ${route.severity}`}>{route.severity}</span>
              </div>
              <div className="vehicle-count">{route.vehicle_count} trips</div>
            </div>
          ))}
        </div>
      </section>

      {/* Congestion Hotspots */}
      <section className="chart-section">
        <h2>🔥 Congestion Hotspots</h2>
        <div className="hotspots-table">
          <table>
            <thead>
              <tr>
                <th>Location</th>
                <th>Route</th>
                <th>Avg Speed</th>
                <th>Incidents</th>
                <th>Severity</th>
              </tr>
            </thead>
            <tbody>
              {congestion?.hotspots?.slice(0, 5).map((hotspot, idx) => (
                <tr key={idx}>
                  <td>{hotspot.latitude.toFixed(2)}°, {hotspot.longitude.toFixed(2)}°</td>
                  <td>{hotspot.route}</td>
                  <td>{hotspot.avg_speed} km/h</td>
                  <td>{hotspot.incident_count}</td>
                  <td><span className={`severity-badge ${hotspot.severity}`}>{hotspot.severity}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Weekly Trends */}
      <section className="chart-section">
        <h2>📅 Weekly Traffic Pattern</h2>
        <div className="weekly-chart">
          {weeklyTrends?.weekly_data?.map((day) => (
            <div key={day.day} className={`day-bar ${day.day_of_week >= 5 ? 'weekend' : 'weekday'}`}>
              <div
                className="bar-fill"
                style={{ height: `${(day.trip_count / Math.max(...weeklyTrends.weekly_data.map(d => d.trip_count))) * 100}%` }}
              >
                <span className="trip-count">{day.trip_count}</span>
              </div>
              <span className="day-label">{day.day.slice(0, 3)}</span>
            </div>
          ))}
        </div>
        <div className="weekly-summary">
          <p>📈 Busiest Day: <strong>{weeklyTrends?.busiest_day}</strong></p>
        </div>
      </section>

      <footer className="dashboard-footer">
        <p>Last updated: {new Date().toLocaleTimeString()}</p>
        <p>Auto-refresh: Every 30 seconds</p>
      </footer>
    </div>
  );
}
