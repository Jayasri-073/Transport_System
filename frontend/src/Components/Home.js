import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

export default function Home() {
  return (
    <div className="home-page">
      <section className="hero">
        <div className="hero-content">
          <h1>🚗 Smart City Transport System</h1>
          <p className="tagline">Real-time Traffic Monitoring & Big Data Analytics</p>
          <p className="description">
            An intelligent traffic management system powered by Python, Apache Spark,
            and Machine Learning for smarter urban mobility.
          </p>
          <div className="cta-buttons">
            <Link to="/dashboard" className="btn primary">View Dashboard</Link>
            <Link to="/alerts" className="btn secondary">Live Alerts</Link>
          </div>
        </div>
      </section>

      <section className="features">
        <h2>🌟 Key Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Real-time Analytics</h3>
            <p>Monitor traffic patterns, congestion levels, and vehicle speeds in real-time.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔮</div>
            <h3>ML Predictions</h3>
            <p>Machine learning powered traffic predictions for better route planning.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🗺️</div>
            <h3>Live Map View</h3>
            <p>Visualize vehicle locations and congestion hotspots on an interactive map.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🚨</div>
            <h3>Smart Alerts</h3>
            <p>Automatic detection of traffic jams and delay warnings.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📈</div>
            <h3>Trend Analysis</h3>
            <p>Daily and weekly traffic pattern analysis with historical data.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Big Data Processing</h3>
            <p>Apache Spark powered batch processing for large-scale analysis.</p>
          </div>
        </div>
      </section>

      <section className="tech-stack">
        <h2>🛠️ Technology Stack</h2>
        <div className="tech-grid">
          <div className="tech-item">
            <span className="tech-name">Python</span>
            <span className="tech-desc">Backend & Analysis</span>
          </div>
          <div className="tech-item">
            <span className="tech-name">Flask</span>
            <span className="tech-desc">REST API</span>
          </div>
          <div className="tech-item">
            <span className="tech-name">React</span>
            <span className="tech-desc">Frontend UI</span>
          </div>
          <div className="tech-item">
            <span className="tech-name">PySpark</span>
            <span className="tech-desc">Big Data</span>
          </div>
          <div className="tech-item">
            <span className="tech-name">Matplotlib</span>
            <span className="tech-desc">Visualization</span>
          </div>
          <div className="tech-item">
            <span className="tech-name">Scikit-learn</span>
            <span className="tech-desc">ML Models</span>
          </div>
        </div>
      </section>

      <section className="quick-links">
        <h2>🔗 Quick Navigation</h2>
        <div className="links-grid">
          <Link to="/dashboard" className="quick-link">
            <span className="icon">📊</span>
            <span className="text">Dashboard</span>
          </Link>
          <Link to="/mapview" className="quick-link">
            <span className="icon">🗺️</span>
            <span className="text">Map View</span>
          </Link>
          <Link to="/predictions" className="quick-link">
            <span className="icon">🔮</span>
            <span className="text">Predictions</span>
          </Link>
          <Link to="/reports" className="quick-link">
            <span className="icon">📈</span>
            <span className="text">Reports</span>
          </Link>
          <Link to="/alerts" className="quick-link">
            <span className="icon">🚨</span>
            <span className="text">Alerts</span>
          </Link>
          <Link to="/admin" className="quick-link">
            <span className="icon">⚙️</span>
            <span className="text">Admin</span>
          </Link>
        </div>
      </section>

      <footer className="home-footer">
        <p>Smart City Transport System - IETE Project</p>
        <p>Built with ❤️ using Python, React & Big Data Technologies</p>
      </footer>
    </div>
  );
}
