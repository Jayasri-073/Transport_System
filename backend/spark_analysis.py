"""
Smart City Transport System - PySpark Big Data Analysis
Performs distributed batch processing on traffic data
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, hour, dayofweek, when, round as spark_round
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
import os

# Path to data
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "vehicle_route_speed_dataset_5000.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "spark_output")


def create_spark_session():
    """Create and configure Spark session."""
    spark = SparkSession.builder \
        .appName("SmartCityTransport") \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark


def load_traffic_data(spark):
    """Load traffic data into Spark DataFrame."""
    schema = StructType([
        StructField("vehicle_id", StringType(), True),
        StructField("route", StringType(), True),
        StructField("speed_kmph", DoubleType(), True),
        StructField("timestamp", StringType(), True),
        StructField("latitude", DoubleType(), True),
        StructField("longitude", DoubleType(), True)
    ])
    
    df = spark.read.csv(DATA_FILE, header=True, schema=schema)
    
    # Convert timestamp string to timestamp type and extract features
    df = df.withColumn("timestamp", col("timestamp").cast(TimestampType()))
    df = df.withColumn("hour", hour(col("timestamp")))
    df = df.withColumn("day_of_week", dayofweek(col("timestamp")))
    
    return df


def analyze_peak_hours(df):
    """Identify peak traffic hours using Spark."""
    print("\n=== Peak Hours Analysis (Spark) ===")
    
    hourly_stats = df.groupBy("hour").agg(
        count("vehicle_id").alias("vehicle_count"),
        spark_round(avg("speed_kmph"), 2).alias("avg_speed")
    ).orderBy("hour")
    
    print("\nHourly Traffic Distribution:")
    hourly_stats.show(24)
    
    # Find peak hours
    peak_hours = hourly_stats.orderBy(col("vehicle_count").desc()).limit(5)
    print("\nTop 5 Peak Hours:")
    peak_hours.show()
    
    return hourly_stats


def analyze_route_congestion(df):
    """Analyze congestion by route."""
    print("\n=== Route Congestion Analysis (Spark) ===")
    
    route_stats = df.groupBy("route").agg(
        count("vehicle_id").alias("trip_count"),
        spark_round(avg("speed_kmph"), 2).alias("avg_speed"),
        spark_round(avg("latitude"), 4).alias("center_lat"),
        spark_round(avg("longitude"), 4).alias("center_lng")
    ).withColumn(
        "congestion_level",
        when(col("avg_speed") < 25, "High")
        .when(col("avg_speed") < 50, "Medium")
        .otherwise("Low")
    ).orderBy("avg_speed")
    
    print("\nRoute Statistics:")
    route_stats.show()
    
    return route_stats


def analyze_weekly_pattern(df):
    """Analyze weekly traffic patterns."""
    print("\n=== Weekly Traffic Pattern (Spark) ===")
    
    weekly_stats = df.groupBy("day_of_week").agg(
        count("vehicle_id").alias("trip_count"),
        spark_round(avg("speed_kmph"), 2).alias("avg_speed")
    ).orderBy("day_of_week")
    
    print("\nDaily Traffic (1=Sunday, 7=Saturday):")
    weekly_stats.show()
    
    return weekly_stats


def detect_congestion_hotspots(df):
    """Detect congestion hotspots based on location."""
    print("\n=== Congestion Hotspots (Spark) ===")
    
    # Filter low speed records (congested)
    congested = df.filter(col("speed_kmph") < 30)
    
    # Round coordinates to group nearby locations
    hotspots = congested.withColumn(
        "lat_group", spark_round(col("latitude"), 2)
    ).withColumn(
        "lng_group", spark_round(col("longitude"), 2)
    ).groupBy("lat_group", "lng_group", "route").agg(
        count("vehicle_id").alias("incident_count"),
        spark_round(avg("speed_kmph"), 2).alias("avg_speed")
    ).orderBy(col("incident_count").desc()).limit(10)
    
    print("\nTop 10 Congestion Hotspots:")
    hotspots.show()
    
    return hotspots


def generate_summary_report(df, hourly_stats, route_stats, weekly_stats):
    """Generate comprehensive summary report."""
    print("\n" + "=" * 60)
    print("SMART CITY TRANSPORT SYSTEM - SUMMARY REPORT")
    print("=" * 60)
    
    # Overall statistics
    total_records = df.count()
    unique_vehicles = df.select("vehicle_id").distinct().count()
    overall_avg_speed = df.agg(spark_round(avg("speed_kmph"), 2)).collect()[0][0]
    
    print(f"\n📊 OVERALL STATISTICS")
    print(f"   Total Records: {total_records:,}")
    print(f"   Unique Vehicles: {unique_vehicles:,}")
    print(f"   Average Speed: {overall_avg_speed} km/h")
    
    # Peak hours
    peak = hourly_stats.orderBy(col("vehicle_count").desc()).first()
    print(f"\n⏰ PEAK TRAFFIC")
    print(f"   Busiest Hour: {peak['hour']}:00")
    print(f"   Vehicle Count: {peak['vehicle_count']}")
    
    # Congested routes
    congested_routes = route_stats.filter(col("avg_speed") < 40).collect()
    print(f"\n🚗 CONGESTION ANALYSIS")
    print(f"   Routes with Speed < 40 km/h: {len(congested_routes)}")
    for r in congested_routes:
        print(f"   - {r['route']}: {r['avg_speed']} km/h ({r['congestion_level']})")
    
    print("\n" + "=" * 60)


def save_results(hourly_stats, route_stats, weekly_stats, hotspots):
    """Save analysis results to files."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    hourly_stats.coalesce(1).write.mode("overwrite").csv(
        os.path.join(OUTPUT_DIR, "hourly_stats"), header=True
    )
    route_stats.coalesce(1).write.mode("overwrite").csv(
        os.path.join(OUTPUT_DIR, "route_stats"), header=True
    )
    weekly_stats.coalesce(1).write.mode("overwrite").csv(
        os.path.join(OUTPUT_DIR, "weekly_stats"), header=True
    )
    hotspots.coalesce(1).write.mode("overwrite").csv(
        os.path.join(OUTPUT_DIR, "hotspots"), header=True
    )
    
    print(f"\n✅ Results saved to: {OUTPUT_DIR}")


def run_spark_analysis():
    """Run complete Spark analysis pipeline."""
    print("🚀 Starting PySpark Big Data Analysis...")
    print("-" * 50)
    
    # Create Spark session
    spark = create_spark_session()
    print(f"Spark Version: {spark.version}")
    
    try:
        # Load data
        print(f"\n📂 Loading data from: {DATA_FILE}")
        df = load_traffic_data(spark)
        print(f"   Loaded {df.count()} records")
        
        # Cache for better performance
        df.cache()
        
        # Run analyses
        hourly_stats = analyze_peak_hours(df)
        route_stats = analyze_route_congestion(df)
        weekly_stats = analyze_weekly_pattern(df)
        hotspots = detect_congestion_hotspots(df)
        
        # Generate summary
        generate_summary_report(df, hourly_stats, route_stats, weekly_stats)
        
        # Save results
        save_results(hourly_stats, route_stats, weekly_stats, hotspots)
        
        print("\n✅ Spark analysis completed successfully!")
        
    finally:
        spark.stop()
        print("Spark session stopped.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running in test mode...")
        spark = create_spark_session()
        df = load_traffic_data(spark)
        print(f"Test passed! Loaded {df.count()} records")
        spark.stop()
    else:
        run_spark_analysis()
