"""Smart City Transport System Flask application."""

from __future__ import annotations

import hmac
import logging
import os
import random
from datetime import datetime
from functools import wraps
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from analysis import (
    congestion_data,
    dashboard_data,
    generate_alerts,
    get_daily_trends,
    get_peak_hours,
    get_speed_analysis,
    get_weekly_trends,
    historical_vs_realtime,
    map_data,
    set_data_filepath,
)


ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
BUILD_DIR = ROOT_DIR / "frontend" / "build"
DEFAULT_DATA_FILE = ROOT_DIR / "vehicle_route_speed_dataset_5000.csv"
UPLOAD_FOLDER = Path(os.environ.get("DATA_UPLOAD_DIR", BACKEND_DIR / "uploads"))
ALLOWED_EXTENSIONS = {"csv"}
REQUIRED_COLUMNS = {
    "vehicle_id",
    "route",
    "speed_kmph",
    "timestamp",
    "latitude",
    "longitude",
}
MAX_UPLOAD_BYTES = int(os.environ.get("MAX_UPLOAD_BYTES", 10 * 1024 * 1024))
TOKEN_MAX_AGE_SECONDS = int(os.environ.get("ADMIN_TOKEN_MAX_AGE_SECONDS", 8 * 60 * 60))


def create_app() -> Flask:
    """Create the Flask application with production-safe defaults."""
    # Static files and client-side routes share the root URL, so serve both explicitly
    # from ``serve_frontend`` instead of registering Flask's competing static route.
    app = Flask(__name__, static_folder=None)
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES
    app.config["JSON_SORT_KEYS"] = False

    cors_origins_env = os.environ.get("CORS_ORIGINS")
    if cors_origins_env:
        origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
    else:
        origins = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "https://transport-system-cgshok610-transport-system.vercel.app",
            r"https://.*\.vercel\.app",
        ]
    CORS(
        app,
        resources={r"/api/*": {"origins": origins}},
        methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    active_data_file = UPLOAD_FOLDER / "active_dataset.csv"
    set_data_filepath(active_data_file if active_data_file.exists() else DEFAULT_DATA_FILE)

    def admin_serializer() -> URLSafeTimedSerializer | None:
        secret = os.environ.get("ADMIN_TOKEN_SECRET")
        if not secret:
            return None
        return URLSafeTimedSerializer(secret, salt="transport-system-admin")

    def admin_required(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            serializer = admin_serializer()
            username = os.environ.get("ADMIN_USERNAME")
            authorization = request.headers.get("Authorization", "")
            token = authorization.removeprefix("Bearer ").strip()

            if not serializer or not username:
                return jsonify({"success": False, "error": "Admin access is not configured."}), 503
            if not token:
                return jsonify({"success": False, "error": "Authentication required."}), 401
            try:
                payload = serializer.loads(token, max_age=TOKEN_MAX_AGE_SECONDS)
            except (BadSignature, SignatureExpired):
                return jsonify({"success": False, "error": "Your session has expired. Please sign in again."}), 401
            if payload.get("username") != username:
                return jsonify({"success": False, "error": "Authentication required."}), 401
            return view(*args, **kwargs)

        return wrapped

    def api_error(message: str, status: int = 500):
        return jsonify({"success": False, "error": message}), status

    @app.errorhandler(RequestEntityTooLarge)
    def handle_large_upload(_error):
        return api_error(f"File is too large. Maximum upload size is {MAX_UPLOAD_BYTES // (1024 * 1024)} MB.", 413)

    @app.get("/api/info")
    def api_info():
        return jsonify({
            "message": "Smart City Transport System API",
            "version": "1.1",
            "endpoints": [
                "/api/dashboard",
                "/api/peak-hours",
                "/api/congestion",
                "/api/trends/daily",
                "/api/trends/weekly",
                "/api/speed-analysis",
                "/api/alerts",
                "/api/historical-vs-realtime",
                "/api/mapview",
                "/api/predict",
                "/api/realtime-simulation",
                "/api/powerbi-data",
            ],
            "timestamp": datetime.now().isoformat(),
        })

    def data_endpoint(operation):
        @wraps(operation)
        def wrapped():
            try:
                return jsonify({"success": True, "data": operation()})
            except Exception:
                app.logger.exception("Data endpoint failed: %s", request.path)
                return api_error("Unable to process the current transport dataset.")

        return wrapped

    @app.get("/api/dashboard")
    @data_endpoint
    def dashboard():
        return dashboard_data()

    @app.get("/api/peak-hours")
    @data_endpoint
    def peak_hours():
        return get_peak_hours()

    @app.get("/api/congestion")
    @data_endpoint
    def congestion():
        return congestion_data()

    @app.get("/api/trends/daily")
    @data_endpoint
    def daily_trends():
        return get_daily_trends()

    @app.get("/api/trends/weekly")
    @data_endpoint
    def weekly_trends():
        return get_weekly_trends()

    @app.get("/api/speed-analysis")
    @data_endpoint
    def speed_analysis():
        return get_speed_analysis()

    @app.get("/api/alerts")
    @data_endpoint
    def alerts():
        return generate_alerts()

    @app.get("/api/historical-vs-realtime")
    @data_endpoint
    def historical_realtime():
        return historical_vs_realtime()

    @app.get("/api/mapview")
    @data_endpoint
    def mapview():
        return map_data()

    @app.get("/api/predict")
    @data_endpoint
    def predict():
        data = pd.read_csv(DEFAULT_DATA_FILE if not active_data_file.exists() else active_data_file)
        data["hour"] = pd.to_datetime(data["timestamp"], errors="raise").dt.hour
        from sklearn.linear_model import LinearRegression

        features = data[["hour"]]
        target = data["speed_kmph"]
        model = LinearRegression().fit(features, target)
        predictions = {
            f"hour_{hour}": round(float(model.predict(pd.DataFrame({"hour": [hour]}))[0]), 2)
            for hour in (8, 12, 17, 19, 22)
        }
        current_hour = datetime.now().hour
        current_prediction = float(model.predict(pd.DataFrame({"hour": [current_hour]}))[0])
        return {
            "predictions_by_hour": predictions,
            "current_hour": current_hour,
            "current_prediction": round(current_prediction, 2),
            "model_score": round(float(model.score(features, target)), 4),
            "coefficient": round(float(model.coef_[0]), 4),
            "intercept": round(float(model.intercept_), 4),
        }

    @app.get("/api/realtime-simulation")
    def realtime_simulation():
        routes = ["Route-A", "Route-B", "Route-C", "Route-D", "Route-E"]
        current_hour = datetime.now().hour
        if 8 <= current_hour <= 10 or 17 <= current_hour <= 20:
            base_speed, congestion = 25, "High"
        elif current_hour >= 22 or current_hour <= 6:
            base_speed, congestion = 70, "Low"
        else:
            base_speed, congestion = 50, "Medium"
        vehicles = [
            {
                "vehicle_id": f"V{random.randint(1000, 9999)}",
                "route": random.choice(routes),
                "speed_kmph": round(base_speed + random.uniform(-15, 15), 2),
                "latitude": round(12.9 + random.uniform(0, 0.3), 6),
                "longitude": round(77.5 + random.uniform(0, 0.2), 6),
                "timestamp": datetime.now().isoformat(),
            }
            for _ in range(20)
        ]
        return jsonify({"success": True, "data": {"vehicles": vehicles, "current_congestion": congestion, "timestamp": datetime.now().isoformat(), "simulation": True}})

    @app.get("/api/powerbi-data")
    @data_endpoint
    def powerbi_data():
        data = pd.read_csv(DEFAULT_DATA_FILE if not active_data_file.exists() else active_data_file)
        data["timestamp"] = pd.to_datetime(data["timestamp"], errors="raise")
        data["hour"] = data["timestamp"].dt.hour
        data["day_name"] = data["timestamp"].dt.day_name()
        hourly = data.groupby("hour").agg(trips=("vehicle_id", "count"), avg_speed=("speed_kmph", "mean")).reset_index()
        weekly = data.groupby("day_name").agg(trips=("vehicle_id", "count"), avg_speed=("speed_kmph", "mean")).reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]).dropna().reset_index().rename(columns={"day_name": "day"})
        routes = data.groupby("route").agg(trips=("vehicle_id", "count"), avg_speed=("speed_kmph", "mean")).reset_index().sort_values("trips", ascending=False)
        for frame in (hourly, weekly, routes):
            frame["avg_speed"] = frame["avg_speed"].round(1)
        return {
            "kpis": {"total_trips": len(data), "total_vehicles": int(data["vehicle_id"].nunique()), "avg_speed": round(float(data["speed_kmph"].mean()), 1), "saturday_trips": int((data["day_name"] == "Saturday").sum())},
            "hourly": hourly.to_dict("records"),
            "weekly": weekly.to_dict("records"),
            "routes": routes.to_dict("records"),
        }

    @app.route("/api/admin/login", methods=["POST"], strict_slashes=False)
    def admin_login():
        configured_username = os.environ.get("ADMIN_USERNAME")
        configured_password = os.environ.get("ADMIN_PASSWORD")
        serializer = admin_serializer()
        credentials = request.get_json(silent=True) or {}
        if not configured_username or not configured_password or not serializer:
            return api_error("Admin access is not configured. Set ADMIN_USERNAME, ADMIN_PASSWORD, and ADMIN_TOKEN_SECRET.", 503)
        valid_username = hmac.compare_digest(str(credentials.get("username", "")), configured_username)
        valid_password = hmac.compare_digest(str(credentials.get("password", "")), configured_password)
        if not (valid_username and valid_password):
            return api_error("Invalid username or password.", 401)
        token = serializer.dumps({"username": configured_username})
        return jsonify({"success": True, "token": token, "expires_in": TOKEN_MAX_AGE_SECONDS})

    @app.route("/api/upload-csv", methods=["POST"], strict_slashes=False)
    @admin_required
    def upload_csv():
        file = request.files.get("file")
        if file is None or not file.filename:
            return api_error("Choose a CSV file to upload.", 400)
        filename = secure_filename(file.filename)
        if "." not in filename or filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSIONS:
            return api_error("Only CSV files are accepted.", 400)

        temporary_file = UPLOAD_FOLDER / f".{filename}.uploading"
        try:
            file.save(temporary_file)
            data = pd.read_csv(temporary_file)
            missing = sorted(REQUIRED_COLUMNS - set(data.columns))
            if missing:
                return api_error(f"Missing required columns: {', '.join(missing)}.", 400)
            if data.empty:
                return api_error("The CSV file contains no rows.", 400)
            if len(data) > 100_000:
                return api_error("The CSV file exceeds the 100,000 row limit.", 400)
            pd.to_numeric(data["speed_kmph"], errors="raise")
            pd.to_numeric(data["latitude"], errors="raise")
            pd.to_numeric(data["longitude"], errors="raise")
            pd.to_datetime(data["timestamp"], errors="raise")
            if data["speed_kmph"].lt(0).any() or data["latitude"].abs().gt(90).any() or data["longitude"].abs().gt(180).any():
                return api_error("The CSV contains invalid speed or coordinate values.", 400)

            temporary_file.replace(active_data_file)
            set_data_filepath(active_data_file)
            return jsonify({"success": True, "message": "Dataset uploaded and activated.", "rows": len(data), "columns": list(data.columns)})
        except (UnicodeDecodeError, pd.errors.ParserError, ValueError) as error:
            return api_error(f"The CSV could not be validated: {error}", 400)
        except Exception:
            app.logger.exception("CSV upload failed")
            return api_error("The dataset could not be uploaded.")
        finally:
            if temporary_file.exists():
                temporary_file.unlink()

    @app.route("/api/<path:_path>")
    def unknown_api_route(_path):
        return api_error("API endpoint not found.", 404)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path: str):
        if not BUILD_DIR.exists():
            return api_info()
        requested_file = BUILD_DIR / path
        if path and requested_file.is_file():
            return send_from_directory(BUILD_DIR, path)
        return send_from_directory(BUILD_DIR, "index.html")

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    logging.basicConfig(level=logging.INFO)
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1", host="0.0.0.0", port=port)
