/**
 * API Service for Smart City Transport System
 * Handles all backend API calls
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

/**
 * Generic fetch wrapper with error handling
 */
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`API Error (${endpoint}):`, error);
        throw error;
    }
}

// Dashboard API
export async function getDashboardData() {
    return fetchAPI('/dashboard');
}

// Peak Hours API
export async function getPeakHours() {
    return fetchAPI('/api/peak-hours');
}

// Congestion API
export async function getCongestionData() {
    return fetchAPI('/api/congestion');
}

// Daily Trends API
export async function getDailyTrends() {
    return fetchAPI('/api/trends/daily');
}

// Weekly Trends API
export async function getWeeklyTrends() {
    return fetchAPI('/api/trends/weekly');
}

// Speed Analysis API
export async function getSpeedAnalysis() {
    return fetchAPI('/api/speed-analysis');
}

// Alerts API
export async function getAlerts() {
    return fetchAPI('/api/alerts');
}

// Historical vs Realtime API
export async function getHistoricalVsRealtime() {
    return fetchAPI('/api/historical-vs-realtime');
}

// Map Data API
export async function getMapData() {
    return fetchAPI('/mapview');
}

// Predictions API
export async function getPredictions() {
    return fetchAPI('/predict');
}

// Real-time Simulation API
export async function getRealtimeSimulation() {
    return fetchAPI('/api/realtime-simulation');
}

// Power BI Data API
export async function getPowerBIData() {
    return fetchAPI('/api/powerbi-data');
}

// CSV Upload API
export async function uploadCSV(file) {
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE_URL}/api/upload-csv`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('CSV Upload Error:', error);
        throw error;
    }
}

const apiService = {
    getDashboardData,
    getPeakHours,
    getCongestionData,
    getDailyTrends,
    getWeeklyTrends,
    getSpeedAnalysis,
    getAlerts,
    getHistoricalVsRealtime,
    getMapData,
    getPredictions,
    getRealtimeSimulation,
    getPowerBIData,
    uploadCSV
};

export default apiService;
