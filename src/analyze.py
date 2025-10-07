import pandas as pd

# Load data
df = pd.read_csv('data/annual_metropolitan_train_station_entries_fy_2024_2025.csv')

print("="*80)
print("MELBOURNE METRO STATION ANALYSIS - FY 2024-25")
print("="*80)

# Top 10 busiest stations
print("\n--- TOP 10 BUSIEST STATIONS ---")
top_10 = df.nlargest(10, 'Pax_annual')[['Stop_name', 'Pax_annual']]
for i, (name, pax) in enumerate(top_10.values, 1):
    print(f"{i:2d}. {name:30s} {pax:>10,} passengers/year")

# Bottom 10 quietest stations
print("\n--- BOTTOM 10 QUIETEST STATIONS ---")
bottom_10 = df.nsmallest(10, 'Pax_annual')[['Stop_name', 'Pax_annual']]
for i, (name, pax) in enumerate(bottom_10.values, 1):
    print(f"{i:2d}. {name:30s} {pax:>10,} passengers/year")

# Time of day analysis - system-wide
print("\n--- WHEN DO PEOPLE TRAVEL? (System-wide) ---")
total_pre_am = df['Pax_pre_AM_peak'].sum()
total_am = df['Pax_AM_peak'].sum()
total_inter = df['Pax_interpeak'].sum()
total_pm = df['Pax_PM_peak'].sum()
total_late = df['Pax_PM_late'].sum()
total_all = df['Pax_annual'].sum()

print(f"Pre-AM Peak:  {total_pre_am/total_all*100:5.1f}% ({total_pre_am:>12,} passengers)")
print(f"AM Peak:      {total_am/total_all*100:5.1f}% ({total_am:>12,} passengers)")
print(f"Interpeak:    {total_inter/total_all*100:5.1f}% ({total_inter:>12,} passengers)")
print(f"PM Peak:      {total_pm/total_all*100:5.1f}% ({total_pm:>12,} passengers)")
print(f"PM Late:      {total_late/total_all*100:5.1f}% ({total_late:>12,} passengers)")

# Weekday vs Weekend
print("\n--- WEEKDAY VS WEEKEND ---")
total_weekday = df['Pax_weekday'].sum()
total_sat = df['Pax_Saturday'].sum()
total_sun = df['Pax_Sunday'].sum()

print(f"Weekday:      {total_weekday/total_all*100:5.1f}% ({total_weekday:>12,} passengers)")
print(f"Saturday:     {total_sat/total_all*100:5.1f}% ({total_sat:>12,} passengers)")
print(f"Sunday:       {total_sun/total_all*100:5.1f}% ({total_sun:>12,} passengers)")

# Most peak-dependent stations
print("\n--- STATIONS WITH HIGHEST AM PEAK CONCENTRATION ---")
df['am_peak_pct'] = (df['Pax_AM_peak'] / df['Pax_annual'] * 100)
top_am = df.nlargest(5, 'am_peak_pct')[['Stop_name', 'am_peak_pct', 'Pax_AM_peak']]
for name, pct, pax in top_am.values:
    print(f"{name:30s} {pct:5.1f}% ({pax:>8,} AM peak pax)")

print("\n--- STATIONS WITH HIGHEST PM PEAK CONCENTRATION ---")
df['pm_peak_pct'] = (df['Pax_PM_peak'] / df['Pax_annual'] * 100)
top_pm = df.nlargest(5, 'pm_peak_pct')[['Stop_name', 'pm_peak_pct', 'Pax_PM_peak']]
for name, pct, pax in top_pm.values:
    print(f"{name:30s} {pct:5.1f}% ({pax:>8,} PM peak pax)")

# Weekend stations
print("\n--- TOP 10 WEEKEND-HEAVY STATIONS ---")
df['weekend_pct'] = ((df['Pax_Saturday'] + df['Pax_Sunday']) / df['Pax_annual'] * 100)
top_weekend = df.nlargest(10, 'weekend_pct')[['Stop_name', 'weekend_pct']]
for name, pct in top_weekend.values:
    print(f"{name:30s} {pct:5.1f}% weekend usage")

print("\n" + "="*80)
print("INSIGHTS SO FAR:")
print("="*80)
print("1. Huge variation between busiest and quietest stations")
print("2. Clear peak hour patterns - can we optimize service frequency?")
print("3. Some stations are heavily weekend-oriented - tourist/leisure destinations?")
print("4. Different travel patterns suggest different service strategies needed")