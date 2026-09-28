# Deployment Guide - Smart City Transport System

This guide outlines the production deployment setup for the Smart City Transport System application, using **Vercel** for the React frontend and **Render** for the Flask Python backend.

---

## Architecture Overview

```
               +----------------------------------+
               |          Vercel Platform         |
               |     React Single Page App        |
               |  (https://transport-system-nu    |
               |          .vercel.app)            |
               +----------------------------------+
                                |
                                | HTTP REST API / JSON
                                v
               +----------------------------------+
               |          Render Platform         |
               |       Python / Flask API         |
               |  (https://transport-system-p5jz  |
               |           .onrender.com)         |
               +----------------------------------+
```

---

## Part A: Deploy React Frontend to Vercel

1. Log in to [Vercel](https://vercel.com) and click **Add New... → Project**.
2. Import the GitHub repository: `https://github.com/Jayasri-073/Transport_System`.
3. Configure project settings:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install`
4. Expand **Environment Variables** and add:
   - **Key**: `REACT_APP_API_URL`
   - **Value**: `https://transport-system-p5jz.onrender.com`
5. Click **Deploy**.

---

## Part B: Deploy Flask Backend to Render

1. Log in to [Render](https://dashboard.render.com) and click **New + → Web Service**.
2. Connect the GitHub repository: `https://github.com/Jayasri-073/Transport_System`.
3. Configure service settings:
   - **Name**: `transport-system-p5jz`
   - **Region**: Select your preferred region
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Expand **Advanced → Environment Variables** and add:
   - `ADMIN_USERNAME` = `<your-chosen-admin-username>`
   - `ADMIN_PASSWORD` = `<your-chosen-admin-password>`
   - `ADMIN_TOKEN_SECRET` = `<a-secure-random-secret-key>`
   - `CORS_ORIGINS` = `https://transport-system-nu.vercel.app,https://transport-system-cgshok610-transport-system.vercel.app`
5. Click **Create Web Service**.

---

## Part C: Environment Variables Reference

### Backend Environment Variables (Render)

| Variable | Description | Example |
| :--- | :--- | :--- |
| `ADMIN_USERNAME` | Username required for admin login | `admin` |
| `ADMIN_PASSWORD` | Password required for admin login | `SecurePass123!` |
| `ADMIN_TOKEN_SECRET` | Secret key used to sign JWT authentication tokens | `a7d8e9f...` |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend URLs | `https://transport-system-nu.vercel.app` |
| `PORT` | Set automatically by Render (default 5001) | `10000` |

### Frontend Environment Variables (Vercel)

| Variable | Description | Example |
| :--- | :--- | :--- |
| `REACT_APP_API_URL` | Base URL of the backend Flask API (no trailing slash) | `https://transport-system-p5jz.onrender.com` |

---

## Part D: Local Development Setup

### Backend (Local)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Backend runs locally at: `http://localhost:5001`

### Frontend (Local)
```bash
cd frontend
npm install
npm start
```
Frontend runs locally at: `http://localhost:3000`

---

## Part E: Deployment Smoke Test Checklist

After deploying to Vercel and Render, verify all steps:

1. **Backend Health Check**: Open `https://transport-system-p5jz.onrender.com/api/health` in your browser. Expected response: `{"status": "ok"}`.
2. **Frontend Loading**: Open `https://transport-system-nu.vercel.app`. Verify that the main homepage loads cleanly.
3. **Dashboard Data**: Navigate to `/dashboard` and check that metrics, peak hours, and congestion charts populate without errors.
4. **Map View**: Open `/mapview` and check that vehicle positions render.
5. **Predictions**: Open `/predictions` and verify machine learning prediction values.
6. **Reports & Alerts**: Open `/reports` and `/alerts` to ensure analytics load.
7. **Power BI Dashboard**: Open `/powerbi` and verify all KPI cards and charts load.
8. **Admin Login**:
   - Go to `/admin`.
   - Enter your configured `ADMIN_USERNAME` and `ADMIN_PASSWORD`.
   - Click **Login**.
   - Verify redirection to `/admin/dashboard`.
9. **CSV Dataset Upload**:
   - Go to `/admin/upload`.
   - Select a valid CSV file (e.g. `vehicle_route_speed_dataset_5000.csv`).
   - Click **Upload CSV**.
   - Verify success message with uploaded row count.
10. **Direct SPA Route Refresh**: Refresh your browser on `/admin/dashboard` or `/predictions` to verify that Vercel SPA rewrites handle direct page loads without returning a 404.
