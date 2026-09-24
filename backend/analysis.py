"""
Smart City Transport System - Traffic Analysis Module
Performs real-time traffic analysis on vehicle data
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Path to the CSV data file
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "vehicle_route_speed_dataset_5000.csv")


def load_data():
    """Load and preprocess the traffic data."""
    df = pd.read_csv(DATA_FILE)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['date'] = df['timestamp'].dt.date
    return df


def dashboard_data():
    """Return real-time dashboard metrics."""
    df = load_data()
    
    # Calculate real metrics from data
    total_vehicles = df['vehicle_id'].nunique()
    total_trips = len(df)
    avg_speed = round(df['speed_kmph'].mean(), 2)
    
    # Active vehicles (last hour simulation)
    recent_data = df[df['timestamp'] >= df['timestamp'].max() - timedelta(hours=1)]
    active_vehicles = recent_data['vehicle_id'].nunique()
    
    # Calculate congestion level (based on average speed)
    if avg_speed < 25:
        congestion_level = "High"
    elif avg_speed < 50:
        congestion_level = "Medium"
    else:
        congestion_level = "Low"
    
    # Route statistics
    route_stats = df.groupby('route').agg({
        'speed_kmph': 'mean',
        'vehicle_id': 'count'
    }).round(2).to_dict()
    
    return {
        "total_vehicles": total_vehicles,
        "total_trips": total_trips,
        "average_speed": avg_speed,
        "active_vehicles": active_vehicles,
        "congestion_level": congestion_level,
        "routes": list(df['route'].unique()),
        "route_stats": {
            route: {
                "avg_speed": route_stats['speed_kmph'][route],
                "trip_count": route_stats['vehicle_id'][route]
            }
            for route in df['route'].unique()
        }
    }


def get_peak_hours():
    """Identify peak traffic hours based on vehicle count and speed."""
    df = load_data()
    
    # Group by hour and calculate metrics
    hourly_stats = df.groupby('hour').agg({
        'vehicle_id': 'count',
        'speed_kmph': 'mean'
    }).round(2)
    
    hourly_stats.columns = ['vehicle_count', 'avg_speed']
    
    # Find peak hours (top 5 hours with most vehicles)
    peak_hours = hourly_stats.nlargest(5, 'vehicle_count')
    
    # Identify morning and evening peaks
    morning_hours = hourly_stats[(hourly_stats.index >= 7) & (hourly_stats.index <= 10)]
    evening_hours = hourly_stats[(hourly_stats.index >= 17) & (hourly_stats.index <= 20)]
    
    return {
        "hourly_data": [
            {
                "hour": int(hour),
                "vehicle_count": int(row['vehicle_count']),
                "avg_speed": float(row['avg_speed'])
            }
            for hour, row in hourly_stats.iterrows()
        ],
        "peak_hours": [
            {
                "hour": int(hour),
                "vehicle_count": int(row['vehicle_count']),
                "avg_speed": float(row['avg_speed'])
            }
            for hour, row in peak_hours.iterrows()
        ],
        "morning_peak": {
            "hour": int(morning_hours['vehicle_count'].idxmax()) if len(morning_hours) > 0 else None,
            "vehicle_count": int(morning_hours['vehicle_count'].max()) if len(morning_hours) > 0 else 0
        },
        "evening_peak": {
            "hour": int(evening_hours['vehicle_count'].idxmax()) if len(evening_hours) > 0 else None,
            "vehicle_count": int(evening_hours['vehicle_count'].max()) if len(evening_hours) > 0 else 0
        }
    }


def congestion_data():
    """Identify high congestion routes and hotspots."""
    df = load_data()
    
    # Congestion is indicated by low speed
    CONGESTION_THRESHOLD = 30  # km/h
    
    # Route-wise congestion analysis
    route_congestion = df.groupby('route').agg({
        'speed_kmph': ['mean', 'min', 'max', 'std'],
        'vehicle_id': 'count'
    }).round(2)
    
    route_congestion.columns = ['avg_speed', 'min_speed', 'max_speed', 'speed_std', 'vehicle_count']
    route_congestion = route_congestion.reset_index()
    
    # Classify congestion severity
    def get_severity(speed):
        if speed < 20:
            return "critical"
        elif speed < 30:
            return "high"
        elif speed < 50:
            return "medium"
        return "low"
    
    # Find location clusters with low speed (hotspots)
    congested_records = df[df['speed_kmph'] < CONGESTION_THRESHOLD]
    
    # Group by approximate location (round to 2 decimal places)
    congested_records = congested_records.copy()
    congested_records['lat_group'] = congested_records['latitude'].round(2)
    congested_records['lon_group'] = congested_records['longitude'].round(2)
    
    hotspots = congested_records.groupby(['lat_group', 'lon_group', 'route']).agg({
        'speed_kmph': 'mean',
        'vehicle_id': 'count'
    }).reset_index()
    
    hotspots = hotspots.nlargest(10, 'vehicle_id')
    
    return {
        "routes": [
            {
                "route": row['route'],
                "avg_speed": float(row['avg_speed']),
                "min_speed": float(row['min_speed']),
                "max_speed": float(row['max_speed']),
                "vehicle_count": int(row['vehicle_count']),
                "severity": get_severity(row['avg_speed'])
            }
            for _, row in route_congestion.iterrows()
        ],
        "hotspots": [
            {
                "latitude": float(row['lat_group']),
                "longitude": float(row['lon_group']),
                "route": row['route'],
                "avg_speed": float(row['speed_kmph']),
                "incident_count": int(row['vehicle_id']),
                "severity": get_severity(row['speed_kmph'])
            }
            for _, row in hotspots.iterrows()
        ],
        "congestion_threshold": CONGESTION_THRESHOLD,
        "total_congested_records": len(congested_records)
    }


def get_daily_trends():
    """Analyze daily traffic patterns."""
    df = load_data()
    
    # Daily statistics
    daily_stats = df.groupby('date').agg({
        'vehicle_id': 'count',
        'speed_kmph': 'mean'
    }).round(2)
    
    daily_stats.columns = ['trip_count', 'avg_speed']
    daily_stats = daily_stats.reset_index()
    
    # Convert date to string for JSON serialization
    daily_stats['date'] = daily_stats['date'].astype(str)
    
    return {
        "daily_data": daily_stats.to_dict('records'),
        "summary": {
            "avg_daily_trips": int(daily_stats['trip_count'].mean()),
            "max_trips_day": daily_stats.loc[daily_stats['trip_count'].idxmax()].to_dict(),
            "min_trips_day": daily_stats.loc[daily_stats['trip_count'].idxmin()].to_dict()
        }
    }


def get_weekly_trends():
    """Analyze weekly traffic patterns."""
    df = load_data()
    
    # Day names for readability
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Weekly statistics
    weekly_stats = df.groupby('day_of_week').agg({
        'vehicle_id': 'count',
        'speed_kmph': 'mean'
    }).round(2)
    
    weekly_stats.columns = ['trip_count', 'avg_speed']
    weekly_stats = weekly_stats.reset_index()
    weekly_stats['day_name'] = weekly_stats['day_of_week'].apply(lambda x: day_names[x])
    
    # Identify busiest day
    busiest_day_idx = weekly_stats['trip_count'].idxmax()
    
    return {
        "weekly_data": [
            {
                "day": row['day_name'],
                "day_of_week": int(row['day_of_week']),
                "trip_count": int(row['trip_count']),
                "avg_speed": float(row['avg_speed'])
            }
            for _, row in weekly_stats.iterrows()
        ],
        "busiest_day": weekly_stats.loc[busiest_day_idx, 'day_name'],
        "weekend_vs_weekday": {
            "weekday_avg": float(weekly_stats[weekly_stats['day_of_week'] < 5]['trip_count'].mean()),
            "weekend_avg": float(weekly_stats[weekly_stats['day_of_week'] >= 5]['trip_count'].mean())
        }
    }


def map_data():
    """Return vehicle location data for map visualization."""
    df = load_data()
    
    # Get latest position for each vehicle
    latest_positions = df.sort_values('timestamp').groupby('vehicle_id').last().reset_index()
    
    # Sample 100 vehicles for map display
    sample_vehicles = latest_positions.sample(min(100, len(latest_positions)))
    
    return {
        "vehicles": [
            {
                "id": row['vehicle_id'],
                "lat": float(row['latitude']),
                "lng": float(row['longitude']),
                "speed": float(row['speed_kmph']),
                "route": row['route'],
                "timestamp": str(row['timestamp'])
            }
            for _, row in sample_vehicles.iterrows()
        ],
        "total_vehicles": len(latest_positions),
        "center": {
            "lat": float(latest_positions['latitude'].mean()),
            "lng": float(latest_positions['longitude'].mean())
        }
    }


def get_speed_analysis():
    """Detailed speed analysis across routes and times."""
    df = load_data()
    
    # Overall speed distribution
    speed_percentiles = df['speed_kmph'].quantile([0.25, 0.5, 0.75]).to_dict()
    
    # Speed by route
    route_speeds = df.groupby('route')['speed_kmph'].describe().round(2)
    
    # Speed by hour
    hourly_speeds = df.groupby('hour')['speed_kmph'].mean().round(2)
    
    return {
        "overall": {
            "mean": float(df['speed_kmph'].mean()),
            "median": float(df['speed_kmph'].median()),
            "std": float(df['speed_kmph'].std()),
            "min": float(df['speed_kmph'].min()),
            "max": float(df['speed_kmph'].max()),
            "percentile_25": float(speed_percentiles[0.25]),
            "percentile_50": float(speed_percentiles[0.50]),
            "percentile_75": float(speed_percentiles[0.75])
        },
        "by_route": route_speeds.to_dict(),
        "by_hour": {int(k): float(v) for k, v in hourly_speeds.to_dict().items()}
    }


def generate_alerts():
    """Generate traffic alerts based on current conditions."""
    df = load_data()
    alerts = []
    
    # Check for low speed conditions (traffic jams)
    route_speeds = df.groupby('route')['speed_kmph'].mean()
    for route, speed in route_speeds.items():
        if speed < 25:
            alerts.append({
                "type": "traffic_jam",
                "severity": "high",
                "route": route,
                "message": f"Heavy traffic detected on {route}. Average speed: {speed:.1f} km/h",
                "timestamp": datetime.now().isoformat()
            })
        elif speed < 40:
            alerts.append({
                "type": "slow_traffic",
                "severity": "medium",
                "route": route,
                "message": f"Slow traffic on {route}. Average speed: {speed:.1f} km/h",
                "timestamp": datetime.now().isoformat()
            })
    
    # Check for congestion hotspots
    congested = df[df['speed_kmph'] < 20]
    if len(congested) > 100:
        alerts.append({
            "type": "congestion_alert",
            "severity": "high",
            "message": f"Multiple congestion points detected. {len(congested)} incidents recorded.",
            "timestamp": datetime.now().isoformat()
        })
    
    return {
        "alerts": alerts,
        "total_alerts": len(alerts),
        "high_severity": len([a for a in alerts if a['severity'] == 'high']),
        "generated_at": datetime.now().isoformat()
    }


def historical_vs_realtime():
    """Compare historical patterns with simulated real-time data."""
    df = load_data()
    
    # Historical average (all data)
    historical_avg_speed = df['speed_kmph'].mean()
    
    # Simulate "real-time" as the most recent data
    recent_data = df[df['timestamp'] >= df['timestamp'].max() - timedelta(hours=2)]
    realtime_avg_speed = recent_data['speed_kmph'].mean()
    
    # Calculate difference
    speed_change = realtime_avg_speed - historical_avg_speed
    change_percent = (speed_change / historical_avg_speed) * 100
    
    # Determine traffic status
    if speed_change < -10:
        status = "Traffic jam detected - speeds significantly below average"
    elif speed_change < -5:
        status = "Slight congestion - speeds below normal"
    elif speed_change > 5:
        status = "Free flow - speeds above normal"
    else:
        status = "Normal traffic conditions"
    
    return {
        "historical": {
            "avg_speed": round(historical_avg_speed, 2),
            "sample_size": len(df)
        },
        "realtime": {
            "avg_speed": round(realtime_avg_speed, 2),
            "sample_size": len(recent_data)
        },
        "comparison": {
            "speed_change": round(speed_change, 2),
            "change_percent": round(change_percent, 2),
            "status": status
        },
        "timestamp": datetime.now().isoformat()
    }


# Test the functions if run directly
if __name__ == "__main__":
    print("Testing analysis functions...")
    print("\n=== Dashboard Data ===")
    print(dashboard_data())
    print("\n=== Peak Hours ===")
    print(get_peak_hours())
    print("\n=== Congestion Data ===")
    print(congestion_data())
