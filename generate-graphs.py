import sys
import pandas as pd
import matplotlib.pyplot as plt
import psutil

# TODO: seaborn
def plot_line_graph(col, title, ylabel, xlabel="Time"):
    plt.plot(data[col])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def plot_2line_graph(col, col2, title, ylabel, xlabel="Time"):
    # TODO: refactor
    plt.plot(data[col])
    plt.plot(data[col2])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

if len(sys.argv) != 2:
    print("Please run like './generate-graphs.py <results.csv>'")
    sys.exit()
filename = str(sys.argv[1])
sys_memory = psutil.virtual_memory().total    # TODO: convert 
print(sys_memory)

# Read pidstat output from file
data = pd.read_csv(filename, delim_whitespace=True)
# Convert time column to datetime and set as index
data["Time"] = pd.to_datetime(data["Time"], format="%H:%M:%S")
data.set_index("Time", inplace=True)
# TODO: convert cols: bytes -> GB, kbps -> Mbps, MEM -> perc * actual
print(data)
print(data.columns)

plot_line_graph("%CPU", "CPU usage over time", "CPU Usage (%)")
plot_line_graph("%MEM", "RAM usage over time", "RAM Usage (%)")
plot_line_graph("disk_used", "Disk usage over time", "Bytes")
plot_2line_graph("kB_rd/s", "kB_wr/s", "Disk I/O over time", "kBps")
plot_2line_graph("kbps_sent", "kbps_rec", "Network traffic over time", "kbps")
