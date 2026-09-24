import React, { useState, useEffect } from 'react';
import { getPredictions, getHistoricalVsRealtime } from '../services/api';
import './Predictions.css';

export default function Predictions() {
  const [predictions, setPredictions] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [pred, comp] = await Promise.all([
          getPredictions(),
          getHistoricalVsRealtime()
        ]);
        setPredictions(pred.data);
        setComparison(comp.data);
      } catch (err) {
        console.error('Failed to fetch predictions:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="predictions-page loading">
        <div className="loader"></div>
        <p>Loading predictions...</p>
      </div>
    );
  }

  return (
    <div className="predictions-page">
      <header className="page-header">
        <h1>🔮 Traffic Predictions</h1>
        <p>ML-powered traffic forecasting</p>
      </header>

      {/* Current Prediction */}
      <section className="current-prediction">
        <div className="prediction-card main">
          <div className="prediction-icon">🚗</div>
          <div className="prediction-content">
            <h3>Current Hour Prediction</h3>
            <div className="prediction-time">{predictions?.current_hour}:00</div>
            <div className="prediction-speed">
              <span className="value">{predictions?.current_prediction}</span>
              <span className="unit">km/h</span>
            </div>
          </div>
        </div>
      </section>

      {/* Hourly Predictions */}
      <section className="hourly-predictions">
        <h2>📊 Predicted Speeds by Hour</h2>
        <div className="predictions-grid">
          {predictions?.predictions_by_hour && Object.entries(predictions.predictions_by_hour).map(([key, value]) => {
            const hour = key.replace('hour_', '');
            return (
              <div key={key} className="hour-prediction-card">
                <span className="hour">{hour}:00</span>
                <span className="predicted-speed">{value} km/h</span>
                <span className={`traffic-status ${value < 40 ? 'slow' : value < 60 ? 'moderate' : 'fast'}`}>
                  {value < 40 ? '🚦 Slow' : value < 60 ? '🚗 Moderate' : '🏎️ Fast'}
                </span>
              </div>
            );
          })}
        </div>
      </section>

      {/* Model Information */}
      <section className="model-info">
        <h2>🤖 ML Model Information</h2>
        <div className="model-stats">
          <div className="model-stat">
            <span className="label">Model Type</span>
            <span className="value">Linear Regression</span>
          </div>
          <div className="model-stat">
            <span className="label">R² Score</span>
            <span className="value">{(predictions?.model_score * 100)?.toFixed(2)}%</span>
          </div>
          <div className="model-stat">
            <span className="label">Coefficient</span>
            <span className="value">{predictions?.coefficient}</span>
          </div>
          <div className="model-stat">
            <span className="label">Intercept</span>
            <span className="value">{predictions?.intercept?.toFixed(2)}</span>
          </div>
        </div>
      </section>

      {/* Historical vs Real-time Comparison */}
      <section className="comparison-section">
        <h2>📈 Historical vs Real-time Comparison</h2>
        <div className="comparison-cards">
          <div className="comparison-card historical">
            <h3>📜 Historical</h3>
            <div className="speed">{comparison?.historical?.avg_speed} km/h</div>
            <div className="sample">Based on {comparison?.historical?.sample_size?.toLocaleString()} records</div>
          </div>

          <div className="comparison-card arrow">
            <div className={`change ${comparison?.comparison?.speed_change > 0 ? 'positive' : 'negative'}`}>
              {comparison?.comparison?.speed_change > 0 ? '↑' : '↓'}
              {Math.abs(comparison?.comparison?.speed_change)} km/h
            </div>
            <div className="percent">({comparison?.comparison?.change_percent?.toFixed(1)}%)</div>
          </div>

          <div className="comparison-card realtime">
            <h3>📡 Real-time</h3>
            <div className="speed">{comparison?.realtime?.avg_speed} km/h</div>
            <div className="sample">Based on {comparison?.realtime?.sample_size?.toLocaleString()} records</div>
          </div>
        </div>

        <div className={`status-message ${comparison?.comparison?.speed_change < -5 ? 'warning' : 'normal'}`}>
          {comparison?.comparison?.status}
        </div>
      </section>

      <footer className="predictions-footer">
        <p>Predictions updated: {new Date().toLocaleTimeString()}</p>
        <p>Auto-refresh: Every 30 seconds</p>
      </footer>
    </div>
  );
}
