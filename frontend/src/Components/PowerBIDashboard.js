import React, { useState, useEffect } from 'react';
import { getPowerBIData } from '../services/api';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
    ResponsiveContainer, Cell, Line, ComposedChart
} from 'recharts';
import './PowerBIDashboard.css';

// Power BI Color Palette
const COLORS = {
    primary: '#118DFF',
    secondary: '#12239E',
    success: '#00B294',
    warning: '#F2C80F',
    danger: '#E81123',
    highlight: '#FF8C00',
    purple: '#8764B8',
    teal: '#00B7C3',
};

const ROUTE_COLORS = {
    'Route-A': '#118DFF',
    'Route-B': '#12239E',
    'Route-C': '#00B294',
    'Route-D': '#F2C80F',
    'Route-E': '#E81123'
};

const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
        return (
            <div className="custom-tooltip">
                <p className="label">{label}</p>
                {payload.map((entry, index) => (
                    <p key={index} style={{ color: entry.color }}>
                        {entry.name}: {entry.value.toLocaleString()}
                        {entry.name === 'avg_speed' ? ' km/h' : ''}
                    </p>
                ))}
            </div>
        );
    }
    return null;
};

export default function PowerBIDashboard() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [lastUpdated, setLastUpdated] = useState(null);

    const fetchData = async () => {
        try {
            setLoading(true);
            const response = await getPowerBIData();
            if (response.success) {
                setData(response.data);
                setLastUpdated(new Date());
                setError(null);
            } else {
                setError(response.error || 'Failed to fetch data');
            }
        } catch (err) {
            setError('Failed to connect to server. Is the backend running?');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="powerbi-dashboard powerbi-loading">
                <div className="loader"></div>
                <p>Loading Power BI Dashboard...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="powerbi-dashboard">
                <div className="powerbi-error">
                    <h2>⚠️ Error</h2>
                    <p>{error}</p>
                    <button onClick={fetchData}>Retry</button>
                </div>
            </div>
        );
    }

    const { kpis, hourly, weekly, routes } = data;

    return (
        <div className="powerbi-dashboard">
            <header className="powerbi-header">
                <h1>📊 Power BI Traffic Dashboard</h1>
                <p className="subtitle">Interactive Traffic Analysis & Insights</p>
            </header>

            <button className="refresh-btn" onClick={fetchData}>
                🔄 Refresh Data
            </button>

            {/* KPI Cards */}
            <section className="kpi-grid">
                <div className="kpi-card trips">
                    <span className="kpi-icon">📍</span>
                    <span className="kpi-value">{kpis.total_trips.toLocaleString()}</span>
                    <span className="kpi-label">Total Trips</span>
                </div>
                <div className="kpi-card vehicles">
                    <span className="kpi-icon">🚗</span>
                    <span className="kpi-value">{kpis.total_vehicles.toLocaleString()}</span>
                    <span className="kpi-label">Unique Vehicles</span>
                </div>
                <div className="kpi-card speed">
                    <span className="kpi-icon">⚡</span>
                    <span className="kpi-value">{kpis.avg_speed} <small>km/h</small></span>
                    <span className="kpi-label">Average Speed</span>
                </div>
                <div className="kpi-card saturday">
                    <span className="kpi-icon">📅</span>
                    <span className="kpi-value">{kpis.saturday_trips.toLocaleString()}</span>
                    <span className="kpi-label">Saturday Trips</span>
                </div>
            </section>

            {/* Charts Grid */}
            <section className="charts-grid">
                {/* Hourly Traffic Chart */}
                <div className="chart-card">
                    <h3><span className="chart-icon">⏰</span> Hourly Traffic Pattern</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <ComposedChart data={hourly}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                            <XAxis
                                dataKey="hour"
                                stroke="#888"
                                tickFormatter={(h) => `${h}:00`}
                            />
                            <YAxis yAxisId="left" stroke={COLORS.primary} />
                            <YAxis yAxisId="right" orientation="right" stroke={COLORS.danger} />
                            <Tooltip content={<CustomTooltip />} />
                            <Bar yAxisId="left" dataKey="trips" name="Trips" radius={[4, 4, 0, 0]}>
                                {hourly.map((entry, index) => (
                                    <Cell
                                        key={`cell-${index}`}
                                        fill={entry.hour === 20 ? COLORS.highlight : COLORS.primary}
                                    />
                                ))}
                            </Bar>
                            <Line
                                yAxisId="right"
                                type="monotone"
                                dataKey="avg_speed"
                                name="Avg Speed"
                                stroke={COLORS.danger}
                                strokeWidth={2}
                                dot={{ fill: '#fff', strokeWidth: 2 }}
                            />
                        </ComposedChart>
                    </ResponsiveContainer>
                    <div className="chart-legend">
                        <span className="legend-item">
                            <span className="legend-color" style={{ background: COLORS.primary }}></span>
                            Regular Hours
                        </span>
                        <span className="legend-item">
                            <span className="legend-color" style={{ background: COLORS.highlight }}></span>
                            8 PM Peak
                        </span>
                        <span className="legend-item">
                            <span className="legend-color" style={{ background: COLORS.danger }}></span>
                            Avg Speed
                        </span>
                    </div>
                </div>

                {/* Weekly Pattern Chart */}
                <div className="chart-card">
                    <h3><span className="chart-icon">📅</span> Weekly Traffic Pattern</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={weekly}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                            <XAxis
                                dataKey="day"
                                stroke="#888"
                                tickFormatter={(d) => d.slice(0, 3)}
                            />
                            <YAxis stroke={COLORS.teal} />
                            <Tooltip content={<CustomTooltip />} />
                            <Bar dataKey="trips" name="Trips" radius={[4, 4, 0, 0]}>
                                {weekly.map((entry, index) => (
                                    <Cell
                                        key={`cell-${index}`}
                                        fill={entry.day === 'Saturday' ? COLORS.highlight : COLORS.teal}
                                    />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                    <div className="chart-legend">
                        <span className="legend-item">
                            <span className="legend-color" style={{ background: COLORS.teal }}></span>
                            Regular Days
                        </span>
                        <span className="legend-item">
                            <span className="legend-color" style={{ background: COLORS.highlight }}></span>
                            Saturday (Peak)
                        </span>
                    </div>
                </div>

                {/* Route Traffic Volume */}
                <div className="chart-card">
                    <h3><span className="chart-icon">🛣️</span> Route Traffic Volume</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={routes} layout="vertical">
                            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                            <XAxis type="number" stroke="#888" />
                            <YAxis dataKey="route" type="category" stroke="#888" width={80} />
                            <Tooltip content={<CustomTooltip />} />
                            <Bar dataKey="trips" name="Trips" radius={[0, 4, 4, 0]}>
                                {routes.map((entry, index) => (
                                    <Cell
                                        key={`cell-${index}`}
                                        fill={ROUTE_COLORS[entry.route] || COLORS.primary}
                                    />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* Route Speed Analysis */}
                <div className="chart-card">
                    <h3><span className="chart-icon">⚡</span> Average Speed by Route</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={routes} layout="vertical">
                            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                            <XAxis type="number" stroke="#888" unit=" km/h" />
                            <YAxis dataKey="route" type="category" stroke="#888" width={80} />
                            <Tooltip content={<CustomTooltip />} />
                            <Bar dataKey="avg_speed" name="Avg Speed" radius={[0, 4, 4, 0]}>
                                {routes.map((entry, index) => (
                                    <Cell
                                        key={`cell-${index}`}
                                        fill={ROUTE_COLORS[entry.route] || COLORS.primary}
                                    />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </section>

            {lastUpdated && (
                <p className="last-updated">
                    Last updated: {lastUpdated.toLocaleTimeString()}
                </p>
            )}
        </div>
    );
}
