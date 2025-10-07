import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 10

# Load data
df = pd.read_csv('data/annual_metropolitan_train_station_entries_fy_2024_2025.csv')

# Create figure with 4 subplots
fig, axes = plt.subplots(2, 2, figsize=(18, 12))
fig.suptitle('Melbourne Metro Train Station Patronage Analysis - FY 2024-25', 
             fontsize=18, fontweight='bold', y=0.995)

# ============================================
# PLOT 1: Top 20 Busiest Stations
# ============================================
top_20 = df.nlargest(20, 'Pax_annual').sort_values('Pax_annual')
colors_top20 = plt.cm.Blues(range(len(top_20), 0, -1))

axes[0, 0].barh(range(len(top_20)), top_20['Pax_annual']/1000000, color=colors_top20)
axes[0, 0].set_yticks(range(len(top_20)))
axes[0, 0].set_yticklabels(top_20['Stop_name'], fontsize=9)
axes[0, 0].set_xlabel('Annual Patronage (Millions)', fontsize=11, fontweight='bold')
axes[0, 0].set_title('Top 20 Busiest Metro Stations', fontsize=13, fontweight='bold', pad=10)
axes[0, 0].grid(axis='x', alpha=0.3)

# Add value labels
for i, (idx, row) in enumerate(top_20.iterrows()):
    axes[0, 0].text(row['Pax_annual']/1000000 + 0.05, i, f"{row['Pax_annual']/1000000:.1f}M", 
                    va='center', fontsize=8)

# ============================================
# PLOT 2: Time of Day Distribution (Pie Chart)
# ============================================
time_cols = ['Pax_pre_AM_peak', 'Pax_AM_peak', 'Pax_interpeak', 'Pax_PM_peak', 'Pax_PM_late']
time_totals = [df[col].sum() for col in time_cols]
time_labels = ['Pre-AM Peak\n(before 7am)', 'AM Peak\n(7-9am)', 
               'Interpeak\n(9am-4pm)', 'PM Peak\n(4-7pm)', 'PM Late\n(after 7pm)']
colors_time = ['#E8F4F8', '#FFB347', '#90EE90', '#FF6B6B', '#C77DFF']

wedges, texts, autotexts = axes[0, 1].pie(time_totals, labels=time_labels, autopct='%1.1f%%', 
                                           colors=colors_time, startangle=90, 
                                           textprops={'fontsize': 10})
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(11)

axes[0, 1].set_title('System-Wide Patronage by Time of Day', 
                     fontsize=13, fontweight='bold', pad=10)

# ============================================
# PLOT 3: Weekday vs Weekend Distribution
# ============================================
day_data = [df['Pax_weekday'].sum()/1000000, 
            df['Pax_Saturday'].sum()/1000000, 
            df['Pax_Sunday'].sum()/1000000]
day_labels = ['Weekday', 'Saturday', 'Sunday']
colors_days = ['#4A90E2', '#F39C12', '#2ECC71']

bars = axes[1, 0].bar(day_labels, day_data, color=colors_days, edgecolor='black', linewidth=1.5)
axes[1, 0].set_ylabel('Total Patronage (Millions)', fontsize=11, fontweight='bold')
axes[1, 0].set_title('Patronage Distribution by Day Type', fontsize=13, fontweight='bold', pad=10)
axes[1, 0].grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar, value in zip(bars, day_data):
    height = bar.get_height()
    axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.1f}M\n({value/sum(day_data)*100:.1f}%)',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

# ============================================
# PLOT 4: Geographic Distribution (Scatter)
# ============================================
scatter = axes[1, 1].scatter(df['Stop_long'], df['Stop_lat'], 
                             s=df['Pax_annual']/2000, 
                             c=df['Pax_annual'], 
                             cmap='YlOrRd', 
                             alpha=0.6, 
                             edgecolors='black', 
                             linewidth=0.5)

# Annotate top 5 stations
top_5 = df.nlargest(5, 'Pax_annual')
for _, row in top_5.iterrows():
    axes[1, 1].annotate(row['Stop_name'], 
                       xy=(row['Stop_long'], row['Stop_lat']),
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=8, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

axes[1, 1].set_xlabel('Longitude', fontsize=11, fontweight='bold')
axes[1, 1].set_ylabel('Latitude', fontsize=11, fontweight='bold')
axes[1, 1].set_title('Geographic Distribution of Stations\n(Size = Patronage)', 
                     fontsize=13, fontweight='bold', pad=10)

# Add colorbar
cbar = plt.colorbar(scatter, ax=axes[1, 1])
cbar.set_label('Annual Patronage', fontsize=10, fontweight='bold')

# ============================================
# Final adjustments and save
# ============================================
plt.tight_layout()
plt.savefig('visuals/melbourne_metro_analysis.png', dpi=300, bbox_inches='tight', facecolor='white')
print("\n✓ Visualization saved: visuals/melbourne_metro_analysis.png")
print("  Check your 'visuals' folder to see the chart!")

plt.show()