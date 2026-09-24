"""
Power BI Style Traffic Analysis Visualizations
Creates professional dashboard-style charts for traffic analysis
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np
from datetime import datetime
import os

# Configuration
DATA_FILE = "../vehicle_route_speed_dataset_5000.csv"
OUTPUT_DIR = "powerbi_charts"

# Power BI Color Palette
COLORS = {
    'primary': '#118DFF',      # Blue
    'secondary': '#12239E',    # Dark Blue
    'success': '#00B294',      # Green
    'warning': '#F2C80F',      # Yellow
    'danger': '#E81123',       # Red
    'neutral': '#605E5C',      # Gray
    'background': '#F3F2F1',   # Light Gray
    'highlight': '#FF8C00',    # Orange
    'purple': '#8764B8',
    'teal': '#00B7C3',
}

# Route colors
ROUTE_COLORS = {
    'Route-A': '#118DFF',
    'Route-B': '#12239E', 
    'Route-C': '#00B294',
    'Route-D': '#F2C80F',
    'Route-E': '#E81123'
}

def load_data():
    """Load and preprocess traffic data."""
    df = pd.read_csv(DATA_FILE)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['day_name'] = df['timestamp'].dt.day_name()
    df['date'] = df['timestamp'].dt.date
    return df

def create_hourly_traffic_chart(df):
    """Create Power BI style hourly traffic chart highlighting 8 PM."""
    fig, ax = plt.subplots(figsize=(14, 7), facecolor='white')
    
    # Hourly statistics
    hourly = df.groupby('hour').agg({
        'vehicle_id': 'count',
        'speed_kmph': 'mean'
    }).reset_index()
    hourly.columns = ['hour', 'trips', 'avg_speed']
    
    # Create bars with conditional coloring (8 PM = 20 highlighted)
    colors = [COLORS['highlight'] if h == 20 else COLORS['primary'] for h in hourly['hour']]
    
    bars = ax.bar(hourly['hour'], hourly['trips'], color=colors, 
                  edgecolor='white', linewidth=0.5, width=0.8)
    
    # Add value labels on bars
    for bar, trips in zip(bars, hourly['trips']):
        height = bar.get_height()
        ax.annotate(f'{int(trips)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold',
                    color=COLORS['secondary'])
    
    # Add speed line on secondary axis
    ax2 = ax.twinx()
    ax2.plot(hourly['hour'], hourly['avg_speed'], color=COLORS['danger'], 
             linewidth=3, marker='o', markersize=8, markerfacecolor='white',
             markeredgewidth=2)
    ax2.set_ylabel('Average Speed (km/h)', fontsize=12, color=COLORS['danger'], fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=COLORS['danger'])
    ax2.set_ylim(0, 120)
    
    # Highlight current hour (8 PM = 20)
    current_hour = 20
    current_trips = hourly[hourly['hour'] == current_hour]['trips'].values[0]
    current_speed = hourly[hourly['hour'] == current_hour]['avg_speed'].values[0]
    
    # Add annotation for 8 PM
    ax.annotate(f'8:00 PM Peak\n{int(current_trips)} trips\n{current_speed:.1f} km/h',
                xy=(current_hour, current_trips),
                xytext=(current_hour + 2, current_trips + 30),
                fontsize=11, fontweight='bold',
                color=COLORS['highlight'],
                arrowprops=dict(arrowstyle='->', color=COLORS['highlight'], lw=2),
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                         edgecolor=COLORS['highlight'], linewidth=2))
    
    # Styling
    ax.set_xlabel('Hour of Day', fontsize=12, fontweight='bold', color=COLORS['neutral'])
    ax.set_ylabel('Number of Trips', fontsize=12, fontweight='bold', color=COLORS['primary'])
    ax.tick_params(axis='y', labelcolor=COLORS['primary'])
    ax.set_xticks(range(24))
    ax.set_xticklabels([f'{h}:00' for h in range(24)], rotation=45, ha='right')
    ax.set_xlim(-0.5, 23.5)
    
    # Title
    ax.set_title('HOURLY TRAFFIC PATTERN - Today', 
                 fontsize=16, fontweight='bold', color=COLORS['secondary'], pad=20)
    
    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=COLORS['primary'], label='Regular Hours'),
        mpatches.Patch(facecolor=COLORS['highlight'], label='8:00 PM (Current)'),
        plt.Line2D([0], [0], color=COLORS['danger'], linewidth=3, marker='o', label='Avg Speed')
    ]
    ax.legend(handles=legend_elements, loc='upper left', frameon=True, fancybox=True)
    
    # Grid
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_facecolor('#FAFAFA')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'powerbi_hourly_traffic.png'), dpi=200, 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ Created: powerbi_hourly_traffic.png")

def create_weekly_pattern_chart(df):
    """Create Power BI style weekly pattern highlighting Saturday."""
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
    
    # Daily statistics
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily = df.groupby('day_name').agg({
        'vehicle_id': 'count',
        'speed_kmph': 'mean'
    }).reset_index()
    daily.columns = ['day', 'trips', 'avg_speed']
    daily['day'] = pd.Categorical(daily['day'], categories=day_order, ordered=True)
    daily = daily.sort_values('day')
    
    # Highlight Saturday
    colors = [COLORS['highlight'] if d == 'Saturday' else COLORS['teal'] for d in daily['day']]
    
    bars = ax.bar(range(len(daily)), daily['trips'], color=colors,
                  edgecolor='white', linewidth=1, width=0.7)
    
    # Add value labels
    for i, (bar, trips) in enumerate(zip(bars, daily['trips'])):
        height = bar.get_height()
        ax.annotate(f'{int(trips)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold',
                    color=COLORS['secondary'])
    
    # Highlight Saturday with annotation
    sat_idx = day_order.index('Saturday')
    sat_trips = daily[daily['day'] == 'Saturday']['trips'].values[0]
    sat_speed = daily[daily['day'] == 'Saturday']['avg_speed'].values[0]
    
    ax.annotate(f'SATURDAY PEAK\n{int(sat_trips)} trips\n{sat_speed:.1f} km/h avg',
                xy=(sat_idx, sat_trips),
                xytext=(sat_idx - 1.5, sat_trips + 80),
                fontsize=12, fontweight='bold', color=COLORS['highlight'],
                arrowprops=dict(arrowstyle='->', color=COLORS['highlight'], lw=2),
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                         edgecolor=COLORS['highlight'], linewidth=2))
    
    # Styling
    ax.set_xticks(range(len(daily)))
    ax.set_xticklabels([d[:3] for d in day_order], fontsize=12, fontweight='bold')
    ax.set_xlabel('Day of Week', fontsize=12, fontweight='bold', color=COLORS['neutral'])
    ax.set_ylabel('Number of Trips', fontsize=12, fontweight='bold', color=COLORS['teal'])
    
    ax.set_title('WEEKLY TRAFFIC PATTERN - Saturday Peak Analysis', 
                 fontsize=16, fontweight='bold', color=COLORS['secondary'], pad=20)
    
    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=COLORS['teal'], label='Regular Days'),
        mpatches.Patch(facecolor=COLORS['highlight'], label='Saturday (Peak)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', frameon=True, fancybox=True)
    
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_facecolor('#FAFAFA')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'powerbi_weekly_pattern.png'), dpi=200,
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ Created: powerbi_weekly_pattern.png")

def create_route_peak_analysis(df):
    """Create Power BI style route-wise peak traffic analysis."""
    fig = plt.figure(figsize=(16, 10), facecolor='white')
    gs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.3)
    
    routes = df['route'].unique()
    
    for idx, route in enumerate(sorted(routes)):
        row = idx // 3
        col = idx % 3
        ax = fig.add_subplot(gs[row, col])
        
        route_data = df[df['route'] == route]
        hourly = route_data.groupby('hour')['vehicle_id'].count().reset_index()
        hourly.columns = ['hour', 'trips']
        
        # Find peak hour
        peak_hour = hourly.loc[hourly['trips'].idxmax(), 'hour']
        peak_trips = hourly['trips'].max()
        
        # Color bars
        colors = [COLORS['highlight'] if h == peak_hour else ROUTE_COLORS.get(route, COLORS['primary']) 
                  for h in hourly['hour']]
        
        ax.bar(hourly['hour'], hourly['trips'], color=colors, edgecolor='white', width=0.8)
        
        # Peak hour annotation
        ax.annotate(f'Peak: {int(peak_hour)}:00',
                    xy=(peak_hour, peak_trips),
                    xytext=(peak_hour, peak_trips + 5),
                    ha='center', fontsize=9, fontweight='bold', color=COLORS['highlight'])
        
        ax.set_title(f'{route}', fontsize=14, fontweight='bold', 
                     color=ROUTE_COLORS.get(route, COLORS['primary']))
        ax.set_xlabel('Hour', fontsize=10)
        ax.set_ylabel('Trips', fontsize=10)
        ax.set_xticks([0, 6, 12, 18, 23])
        ax.set_xticklabels(['0', '6', '12', '18', '23'])
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_facecolor('#FAFAFA')
    
    fig.suptitle('ROUTE-WISE PEAK TRAFFIC ANALYSIS - All Day Pattern', 
                 fontsize=18, fontweight='bold', color=COLORS['secondary'], y=0.98)
    
    plt.savefig(os.path.join(OUTPUT_DIR, 'powerbi_route_peaks.png'), dpi=200,
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ Created: powerbi_route_peaks.png")

def create_saturday_route_analysis(df):
    """Create detailed Saturday traffic analysis by route."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='white')
    
    saturday_data = df[df['day_name'] == 'Saturday']
    
    # Left: Saturday hourly by route (stacked)
    ax1 = axes[0]
    routes = sorted(df['route'].unique())
    
    hourly_by_route = saturday_data.groupby(['hour', 'route'])['vehicle_id'].count().unstack(fill_value=0)
    
    bottom = np.zeros(24)
    for route in routes:
        if route in hourly_by_route.columns:
            ax1.bar(range(24), hourly_by_route[route], bottom=bottom,
                   label=route, color=ROUTE_COLORS.get(route, COLORS['primary']),
                   edgecolor='white', linewidth=0.5)
            bottom += hourly_by_route[route].values
    
    ax1.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Number of Trips', fontsize=12, fontweight='bold')
    ax1.set_title('SATURDAY - Hourly Traffic by Route', fontsize=14, fontweight='bold',
                  color=COLORS['secondary'])
    ax1.set_xticks([0, 4, 8, 12, 16, 20, 23])
    ax1.set_xticklabels(['0', '4', '8', '12', '16', '20', '23'])
    ax1.legend(loc='upper left', frameon=True)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_facecolor('#FAFAFA')
    
    # Right: Route comparison on Saturday
    ax2 = axes[1]
    route_saturday = saturday_data.groupby('route').agg({
        'vehicle_id': 'count',
        'speed_kmph': 'mean'
    }).reset_index()
    route_saturday.columns = ['route', 'trips', 'avg_speed']
    route_saturday = route_saturday.sort_values('trips', ascending=True)
    
    colors = [ROUTE_COLORS.get(r, COLORS['primary']) for r in route_saturday['route']]
    bars = ax2.barh(route_saturday['route'], route_saturday['trips'], color=colors,
                    edgecolor='white', height=0.6)
    
    # Add value labels
    for bar, trips, speed in zip(bars, route_saturday['trips'], route_saturday['avg_speed']):
        width = bar.get_width()
        ax2.annotate(f'{int(trips)} trips ({speed:.1f} km/h)',
                    xy=(width, bar.get_y() + bar.get_height()/2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=10, fontweight='bold')
    
    ax2.set_xlabel('Number of Trips', fontsize=12, fontweight='bold')
    ax2.set_title('SATURDAY - Route Performance', fontsize=14, fontweight='bold',
                  color=COLORS['secondary'])
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    ax2.set_facecolor('#FAFAFA')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'powerbi_saturday_analysis.png'), dpi=200,
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ Created: powerbi_saturday_analysis.png")

def create_dashboard_summary(df):
    """Create Power BI style dashboard summary."""
    fig = plt.figure(figsize=(18, 12), facecolor='white')
    gs = GridSpec(3, 4, figure=fig, hspace=0.4, wspace=0.3)
    
    # KPI Cards (top row)
    total_trips = len(df)
    total_vehicles = df['vehicle_id'].nunique()
    avg_speed = df['speed_kmph'].mean()
    saturday_trips = len(df[df['day_name'] == 'Saturday'])
    
    kpis = [
        ('TOTAL TRIPS', f'{total_trips:,}', COLORS['primary']),
        ('UNIQUE VEHICLES', f'{total_vehicles:,}', COLORS['success']),
        ('AVG SPEED', f'{avg_speed:.1f} km/h', COLORS['warning']),
        ('SATURDAY TRIPS', f'{saturday_trips:,}', COLORS['highlight'])
    ]
    
    for i, (title, value, color) in enumerate(kpis):
        ax = fig.add_subplot(gs[0, i])
        ax.text(0.5, 0.6, value, ha='center', va='center', fontsize=28, fontweight='bold', color=color)
        ax.text(0.5, 0.25, title, ha='center', va='center', fontsize=11, fontweight='bold', 
                color=COLORS['neutral'])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_facecolor(COLORS['background'])
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(color)
            spine.set_linewidth(3)
    
    # Hourly chart (middle left)
    ax2 = fig.add_subplot(gs[1, :2])
    hourly = df.groupby('hour')['vehicle_id'].count()
    colors = [COLORS['highlight'] if h == 20 else COLORS['primary'] for h in hourly.index]
    ax2.bar(hourly.index, hourly.values, color=colors, edgecolor='white')
    ax2.set_title('Hourly Traffic (8PM Highlighted)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Hour')
    ax2.set_ylabel('Trips')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.set_facecolor('#FAFAFA')
    
    # Weekly chart (middle right)
    ax3 = fig.add_subplot(gs[1, 2:])
    day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    daily = df.groupby('day_name')['vehicle_id'].count()
    daily_sorted = [daily.get(d.replace(d[:3], d), 0) for d in 
                    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]
    colors = [COLORS['highlight'] if i == 5 else COLORS['teal'] for i in range(7)]
    ax3.bar(day_order, daily_sorted, color=colors, edgecolor='white')
    ax3.set_title('Weekly Pattern (Saturday Highlighted)', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Day')
    ax3.set_ylabel('Trips')
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    ax3.set_facecolor('#FAFAFA')
    
    # Route breakdown (bottom)
    ax4 = fig.add_subplot(gs[2, :2])
    route_trips = df.groupby('route')['vehicle_id'].count().sort_values(ascending=True)
    colors = [ROUTE_COLORS.get(r, COLORS['primary']) for r in route_trips.index]
    ax4.barh(route_trips.index, route_trips.values, color=colors, edgecolor='white')
    ax4.set_title('Route Traffic Volume', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Trips')
    ax4.grid(axis='x', alpha=0.3, linestyle='--')
    ax4.set_facecolor('#FAFAFA')
    
    # Speed by route (bottom right)
    ax5 = fig.add_subplot(gs[2, 2:])
    route_speed = df.groupby('route')['speed_kmph'].mean().sort_values(ascending=True)
    colors = [ROUTE_COLORS.get(r, COLORS['primary']) for r in route_speed.index]
    ax5.barh(route_speed.index, route_speed.values, color=colors, edgecolor='white')
    ax5.set_title('Average Speed by Route', fontsize=12, fontweight='bold')
    ax5.set_xlabel('Speed (km/h)')
    ax5.grid(axis='x', alpha=0.3, linestyle='--')
    ax5.set_facecolor('#FAFAFA')
    
    fig.suptitle('SMART CITY TRANSPORT - POWER BI DASHBOARD', 
                 fontsize=20, fontweight='bold', color=COLORS['secondary'], y=0.98)
    
    plt.savefig(os.path.join(OUTPUT_DIR, 'powerbi_dashboard.png'), dpi=200,
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ Created: powerbi_dashboard.png")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=" * 60)
    print("Generating Power BI Style Traffic Visualizations...")
    print("=" * 60)
    
    df = load_data()
    
    create_hourly_traffic_chart(df)
    create_weekly_pattern_chart(df)
    create_route_peak_analysis(df)
    create_saturday_route_analysis(df)
    create_dashboard_summary(df)
    
    print("=" * 60)
    print(f"✅ All Power BI charts saved to: {OUTPUT_DIR}/")
    print("=" * 60)
