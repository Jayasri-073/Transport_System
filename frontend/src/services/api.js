const configuredBaseUrl = process.env.REACT_APP_API_URL;
const API_BASE_URL = (configuredBaseUrl || (process.env.NODE_ENV === 'development' ? 'http://localhost:5001' : '')).replace(/\/$/, '');

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.error || `Request failed (${response.status})`);
  }
  return payload;
}

function fetchAPI(endpoint) {
  return request(endpoint);
}

export const getDashboardData = () => fetchAPI('/api/dashboard');
export const getPeakHours = () => fetchAPI('/api/peak-hours');
export const getCongestionData = () => fetchAPI('/api/congestion');
export const getDailyTrends = () => fetchAPI('/api/trends/daily');
export const getWeeklyTrends = () => fetchAPI('/api/trends/weekly');
export const getSpeedAnalysis = () => fetchAPI('/api/speed-analysis');
export const getAlerts = () => fetchAPI('/api/alerts');
export const getHistoricalVsRealtime = () => fetchAPI('/api/historical-vs-realtime');
export const getMapData = () => fetchAPI('/api/mapview');
export const getPredictions = () => fetchAPI('/api/predict');
export const getRealtimeSimulation = () => fetchAPI('/api/realtime-simulation');
export const getPowerBIData = () => fetchAPI('/api/powerbi-data');

export async function loginAdmin(username, password) {
  return request('/api/admin/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
}

export async function uploadCSV(file, token) {
  const formData = new FormData();
  formData.append('file', file);
  return request('/api/upload-csv', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: formData,
  });
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
  loginAdmin,
  uploadCSV,
};

export default apiService;
