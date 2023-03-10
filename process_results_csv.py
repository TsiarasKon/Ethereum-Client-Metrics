import sys
import psutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os


def convert_bytes(bytes, output_unit, input_unit='b'):
    unit_divisors = {
        'b': 0,
        'KB': 10,
        'MB': 20,
        'GB': 30
    }
    if output_unit not in unit_divisors or input_unit not in unit_divisors:
        raise IndexError(f"Conversion units must be in {unit_divisors}")
    divisor = unit_divisors[output_unit] - unit_divisors[input_unit]
    return bytes / float(1 << divisor)


start_date = '2023-01-01'
sys_memory = psutil.virtual_memory().total

if len(sys.argv) < 2:
    print(
        "Please run like './process_results_csv.py <results.csv> [start-date]'")
    sys.exit()

filename = sys.argv[1]
if len(sys.argv) == 3:
    start_date = sys.argv[2]

df = pd.read_csv(filename, delim_whitespace=True, usecols=[
                 'Time', '%CPU', '%MEM', 'kB_rd/s', 'kB_wr/s', 'kbps_sent', 'kbps_rec', 'disk_used'])

# Convert columns to MB or GB accordingly
df['MEM'] = df['%MEM'] * convert_bytes(sys_memory, "GB") / 100
df['Reads'] = df['kB_rd/s'].map(lambda val: convert_bytes(val, "MB", "KB"))
df['Writes'] = df['kB_wr/s'].map(lambda val: convert_bytes(val, "MB", "KB"))
df['Sent'] = df['kbps_sent'].map(lambda val: convert_bytes(val, "MB", "KB"))
df['Received'] = df['kbps_rec'].map(lambda val: convert_bytes(val, "MB", "KB"))
df['Disk'] = df['disk_used'].map(lambda val: convert_bytes(val, "GB", "KB"))
df.rename(columns={'%CPU': 'CPU'}, inplace=True)
df.drop(['%MEM', 'kB_rd/s', 'kB_wr/s', 'kbps_sent', 'kbps_rec', 'disk_used'], axis=1, inplace=True)

# Insert dates in front of 'Time' col:
# (looping a df is terrible efficiency-wise, but it's good enough here)
datetime_col = [pd.to_datetime(f"{start_date} {df.iloc[0]['Time']}")]
for i in range(1, len(df.index)):
    i_time = df.iloc[i]['Time']
    if i_time < df.iloc[i-1]['Time']:
        datetime_col.append(pd.to_datetime(
            f"{datetime_col[i-1].date()} {i_time}") + pd.DateOffset(1))
        print(pd.to_datetime(
            f"{datetime_col[i-1].date()} {i_time}") + pd.DateOffset(1))
    else:
        datetime_col.append(pd.to_datetime(
            f"{datetime_col[i-1].date()} {i_time}"))
        print(pd.to_datetime(f"{datetime_col[i-1].date()} {i_time}"))
df['Time2'] = pd.Series(datetime_col)

# Account for missing rows:
df.set_index('Time2', inplace=True)
date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='S')
df = df[~df.index.duplicated()]
df = df.reindex(date_range).ffill()
df.reset_index(inplace=True, names=['Datetime'])

print(df)
df.to_csv("p_" + filename.split(os.sep)[-1], index=False)
