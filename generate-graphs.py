import sys
import pandas as pd
import matplotlib.pyplot as plt
import psutil

def convert_bytes(bytes, output_unit, input_unit='b'):
    unit_divisors = {
        'b': 0,
        'KB': 10,
        'MB': 20,
        'GB': 30
    }
    if output_unit not in unit_divisors or input_unit not in unit_divisors:
        raise IndexError(f"Conversion units must in {unit_divisors}")
    divisor = unit_divisors[output_unit] - unit_divisors[input_unit]
    return bytes / float(1 << divisor)

# TODO: seaborn
def plot_line_graph(col, title, ylabel, xlabel='Time'):
    plt.plot(df[col])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
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

# Read pidstat output from file
df = pd.read_csv(filename, delim_whitespace=True)
# Convert time column to datetime and set as index
# df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S')
df['Time'] = pd.to_timedelta(df['Time'])    # TODO: fix needed for when day resets
df.set_index('Time', inplace=True)
df['%MEM'] *= convert_bytes(sys_memory, "GB") / 100
df['disk_used'] = df['disk_used'].map(lambda val: convert_bytes(val, "GB", "KB"))
df['kB_rd/s'] = df['kB_rd/s'].map(lambda val: convert_bytes(val, "MB", "KB"))
df['kB_wr/s'] = df['kB_wr/s'].map(lambda val: convert_bytes(val, "MB", "KB"))
df['kbps_sent'] = df['kbps_sent'].map(lambda val: convert_bytes(val, "MB", "KB"))
df['kbps_rec'] = df['kbps_rec'].map(lambda val: convert_bytes(val, "MB", "KB"))
print(df)
print(df["disk_used"])
print(df.columns)

plot_line_graph("%CPU", "CPU usage over time", "CPU Usage (%)")
plot_line_graph("%MEM", "RAM usage over time", "RAM Usage (GB)")
plot_line_graph("disk_used", "Disk usage over time", "GB")
plot_2line_graph("kB_rd/s", "kB_wr/s", "Disk I/O over time", "kBps")
plot_2line_graph("kbps_sent", "kbps_rec", "Network traffic over time", "kbps")
