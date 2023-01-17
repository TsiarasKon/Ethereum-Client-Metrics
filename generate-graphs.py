import sys
import psutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

INTERVAL = 60   # in seconds

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

@mticker.FuncFormatter
def hhmmss_formatter(seconds, pos=None):
    # As opposed to strftime format, it supports h > 23
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f'{h:02d}:{m:02d}:{s:02d}'

def plot_line_graph(col, title, ylabel, xlabel='Time'):
    fig, ax = plt.subplots(constrained_layout=True)
    ax.xaxis.set_major_formatter(hhmmss_formatter)
    ax.plot(df.index, df[col])
    ax.set_title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.show()

def plot_2line_graph(col, col2, title, ylabel, xlabel='Time'):
    # TODO: refactor
    plt.plot(df[col])
    plt.plot(df[col2])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

if len(sys.argv) != 2:
    print("Please run like './generate-graphs.py <results.csv>'")
    sys.exit()

filename = str(sys.argv[1])
sys_memory = psutil.virtual_memory().total

df = pd.read_csv(filename, delim_whitespace=True, usecols=['%CPU', '%MEM', 'kB_rd/s', 'kB_wr/s', 'kbps_sent', 'kbps_rec', 'disk_used'])
# Index df with timedeltas and average rows by INTERVAL
df['seconds_delta'] = pd.to_timedelta(df.index, unit="S").total_seconds()
df = df.groupby(df.index // INTERVAL).mean(numeric_only=False)
df.set_index('seconds_delta', inplace=True)

# Convert columns to MB or GB accordingly
df['%MEM'] *= convert_bytes(sys_memory, "GB") / 100
df['kB_rd/s'] = df['kB_rd/s'].map(lambda val: convert_bytes(val, "MB", "KB"))
df['kB_wr/s'] = df['kB_wr/s'].map(lambda val: convert_bytes(val, "MB", "KB"))
df['kbps_sent'] = df['kbps_sent'].map(lambda val: convert_bytes(val, "MB", "KB"))
df['kbps_rec'] = df['kbps_rec'].map(lambda val: convert_bytes(val, "MB", "KB"))
df['disk_used'] = df['disk_used'].map(lambda val: convert_bytes(val, "GB", "KB"))
print(df)

# Plots
plot_line_graph("%CPU", "CPU usage over time", "CPU Usage (%)")
plot_line_graph("%MEM", "RAM usage over time", "RAM Usage (GB)")
plot_line_graph("disk_used", "Disk usage over time", "GB")
plot_2line_graph("kB_rd/s", "kB_wr/s", "Disk I/O over time", "MBps")
plot_2line_graph("kbps_sent", "kbps_rec", "Network traffic over time", "MBps")
