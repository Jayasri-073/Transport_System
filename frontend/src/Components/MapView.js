import React, { useState, useEffect } from 'react';
import { getMapData } from '../services/api';
import './MapView.css';

export default function MapView() {
  const [mapData, setMapData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedRoute, setSelectedRoute] = useState('all');

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getMapData();
        setMapData(data.data);
      } catch (err) {
        console.error('Failed to fetch map data:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="mapview-page loading">
        <div className="loader"></div>
        <p>Loading map data...</p>
      </div>
    );
  }

  const filteredVehicles = selectedRoute === 'all'
    ? mapData?.vehicles
    : mapData?.vehicles?.filter(v => v.route === selectedRoute);

  const routes = [...new Set(mapData?.vehicles?.map(v => v.route))];

  return (
    <div className="mapview-page">
      <header className="page-header">
        <h1>🗺️ Live Map View</h1>
        <p>Real-time vehicle locations</p>
      </header>

      {/* Map Stats */}
      <section className="map-stats">
        <div className="stat-card">
          <span className="value">{mapData?.total_vehicles}</span>
          <span className="label">Total Vehicles</span>
        </div>
        <div className="stat-card">
          <span className="value">{filteredVehicles?.length}</span>
          <span className="label">Showing</span>
        </div>
        <div className="stat-card">
          <span className="value">{mapData?.center?.lat?.toFixed(2)}°</span>
          <span className="label">Center Lat</span>
        </div>
        <div className="stat-card">
          <span className="value">{mapData?.center?.lng?.toFixed(2)}°</span>
          <span className="label">Center Lng</span>
        </div>
      </section>

      {/* Route Filter */}
      <section className="route-filter">
        <label>Filter by Route:</label>
        <select value={selectedRoute} onChange={(e) => setSelectedRoute(e.target.value)}>
          <option value="all">All Routes</option>
          {routes.map(route => (
            <option key={route} value={route}>{route}</option>
          ))}
        </select>
      </section>

      {/* Map Visualization */}
      <section className="map-container">
        <div className="map-placeholder">
          <div className="map-grid">
            {filteredVehicles?.map((vehicle, idx) => {
              const x = ((vehicle.lng - (mapData?.center?.lng - 0.2)) / 0.4) * 100;
              const y = ((mapData?.center?.lat + 0.2 - vehicle.lat) / 0.4) * 100;
              return (
                <div
                  key={idx}
                  className={`vehicle-marker ${vehicle.speed < 30 ? 'slow' : vehicle.speed < 60 ? 'medium' : 'fast'}`}
                  style={{
                    left: `${Math.min(Math.max(x, 5), 95)}%`,
                    top: `${Math.min(Math.max(y, 5), 95)}%`
                  }}
                  title={`${vehicle.id} - ${vehicle.route} - ${vehicle.speed} km/h`}
                >
                  <span className="marker-dot"></span>
                  <span className="marker-label">{vehicle.id}</span>
                </div>
              );
            })}
          </div>
          <div className="map-overlay">
            <p>📍 Interactive map visualization</p>
            <p className="note">Vehicle positions are relative to data center point</p>
          </div>
        </div>
      </section>

      {/* Legend */}
      <section className="map-legend">
        <h3>Speed Legend</h3>
        <div className="legend-items">
          <div className="legend-item">
            <span className="dot fast"></span>
            <span>&gt; 60 km/h (Fast)</span>
          </div>
          <div className="legend-item">
            <span className="dot medium"></span>
            <span>30-60 km/h (Moderate)</span>
          </div>
          <div className="legend-item">
            <span className="dot slow"></span>
            <span>&lt; 30 km/h (Slow)</span>
          </div>
        </div>
      </section>

      {/* Vehicle List */}
      <section className="vehicle-list">
        <h2>🚗 Vehicle List</h2>
        <div className="vehicle-table">
          <table>
            <thead>
              <tr>
                <th>Vehicle ID</th>
                <th>Route</th>
                <th>Speed</th>
                <th>Latitude</th>
                <th>Longitude</th>
              </tr>
            </thead>
            <tbody>
              {filteredVehicles?.slice(0, 20).map((vehicle, idx) => (
                <tr key={idx} className={vehicle.speed < 30 ? 'slow' : ''}>
                  <td>{vehicle.id}</td>
                  <td><span className="route-badge">{vehicle.route}</span></td>
                  <td>
                    <span className={`speed-value ${vehicle.speed < 30 ? 'slow' : vehicle.speed > 60 ? 'fast' : ''}`}>
                      {vehicle.speed} km/h
                    </span>
                  </td>
                  <td>{vehicle.lat?.toFixed(4)}°</td>
                  <td>{vehicle.lng?.toFixed(4)}°</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
