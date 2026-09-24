import React, { useState, useEffect } from 'react';
import { getDailyTrends, getWeeklyTrends, getSpeedAnalysis } from '../services/api';
import './Reports.css';

export default function Reports() {
  const [dailyTrends, setDailyTrends] = useState(null);
  const [weeklyTrends, setWeeklyTrends] = useState(null);
  const [speedAnalysis, setSpeedAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('daily');

  useEffect(() => {
    async function fetchData() {
      try {
        const [daily, weekly, speed] = await Promise.all([
          getDailyTrends(),
          getWeeklyTrends(),
          getSpeedAnalysis()
        ]);
        setDailyTrends(daily.data);
        setWeeklyTrends(weekly.data);
        setSpeedAnalysis(speed.data);
      } catch (err) {
        console.error('Failed to fetch reports:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="reports-page loading">
        <div className="loader"></div>
        <p>Loading reports...</p>
      </div>
    );
  }

  return (
    <div className="reports-page">
      <header className="page-header">
        <h1>📊 Historical Reports</h1>
        <p>Traffic analysis and trends</p>
      </header>

      {/* Statistics Overview */}
      <section className="stats-overview">
        <div className="stat-card">
          <h3>Average Daily Trips</h3>
          <span className="stat-value">{dailyTrends?.summary?.avg_daily_trips?.toLocaleString()}</span>
        </div>
        <div className="stat-card">
          <h3>Mean Speed</h3>
          <span className="stat-value">{speedAnalysis?.overall?.mean?.toFixed(1)} <small>km/h</small></span>
        </div>
        <div className="stat-card">
          <h3>Speed Range</h3>
          <span className="stat-value">{speedAnalysis?.overall?.min?.toFixed(0)} - {speedAnalysis?.overall?.max?.toFixed(0)} <small>km/h</small></span>
        </div>
        <div className="stat-card">
          <h3>Busiest Day</h3>
          <span className="stat-value">{weeklyTrends?.busiest_day}</span>
        </div>
      </section>

      {/* Tabs */}
      <div className="tabs">
        <button
          className={activeTab === 'daily' ? 'active' : ''}
          onClick={() => setActiveTab('daily')}
        >
          📅 Daily Trends
        </button>
        <button
          className={activeTab === 'weekly' ? 'active' : ''}
          onClick={() => setActiveTab('weekly')}
        >
          📆 Weekly Trends
        </button>
        <button
          className={activeTab === 'speed' ? 'active' : ''}
          onClick={() => setActiveTab('speed')}
        >
          ⚡ Speed Analysis
        </button>
      </div>

      {/* Daily Trends Tab */}
      {activeTab === 'daily' && (
        <section className="report-section">
          <h2>Daily Traffic Trends</h2>
          <div className="data-table">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Trip Count</th>
                  <th>Avg Speed (km/h)</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {dailyTrends?.daily_data?.map((day, idx) => (
                  <tr key={idx}>
                    <td>{day.date}</td>
                    <td>{day.trip_count}</td>
                    <td>{day.avg_speed}</td>
                    <td>
                      <span className={`status-badge ${day.avg_speed < 40 ? 'congested' : day.avg_speed < 60 ? 'moderate' : 'clear'}`}>
                        {day.avg_speed < 40 ? 'Congested' : day.avg_speed < 60 ? 'Moderate' : 'Clear'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="summary-box">
            <h4>Summary</h4>
            <p><strong>Highest Traffic Day:</strong> {dailyTrends?.summary?.max_trips_day?.date} ({dailyTrends?.summary?.max_trips_day?.trip_count} trips)</p>
            <p><strong>Lowest Traffic Day:</strong> {dailyTrends?.summary?.min_trips_day?.date} ({dailyTrends?.summary?.min_trips_day?.trip_count} trips)</p>
          </div>
        </section>
      )}

      {/* Weekly Trends Tab */}
      {activeTab === 'weekly' && (
        <section className="report-section">
          <h2>Weekly Traffic Pattern</h2>
          <div className="weekly-chart">
            {weeklyTrends?.weekly_data?.map((day) => (
              <div key={day.day} className="day-column">
                <div className="bar-container">
                  <div
                    className={`bar ${day.day_of_week >= 5 ? 'weekend' : 'weekday'}`}
                    style={{
                      height: `${(day.trip_count / Math.max(...weeklyTrends.weekly_data.map(d => d.trip_count))) * 200}px`
                    }}
                  >
                    <span className="bar-value">{day.trip_count}</span>
                  </div>
                </div>
                <span className="day-label">{day.day}</span>
                <span className="speed-label">{day.avg_speed} km/h</span>
              </div>
            ))}
          </div>

          <div className="comparison-box">
            <h4>Weekday vs Weekend</h4>
            <div className="comparison-stats">
              <div className="comp-stat">
                <span className="label">Weekday Avg</span>
                <span className="value">{weeklyTrends?.weekend_vs_weekday?.weekday_avg?.toFixed(0)} trips</span>
              </div>
              <div className="comp-stat">
                <span className="label">Weekend Avg</span>
                <span className="value">{weeklyTrends?.weekend_vs_weekday?.weekend_avg?.toFixed(0)} trips</span>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Speed Analysis Tab */}
      {activeTab === 'speed' && (
        <section className="report-section">
          <h2>Speed Distribution Analysis</h2>

          <div className="speed-stats">
            <div className="speed-stat">
              <span className="label">25th Percentile</span>
              <span className="value">{speedAnalysis?.overall?.percentile_25?.toFixed(1)} km/h</span>
            </div>
            <div className="speed-stat highlight">
              <span className="label">Median (50th)</span>
              <span className="value">{speedAnalysis?.overall?.percentile_50?.toFixed(1)} km/h</span>
            </div>
            <div className="speed-stat">
              <span className="label">75th Percentile</span>
              <span className="value">{speedAnalysis?.overall?.percentile_75?.toFixed(1)} km/h</span>
            </div>
            <div className="speed-stat">
              <span className="label">Std Deviation</span>
              <span className="value">{speedAnalysis?.overall?.std?.toFixed(1)} km/h</span>
            </div>
          </div>

          <h3>Speed by Hour</h3>
          <div className="hourly-speed-chart">
            {Object.entries(speedAnalysis?.by_hour || {}).map(([hour, speed]) => (
              <div key={hour} className="hour-speed">
                <div
                  className="speed-bar"
                  style={{ width: `${(speed / 120) * 100}%` }}
                  title={`${speed} km/h`}
                ></div>
                <span className="hour">{hour}:00</span>
                <span className="speed-value">{speed.toFixed(1)}</span>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
