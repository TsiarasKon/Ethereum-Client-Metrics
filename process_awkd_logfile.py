import sys
import psutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

start_date = '2023-01-01'

if len(sys.argv) < 2:
    print(
        "Please run like './process_awkd_logfile.py <logfile.csv> [start-date]'")
    sys.exit()

filename = sys.argv[1]
if len(sys.argv) == 3:
    start_date = sys.argv[2]

df = pd.read_csv(filename, delim_whitespace=True, names=['Time', 'Peers'])

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
df.set_index('Time2', inplace=True)
del df['Time']

# Account for missing rows:
date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='S')
df = df[~df.index.duplicated()]
df = df.reindex(date_range).ffill()
df.reset_index(inplace=True, names=['Datetime'])

df['Peers'] = df['Peers'].astype('int')
print(df)
df.to_csv("p_" + filename.split(os.sep)[-1], index=False)
