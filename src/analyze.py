import pandas as pd
from datetime import date, timedelta

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

# Time of day analysis - system-wide.
# NOTE: Pax_pre_AM_peak ... Pax_PM_late are AVERAGE entries on a typical
# weekday, so together they describe the shape of one weekday. Shares are taken
# against the sum of the bands (one weekday), NOT against Pax_annual.
print("\n--- WHEN DO PEOPLE TRAVEL? (share of a typical weekday) ---")
total_pre_am = df['Pax_pre_AM_peak'].sum()
total_am = df['Pax_AM_peak'].sum()
total_inter = df['Pax_interpeak'].sum()
total_pm = df['Pax_PM_peak'].sum()
total_late = df['Pax_PM_late'].sum()
band_total = total_pre_am + total_am + total_inter + total_pm + total_late

print(f"Pre-AM Peak:  {total_pre_am/band_total*100:5.1f}%")
print(f"AM Peak:      {total_am/band_total*100:5.1f}%")
print(f"Interpeak:    {total_inter/band_total*100:5.1f}%")
print(f"PM Peak:      {total_pm/band_total*100:5.1f}%")
print(f"PM Late:      {total_late/band_total*100:5.1f}%")
print(f"AM + PM peak combined: {(total_am + total_pm)/band_total*100:.1f}%")

# Weekday vs Weekend (annual share).
# NOTE: Pax_weekday / Pax_Saturday / Pax_Sunday are AVERAGE entries per day of
# each type. To get the annual patronage share each daily average must be
# weighted by how many of that day type occur in the financial year -- a year
# has ~261 weekdays but only ~52 Saturdays and ~52 Sundays, so comparing the
# raw averages 1:1 massively overstates the weekend.
print("\n--- WEEKDAY VS WEEKEND (annual share) ---")
day_counts = {i: 0 for i in range(7)}  # Mon=0 .. Sun=6
d = date(2024, 7, 1)                    # FY24-25: 1 Jul 2024 - 30 Jun 2025
while d <= date(2025, 6, 30):
    day_counts[d.weekday()] += 1
    d += timedelta(days=1)
n_weekday = sum(day_counts[i] for i in range(5))
n_sat, n_sun = day_counts[5], day_counts[6]

annual_weekday = df['Pax_weekday'].sum() * n_weekday
annual_sat = df['Pax_Saturday'].sum() * n_sat
annual_sun = df['Pax_Sunday'].sum() * n_sun
annual_total = annual_weekday + annual_sat + annual_sun

print(f"  (FY24-25: {n_weekday} weekdays, {n_sat} Saturdays, {n_sun} Sundays)")
print(f"Weekday:       {annual_weekday/annual_total*100:5.1f}%")
print(f"Saturday:      {annual_sat/annual_total*100:5.1f}%")
print(f"Sunday:        {annual_sun/annual_total*100:5.1f}%")
print(f"Weekend total: {(annual_sat + annual_sun)/annual_total*100:5.1f}%")

# Most peak-dependent stations (ranking by share of that station's own weekday
# average that falls in the AM / PM peak band).
print("\n--- STATIONS WITH HIGHEST AM PEAK CONCENTRATION ---")
weekday_avg = (df['Pax_pre_AM_peak'] + df['Pax_AM_peak'] + df['Pax_interpeak']
               + df['Pax_PM_peak'] + df['Pax_PM_late'])
df['am_peak_pct'] = (df['Pax_AM_peak'] / weekday_avg * 100)
top_am = df.nlargest(5, 'am_peak_pct')[['Stop_name', 'am_peak_pct', 'Pax_AM_peak']]
for name, pct, pax in top_am.values:
    print(f"{name:30s} {pct:5.1f}% ({pax:>8,} AM peak pax)")

print("\n--- STATIONS WITH HIGHEST PM PEAK CONCENTRATION ---")
df['pm_peak_pct'] = (df['Pax_PM_peak'] / weekday_avg * 100)
top_pm = df.nlargest(5, 'pm_peak_pct')[['Stop_name', 'pm_peak_pct', 'Pax_PM_peak']]
for name, pct, pax in top_pm.values:
    print(f"{name:30s} {pct:5.1f}% ({pax:>8,} PM peak pax)")

# Weekend stations: annual weekend share per station (weighted by day counts).
print("\n--- TOP 10 WEEKEND-HEAVY STATIONS ---")
station_weekend = df['Pax_Saturday'] * n_sat + df['Pax_Sunday'] * n_sun
station_annual = (df['Pax_weekday'] * n_weekday + df['Pax_Saturday'] * n_sat
                  + df['Pax_Sunday'] * n_sun)
df['weekend_pct'] = station_weekend / station_annual * 100
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
