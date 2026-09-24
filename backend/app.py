"""
Smart City Transport System - Flask API Server
Provides REST endpoints for traffic analysis and visualization
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from analysis import (
    dashboard_data, 
    congestion_data, 
    map_data, 
    get_peak_hours,
    get_daily_trends,
    get_weekly_trends,
    get_speed_analysis,
    generate_alerts,
    historical_vs_realtime
)
import pandas as pd
from datetime import datetime


app = Flask(__name__)
# Enable CORS for React frontend - allow all origins for development
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})


@app.route("/")
def home():
    """API home endpoint with available routes."""
    return jsonify({
        "message": "Smart City Transport System API",
        "version": "1.0",
        "endpoints": [
            "/dashboard - Main dashboard metrics",
            "/api/peak-hours - Peak traffic hours analysis",
            "/api/congestion - Congestion hotspots and routes",
            "/api/trends/daily - Daily traffic trends",
            "/api/trends/weekly - Weekly traffic trends",
            "/api/speed-analysis - Detailed speed metrics",
            "/api/alerts - Traffic alerts",
            "/api/historical-vs-realtime - Compare historical and live data",
            "/mapview - Vehicle locations for map",
            "/predict - Traffic prediction"
        ],
        "timestamp": datetime.now().isoformat()
    })


@app.route("/dashboard")
def dashboard():
    """Main dashboard metrics endpoint."""
    try:
        data = dashboard_data()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/peak-hours")
def peak_hours():
    """Peak traffic hours analysis."""
    try:
        data = get_peak_hours()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/congestion")
def congestion():
    """Congestion analysis with hotspots."""
    try:
        data = congestion_data()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/trends/daily")
def daily_trends():
    """Daily traffic trends."""
    try:
        data = get_daily_trends()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/trends/weekly")
def weekly_trends():
    """Weekly traffic trends."""
    try:
        data = get_weekly_trends()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/speed-analysis")
def speed_analysis():
    """Detailed speed analysis."""
    try:
        data = get_speed_analysis()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/alerts")
def alerts():
    """Traffic alerts endpoint."""
    try:
        data = generate_alerts()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/historical-vs-realtime")
def historical_realtime():
    """Compare historical and real-time data."""
    try:
        data = historical_vs_realtime()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/mapview")
def mapview():
    """Vehicle locations for map visualization."""
    try:
        data = map_data()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/predict")
def predict():
    """Traffic speed prediction using ML."""
    try:
        from sklearn.linear_model import LinearRegression
        df = pd.read_csv("../vehicle_route_speed_dataset_5000.csv")
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        
        X = df[["hour"]]
        y = df["speed_kmph"]
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict for different hours
        predictions = {}
        for hour in [8, 12, 17, 19, 22]:
            pred = model.predict([[hour]])[0]
            predictions[f"hour_{hour}"] = round(pred, 2)
        
        # Get current hour prediction
        current_hour = datetime.now().hour
        current_prediction = model.predict([[current_hour]])[0]
        
        return jsonify({
            "success": True,
            "data": {
                "predictions_by_hour": predictions,
                "current_hour": current_hour,
                "current_prediction": round(current_prediction, 2),
                "model_score": round(model.score(X, y), 4),
                "coefficient": round(model.coef_[0], 4),
                "intercept": round(model.intercept_, 4)
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/realtime-simulation")
def realtime_simulation():
    """Simulate real-time traffic data stream."""
    import random
    from datetime import datetime
    
    routes = ['Route-A', 'Route-B', 'Route-C', 'Route-D', 'Route-E']
    current_hour = datetime.now().hour
    
    # Simulate based on time of day
    if 8 <= current_hour <= 10 or 17 <= current_hour <= 20:
        base_speed = 25  # Rush hour - slower
        congestion = "High"
    elif 22 <= current_hour or current_hour <= 6:
        base_speed = 70  # Night - faster
        congestion = "Low"
    else:
        base_speed = 50  # Normal
        congestion = "Medium"
    
    vehicles = []
    for i in range(20):
        vehicles.append({
            "vehicle_id": f"V{random.randint(1000, 9999)}",
            "route": random.choice(routes),
            "speed_kmph": round(base_speed + random.uniform(-15, 15), 2),
            "latitude": round(12.9 + random.uniform(0, 0.3), 6),
            "longitude": round(77.5 + random.uniform(0, 0.2), 6),
            "timestamp": datetime.now().isoformat()
        })
    
    return jsonify({
        "success": True,
        "data": {
            "vehicles": vehicles,
            "current_congestion": congestion,
            "timestamp": datetime.now().isoformat(),
            "simulation": True
        }
    })

# Store the current CSV file path
CURRENT_CSV_FILE = "../vehicle_route_speed_dataset_5000.csv"
UPLOAD_FOLDER = "uploads"

import os
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/api/upload-csv", methods=["POST"])
def upload_csv():
    """Handle CSV file upload."""
    global CURRENT_CSV_FILE
    
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({"success": False, "error": "File must be a CSV"}), 400
    
    try:
        # Save the file
        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Validate CSV has required columns
        df = pd.read_csv(filepath)
        required_columns = ['vehicle_id', 'route', 'speed_kmph', 'timestamp']
        missing = [col for col in required_columns if col not in df.columns]
        
        if missing:
            os.remove(filepath)
            return jsonify({
                "success": False, 
                "error": f"Missing required columns: {', '.join(missing)}"
            }), 400
        
        CURRENT_CSV_FILE = filepath
        
        return jsonify({
            "success": True,
            "message": f"File '{filename}' uploaded successfully",
            "rows": len(df),
            "columns": list(df.columns)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/powerbi-data")
def powerbi_data():
    """Get Power BI dashboard data for frontend charts."""
    try:
        df = pd.read_csv(CURRENT_CSV_FILE)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['day_name'] = df['timestamp'].dt.day_name()
        
        # KPI data
        kpis = {
            "total_trips": len(df),
            "total_vehicles": df['vehicle_id'].nunique(),
            "avg_speed": round(df['speed_kmph'].mean(), 1),
            "saturday_trips": len(df[df['day_name'] == 'Saturday'])
        }
        
        # Hourly data
        hourly = df.groupby('hour').agg({
            'vehicle_id': 'count',
            'speed_kmph': 'mean'
        }).reset_index()
        hourly.columns = ['hour', 'trips', 'avg_speed']
        hourly['avg_speed'] = hourly['avg_speed'].round(1)
        hourly_data = hourly.to_dict('records')
        
        # Weekly data
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily = df.groupby('day_name').agg({
            'vehicle_id': 'count',
            'speed_kmph': 'mean'
        }).reset_index()
        daily.columns = ['day', 'trips', 'avg_speed']
        daily['day'] = pd.Categorical(daily['day'], categories=day_order, ordered=True)
        daily = daily.sort_values('day')
        daily['avg_speed'] = daily['avg_speed'].round(1)
        weekly_data = daily.to_dict('records')
        
        # Route data
        route_data = df.groupby('route').agg({
            'vehicle_id': 'count',
            'speed_kmph': 'mean'
        }).reset_index()
        route_data.columns = ['route', 'trips', 'avg_speed']
        route_data['avg_speed'] = route_data['avg_speed'].round(1)
        route_data = route_data.sort_values('trips', ascending=False)
        routes_data = route_data.to_dict('records')
        
        return jsonify({
            "success": True,
            "data": {
                "kpis": kpis,
                "hourly": hourly_data,
                "weekly": weekly_data,
                "routes": routes_data
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    print("Starting Smart City Transport System API...")
    print("Available at: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)

