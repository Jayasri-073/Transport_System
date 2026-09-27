# 🚗 Smart City Transport System

A comprehensive real-time traffic monitoring and analysis system built with React and Flask. Features interactive dashboards, traffic predictions, and Power BI-style analytics.

![Dashboard Preview](frontend/src/logo.svg)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Running the App](#-running-the-app)
- [App Walkthrough](#-app-walkthrough)
- [API Endpoints](#-api-endpoints)
- [Admin Access](#-admin-access)
- [CSV Data Format](#-csv-data-format)

---

## ✨ Features

### 🏠 Home Page
- Welcome screen with system overview
- Quick navigation to all features
- Real-time status indicators

### 📊 Dashboard
- **KPI Cards**: Total Vehicles, Total Trips, Average Speed, Congestion Level
- **Peak Hours Analysis**: Morning and evening peak traffic identification
- **Hourly Traffic Chart**: Visual representation of traffic throughout the day
- **Route Congestion Status**: Color-coded severity for each route (A-E)
- **Congestion Hotspots**: Table showing high-traffic locations
- **Weekly Pattern Chart**: Traffic trends across the week
- Auto-refreshes every 30 seconds

### 🗺️ Map View
- Interactive map showing vehicle locations
- Real-time traffic visualization on routes
- Location markers with speed and route info

### 🔮 Predictions
- Machine Learning-based traffic speed predictions
- Linear Regression model trained on historical data
- Predictions for different hours of the day
- Model accuracy score display

### 📈 Reports
- Detailed traffic analysis reports
- Historical vs real-time data comparison
- Speed analysis by route
- Exportable data insights

### ⚠️ Alerts
- Real-time traffic alerts and warnings
- Congestion notifications
- Route-specific alerts with severity levels

### 📊 Power BI Dashboard
- **4 KPI Summary Cards**: Total Trips, Unique Vehicles, Avg Speed, Saturday Trips
- **Hourly Traffic Pattern**: Combined bar + line chart (8 PM highlighted)
- **Weekly Traffic Pattern**: Bar chart with Saturday peak highlighted
- **Route Traffic Volume**: Horizontal bar chart showing trips per route
- **Route Speed Analysis**: Average speed comparison across routes
- Interactive charts built with Recharts
- Refresh button for live data updates

### 👤 Admin Panel
- Secure admin login
- CSV data upload functionality
- Data validation and error handling
- Direct link to Power BI dashboard after upload

---

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| React 19 | UI Framework |
| React Router 7 | Navigation |
| Recharts | Power BI Charts |
| CSS3 | Styling (Dark Theme) |

### Backend
| Technology | Purpose |
|------------|---------|
| Flask | REST API Server |
| Pandas | Data Processing |
| scikit-learn | ML Predictions |
| Flask-CORS | Cross-Origin Requests |

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v16 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download](https://python.org/)
- **npm** (comes with Node.js)
- **pip** (comes with Python)

---

## 🚀 Installation

### Step 1: Clone/Download the Project

```bash
cd /path/to/Transport_System
```

### Step 2: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or install manually:
```bash
pip install flask flask-cors pandas scikit-learn
```

### Step 3: Install Frontend Dependencies

```bash
cd frontend
npm install
```

### Step 4: Fix macOS Quarantine (if needed)

If you downloaded the project and see "bad interpreter" errors:
```bash
cd frontend
xattr -rd com.apple.quarantine node_modules
```

---

## ▶️ Running the App

### Start Backend Server

```bash
cd backend
python3 app.py
```
Backend runs at: **http://localhost:5001**

### Start Frontend Server

Open a new terminal:
```bash
cd frontend
npm start
```
Frontend runs at: **http://localhost:3000**

### Access the App

Open your browser and go to: **http://localhost:3000**

---

## 📱 App Walkthrough

### Navigation Bar
The navbar contains links to all features:
- 🏠 Home
- 📊 Dashboard  
- 🗺️ Map View
- 🔮 Predictions
- 📈 Reports
- ⚠️ Alerts
- 📊 Power BI (purple button)
- 👤 Admin (red button)

### Using the Dashboard
1. Navigate to **Dashboard** from navbar
2. View real-time KPIs at the top
3. Check peak hours analysis
4. Review route congestion status
5. Examine congestion hotspots table
6. Data auto-refreshes every 30 seconds

### Using Power BI Dashboard
1. Click **"📊 Power BI"** in the navbar
2. View 4 KPI summary cards
3. Analyze hourly traffic patterns (8 PM highlighted)
4. Check weekly patterns (Saturday peak highlighted)
5. Compare route traffic volumes
6. Click **"🔄 Refresh Data"** to update

### Uploading New Data
1. Go to **Admin** → Login with credentials
2. Click **"Upload Data"**
3. Select a CSV file (must have required columns)
4. Click **"🚀 Upload CSV"**
5. After success, click **"📊 View Power BI Dashboard"**

### Viewing Predictions
1. Navigate to **Predictions**
2. View ML model predictions for different hours
3. Check model accuracy score
4. See current hour prediction

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info and available routes |
| `/api/dashboard` | GET | Main dashboard metrics |
| `/api/peak-hours` | GET | Peak traffic hours analysis |
| `/api/congestion` | GET | Congestion hotspots and routes |
| `/api/trends/daily` | GET | Daily traffic trends |
| `/api/trends/weekly` | GET | Weekly traffic trends |
| `/api/speed-analysis` | GET | Detailed speed metrics |
| `/api/alerts` | GET | Traffic alerts |
| `/api/historical-vs-realtime` | GET | Compare historical and live data |
| `/api/mapview` | GET | Vehicle locations for map |
| `/api/predict` | GET | Traffic prediction using ML |
| `/api/realtime-simulation` | GET | Simulate real-time traffic |
| `/api/powerbi-data` | GET | Power BI dashboard data |
| `/api/upload-csv` | POST | Upload new CSV data file |

---

## 🔐 Admin Access

| Field | Value |
|-------|-------|
| **Username** | Value of `ADMIN_USERNAME` on the server |
| **Password** | Value of `ADMIN_PASSWORD` on the server |

> Set `ADMIN_USERNAME`, `ADMIN_PASSWORD`, and a strong `ADMIN_TOKEN_SECRET` as Render environment variables. Admin login and CSV uploads are unavailable until all three are configured.

---

## 📄 CSV Data Format

When uploading CSV files, ensure they have these **required columns**:

| Column | Type | Description |
|--------|------|-------------|
| `vehicle_id` | String | Unique vehicle identifier (e.g., V1234) |
| `route` | String | Route name (e.g., Route-A, Route-B) |
| `speed_kmph` | Float | Speed in km/h |
| `timestamp` | DateTime | Timestamp (YYYY-MM-DD HH:MM:SS) |
| `latitude` | Float | Latitude between -90 and 90 |
| `longitude` | Float | Longitude between -180 and 180 |

### Sample CSV Format:
```csv
vehicle_id,route,speed_kmph,timestamp,latitude,longitude
V1234,Route-A,45.5,2026-01-18 14:30:00,12.9716,77.5946
V5678,Route-B,62.3,2026-01-18 14:31:00,12.9352,77.6245
```

---

## 📁 Project Structure

```
Transport_System/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── analysis.py            # Data analysis functions
│   ├── visualizations.py      # Chart generation
│   ├── powerbi_visualizations.py  # Power BI charts
│   ├── requirements.txt       # Python dependencies
│   └── uploads/               # Uploaded CSV files
├── frontend/
│   ├── src/
│   │   ├── Components/        # React components
│   │   │   ├── Dashboard.js
│   │   │   ├── MapView.js
│   │   │   ├── Predictions.js
│   │   │   ├── Reports.js
│   │   │   ├── Alerts.js
│   │   │   ├── PowerBIDashboard.js
│   │   │   └── *.css
│   │   ├── AdminPanel/        # Admin components
│   │   │   ├── AdminLogin.js
│   │   │   ├── AdminDashboard.js
│   │   │   └── AdminUpload.js
│   │   ├── services/
│   │   │   └── api.js         # API service functions
│   │   ├── App.js             # Main app component
│   │   └── App.css            # Global styles
│   └── package.json
└── vehicle_route_speed_dataset_5000.csv  # Sample data
```

---

## 🎨 Color Scheme

The app uses a modern dark theme:
- **Background**: Dark navy (#1a1a2e)
- **Primary**: Teal (#4ecdc4)
- **Success**: Green (#00B294)
- **Warning**: Yellow (#F2C80F)
- **Danger**: Red (#E81123)
- **Highlight**: Orange (#FF8C00)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📝 License

This project is for educational purposes.

---

## 🆘 Troubleshooting

### "bad interpreter: Operation not permitted" error
```bash
cd frontend
xattr -rd com.apple.quarantine node_modules
```

### Backend connection error
Make sure the Flask server is running on port 5001:
```bash
cd backend
python3 app.py
```

### Port already in use
Kill the process using the port:
```bash
lsof -ti:5001 | xargs kill -9  # For backend
lsof -ti:3000 | xargs kill -9  # For frontend
```

---

Made with ❤️ for Smart City Traffic Management
