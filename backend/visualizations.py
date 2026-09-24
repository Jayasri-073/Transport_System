"""
Smart City Transport System - Data Visualizations
Generate charts using Matplotlib and Seaborn
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from datetime import datetime

# Configure plot style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Paths
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "vehicle_route_speed_dataset_5000.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "visualizations")


def load_data():
    """Load and preprocess data."""
    df = pd.read_csv(DATA_FILE)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['date'] = df['timestamp'].dt.date
    return df


def create_peak_hours_chart(df):
    """Create peak hours bar chart."""
    fig, ax = plt.subplots(figsize=(14, 6))
    
    hourly_stats = df.groupby('hour').agg({
        'vehicle_id': 'count',
        'speed_kmph': 'mean'
    }).round(2)
    
    # Create bar chart
    colors = ['#FF6B6B' if 7 <= h <= 10 or 17 <= h <= 20 else '#4ECDC4' 
              for h in hourly_stats.index]
    
    bars = ax.bar(hourly_stats.index, hourly_stats['vehicle_id'], 
                  color=colors, edgecolor='white', linewidth=0.5)
    
    # Add speed line on secondary axis
    ax2 = ax.twinx()
    ax2.plot(hourly_stats.index, hourly_stats['speed_kmph'], 
             color='#2C3E50', linewidth=3, marker='o', markersize=6)
    ax2.set_ylabel('Average Speed (km/h)', fontsize=12, color='#2C3E50')
    
    # Styling
    ax.set_xlabel('Hour of Day', fontsize=12)
    ax.set_ylabel('Number of Vehicles', fontsize=12)
    ax.set_title('🚗 Peak Traffic Hours Analysis', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(range(24))
    ax.set_xticklabels([f'{h}:00' for h in range(24)], rotation=45, ha='right')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#FF6B6B', label='Peak Hours (Rush Hour)'),
        Patch(facecolor='#4ECDC4', label='Off-Peak Hours')
    ]
    ax.legend(handles=legend_elements, loc='upper left')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'peak_hours.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: peak_hours.png")


def create_route_congestion_chart(df):
    """Create route congestion heatmap."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Route-wise average speed bar chart
    route_stats = df.groupby('route')['speed_kmph'].agg(['mean', 'std', 'count'])
    route_stats = route_stats.sort_values('mean')
    
    colors = ['#FF6B6B' if speed < 40 else '#4ECDC4' if speed < 60 else '#45B7D1' 
              for speed in route_stats['mean']]
    
    axes[0].barh(route_stats.index, route_stats['mean'], color=colors, 
                  xerr=route_stats['std'], capsize=5, edgecolor='white')
    axes[0].set_xlabel('Average Speed (km/h)', fontsize=12)
    axes[0].set_ylabel('Route', fontsize=12)
    axes[0].set_title('📊 Route-wise Average Speed', fontsize=14, fontweight='bold')
    axes[0].axvline(x=40, color='red', linestyle='--', alpha=0.7, label='Congestion Threshold')
    axes[0].legend()
    
    # Heatmap: Route vs Hour
    pivot = df.pivot_table(
        values='speed_kmph', 
        index='route', 
        columns='hour', 
        aggfunc='mean'
    )
    
    sns.heatmap(pivot, annot=False, cmap='RdYlGn', ax=axes[1], 
                cbar_kws={'label': 'Speed (km/h)'})
    axes[1].set_title('🔥 Congestion Heatmap (Route × Hour)', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Hour of Day', fontsize=12)
    axes[1].set_ylabel('Route', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'route_congestion.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: route_congestion.png")


def create_speed_distribution(df):
    """Create speed distribution histogram."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Overall speed distribution
    axes[0].hist(df['speed_kmph'], bins=50, color='#3498DB', edgecolor='white', alpha=0.8)
    axes[0].axvline(df['speed_kmph'].mean(), color='red', linestyle='--', 
                     linewidth=2, label=f'Mean: {df["speed_kmph"].mean():.1f} km/h')
    axes[0].axvline(df['speed_kmph'].median(), color='green', linestyle='--', 
                     linewidth=2, label=f'Median: {df["speed_kmph"].median():.1f} km/h')
    axes[0].set_xlabel('Speed (km/h)', fontsize=12)
    axes[0].set_ylabel('Frequency', fontsize=12)
    axes[0].set_title('📈 Speed Distribution', fontsize=14, fontweight='bold')
    axes[0].legend()
    
    # Speed by route (box plot)
    df.boxplot(column='speed_kmph', by='route', ax=axes[1], 
               patch_artist=True,
               boxprops=dict(facecolor='#3498DB', alpha=0.7))
    axes[1].set_xlabel('Route', fontsize=12)
    axes[1].set_ylabel('Speed (km/h)', fontsize=12)
    axes[1].set_title('📦 Speed Distribution by Route', fontsize=14, fontweight='bold')
    plt.suptitle('')  # Remove automatic title
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'speed_distribution.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: speed_distribution.png")


def create_daily_trends(df):
    """Create daily traffic trends line chart."""
    fig, ax = plt.subplots(figsize=(14, 6))
    
    daily_stats = df.groupby('date').agg({
        'vehicle_id': 'count',
        'speed_kmph': 'mean'
    }).round(2)
    
    # Plot trips
    ax.fill_between(daily_stats.index, daily_stats['vehicle_id'], 
                    alpha=0.3, color='#3498DB')
    ax.plot(daily_stats.index, daily_stats['vehicle_id'], 
            color='#3498DB', linewidth=2, marker='o', markersize=4, label='Trip Count')
    
    # Speed on secondary axis
    ax2 = ax.twinx()
    ax2.plot(daily_stats.index, daily_stats['speed_kmph'], 
             color='#E74C3C', linewidth=2, marker='s', markersize=4, label='Avg Speed')
    ax2.set_ylabel('Average Speed (km/h)', fontsize=12, color='#E74C3C')
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Number of Trips', fontsize=12, color='#3498DB')
    ax.set_title('📅 Daily Traffic Trends', fontsize=16, fontweight='bold', pad=20)
    
    # Combine legends
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'daily_trends.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: daily_trends.png")


def create_weekly_trends(df):
    """Create weekly traffic patterns chart."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    weekly_stats = df.groupby('day_of_week').agg({
        'vehicle_id': 'count',
        'speed_kmph': 'mean'
    }).round(2)
    
    # Bar chart for trips
    colors = ['#FF6B6B' if d >= 5 else '#4ECDC4' for d in weekly_stats.index]
    bars = ax.bar(weekly_stats.index, weekly_stats['vehicle_id'], 
                  color=colors, edgecolor='white', linewidth=0.5)
    
    # Speed line
    ax2 = ax.twinx()
    ax2.plot(weekly_stats.index, weekly_stats['speed_kmph'], 
             color='#2C3E50', linewidth=3, marker='D', markersize=8)
    ax2.set_ylabel('Average Speed (km/h)', fontsize=12)
    
    ax.set_xlabel('Day of Week', fontsize=12)
    ax.set_ylabel('Number of Trips', fontsize=12)
    ax.set_title('📆 Weekly Traffic Pattern', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(range(7))
    ax.set_xticklabels(day_names, rotation=45, ha='right')
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#4ECDC4', label='Weekdays'),
        Patch(facecolor='#FF6B6B', label='Weekends')
    ]
    ax.legend(handles=legend_elements, loc='upper left')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'weekly_trends.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: weekly_trends.png")


def create_geographic_scatter(df):
    """Create geographic scatter plot of vehicle locations."""
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Sample data for better visualization
    sample = df.sample(min(1000, len(df)))
    
    scatter = ax.scatter(
        sample['longitude'], 
        sample['latitude'],
        c=sample['speed_kmph'],
        cmap='RdYlGn',
        alpha=0.6,
        s=30,
        edgecolors='none'
    )
    
    plt.colorbar(scatter, label='Speed (km/h)')
    
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.set_title('🗺️ Vehicle Locations (Color = Speed)', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'geographic_scatter.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: geographic_scatter.png")


def create_summary_dashboard(df):
    """Create a summary dashboard with multiple charts."""
    fig = plt.figure(figsize=(20, 12))
    
    # Overall metrics
    ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)
    ax1.text(0.1, 0.7, f"Total Trips: {len(df):,}", fontsize=24, fontweight='bold', 
             transform=ax1.transAxes, color='#3498DB')
    ax1.text(0.4, 0.7, f"Unique Vehicles: {df['vehicle_id'].nunique():,}", fontsize=24, 
             fontweight='bold', transform=ax1.transAxes, color='#2ECC71')
    ax1.text(0.7, 0.7, f"Avg Speed: {df['speed_kmph'].mean():.1f} km/h", fontsize=24, 
             fontweight='bold', transform=ax1.transAxes, color='#E74C3C')
    ax1.text(0.5, 0.2, "SMART CITY TRANSPORT SYSTEM - DASHBOARD", fontsize=28, 
             fontweight='bold', transform=ax1.transAxes, ha='center', color='#2C3E50')
    ax1.axis('off')
    
    # Hourly traffic
    ax2 = plt.subplot2grid((3, 3), (1, 0))
    hourly = df.groupby('hour')['vehicle_id'].count()
    ax2.bar(hourly.index, hourly.values, color='#4ECDC4')
    ax2.set_title('Hourly Traffic', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Hour')
    
    # Route distribution
    ax3 = plt.subplot2grid((3, 3), (1, 1))
    route_counts = df['route'].value_counts()
    ax3.pie(route_counts.values, labels=route_counts.index, autopct='%1.1f%%',
            colors=sns.color_palette("husl", len(route_counts)))
    ax3.set_title('Route Distribution', fontsize=12, fontweight='bold')
    
    # Speed histogram
    ax4 = plt.subplot2grid((3, 3), (1, 2))
    ax4.hist(df['speed_kmph'], bins=30, color='#3498DB', edgecolor='white')
    ax4.set_title('Speed Distribution', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Speed (km/h)')
    
    # Weekly pattern
    ax5 = plt.subplot2grid((3, 3), (2, 0), colspan=2)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    weekly = df.groupby('day_of_week')['vehicle_id'].count()
    ax5.bar(range(7), weekly.values, color=['#4ECDC4']*5 + ['#FF6B6B']*2)
    ax5.set_xticks(range(7))
    ax5.set_xticklabels(days)
    ax5.set_title('Weekly Traffic Pattern', fontsize=12, fontweight='bold')
    
    # Congestion by route
    ax6 = plt.subplot2grid((3, 3), (2, 2))
    route_speed = df.groupby('route')['speed_kmph'].mean().sort_values()
    colors = ['#FF6B6B' if s < 40 else '#FFA500' if s < 60 else '#4ECDC4' for s in route_speed.values]
    ax6.barh(route_speed.index, route_speed.values, color=colors)
    ax6.set_title('Route Speeds', fontsize=12, fontweight='bold')
    ax6.set_xlabel('Avg Speed (km/h)')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'dashboard_summary.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Created: dashboard_summary.png")


def generate_all_visualizations():
    """Generate all visualization charts."""
    print("🎨 Generating Visualizations...")
    print("-" * 50)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load data
    print(f"📂 Loading data from: {DATA_FILE}")
    df = load_data()
    print(f"   Loaded {len(df)} records")
    
    # Generate each chart
    create_peak_hours_chart(df)
    create_route_congestion_chart(df)
    create_speed_distribution(df)
    create_daily_trends(df)
    create_weekly_trends(df)
    create_geographic_scatter(df)
    create_summary_dashboard(df)
    
    print("-" * 50)
    print(f"✅ All visualizations saved to: {OUTPUT_DIR}")
    print(f"   Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    generate_all_visualizations()
