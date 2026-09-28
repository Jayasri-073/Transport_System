const DEFAULT_API_BASE_URL = process.env.NODE_ENV === 'development'
  ? 'http://localhost:5001'
  : 'https://transport-system-p5jz.onrender.com';
const rawApiUrl = process.env.REACT_APP_API_URL;
const validApiUrl = rawApiUrl && rawApiUrl !== 'undefined' && rawApiUrl !== 'null' && rawApiUrl.trim() !== ''
  ? rawApiUrl.trim()
  : DEFAULT_API_BASE_URL;
export const API_BASE_URL = validApiUrl.replace(/\/$/, '');

export class ApiRequestError extends Error {
  constructor(status, message) {
    super(message);
    this.name = 'ApiRequestError';
    this.status = status;
  }
}

async function request(endpoint, options = {}) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${endpoint}`, options);
  } catch (_error) {
    throw new ApiRequestError(0, 'Unable to reach the transport server. Check your connection and the API URL.');
  }
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const messages = {
      401: 'Incorrect username or password.',
      403: 'You do not have permission to perform this action.',
      404: 'The requested API endpoint was not found.',
      405: 'The login API endpoint does not accept this request method. Check the production API configuration.',
      500: 'The transport server encountered an error. Please try again shortly.',
    };
    throw new ApiRequestError(response.status, payload.error || messages[response.status] || `Request failed (${response.status})`);
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
