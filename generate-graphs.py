import sys
import psutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns


@mticker.FuncFormatter
def hhmm_formatter(seconds, pos=None):
    # As opposed to strftime format, it supports h > 23
    m, _ = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    # return f'{h:02d}:{m:02d}:{s:02d}'
    return f'{h:02d}:{m:02d}'

@mticker.FuncFormatter
def hours_formatter(seconds, pos=None):
    # As opposed to strftime format, it supports h > 23
    m, _ = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return str(h)


ROW_CUTOFF = None  # if not None, use df[:ROW_CUTOFF] for everything
INTERVAL = 60   # in seconds
CONFIGS = {
    'Geth': {
        'TIME_TICKS_STEP': 180,
        'TIME_FORMATTER': hours_formatter,
        'TIME_LABEL': "Time (hours)",
    },
    'Nethermind': {
        'TIME_TICKS_STEP': 60,
        'TIME_FORMATTER': hhmm_formatter,
        'TIME_LABEL': "Time (hours:minutes)",
    },
    'Besu': {
        'TIME_TICKS_STEP': 60,
        'TIME_FORMATTER': hours_formatter,
        'TIME_LABEL': "Time (hours)",
    },
    'Erigon': {
        'TIME_TICKS_STEP': 60,
        'TIME_FORMATTER': hours_formatter,
        'TIME_LABEL': "Time (hours)",
    },
}
# Hard-coded events (based on clients' log outputs), to be marked with vertical lines in plots:
EVENTS = {
    'Geth': {
        'Began state heal (22:21)': dict({ 'x': 80469, 'color': 'green', 'linestyle':':' }),     # 22:16:47
        'Sync competed (22:41)': dict({ 'x': 81625, 'color': 'gray', 'linestyle':'-' }),     # 22:36:53
    },
    'Nethermind': {
        # 'Beacon headers sync (time)': dict({ 'x': 4000, 'color': 'm', 'linestyle':':' }),
        'Sync competed (time)': dict({ 'x': 18000, 'color': 'gray', 'linestyle':'-' }),
    },
    'Besu': {
    },
    'Erigon': {
    },
}

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

def plot_lines(cols, title, ylabel):
    fig, ax = plt.subplots(constrained_layout=True)
    ax.xaxis.set_major_formatter(TIME_FORMATTER)
    if len(cols) > 1:
        for col in cols:
            ax.plot(df.index, df[col])
    else:
        ax.plot(df.index, df[cols[0]], label='_nolegend_')
    ax.set_xticks([sec for sec in df.index[::TIME_TICKS_STEP]])
    for event, val_dict in EVENTS[client].items():
        plt.axvline(label=event, **val_dict)

    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(TIME_LABEL)
    # plt.xticks(rotation=45)
    plt.legend([*cols, *EVENTS[client].keys()] if len(cols) > 1 else [*EVENTS[client].keys()])
    plt.grid('on', linestyle='--')
    plt.savefig(cols[0])
    plt.show()

if len(sys.argv) != 3 or str(sys.argv[1]) not in EVENTS.keys():
    print("Please run like './generate-graphs.py <Geth|Nethermind|Besu|Erigon> <results.csv>'")
    sys.exit()

client = str(sys.argv[1])
filename = str(sys.argv[2])
TIME_TICKS_STEP = CONFIGS[client]['TIME_TICKS_STEP']
TIME_FORMATTER = CONFIGS[client]['TIME_FORMATTER']
TIME_LABEL = CONFIGS[client]['TIME_LABEL']
sys_memory = psutil.virtual_memory().total
sns.set()

# Read csv and prune it if ROW_CUTOFF defined 
df = pd.read_csv(filename, delim_whitespace=True, usecols=['%CPU', '%MEM', 'kB_rd/s', 'kB_wr/s', 'kbps_sent', 'kbps_rec', 'disk_used'])
if ROW_CUTOFF is not None:
    df = df[:ROW_CUTOFF]

# Index df with timedeltas and average rows by INTERVAL
df['seconds_delta'] = pd.to_timedelta(df.index, unit="S").total_seconds()
df = df.groupby(df.index // INTERVAL).mean(numeric_only=False)
df.set_index('seconds_delta', inplace=True)

# Convert columns to MB or GB accordingly
df['MEM'] = df['%MEM'] * convert_bytes(sys_memory, "GB") / 100
df['Reads'] = df['kB_rd/s'].map(lambda val: convert_bytes(val, "MB", "KB"))
df['Writes'] = df['kB_wr/s'].map(lambda val: convert_bytes(val, "MB", "KB"))
df['Sent'] = df['kbps_sent'].map(lambda val: convert_bytes(val, "MB", "KB"))
df['Received'] = df['kbps_rec'].map(lambda val: convert_bytes(val, "MB", "KB"))
df['disk_used'] = df['disk_used'].map(lambda val: convert_bytes(val, "GB", "KB"))
print(df)

# Plots
plot_lines(["%CPU"], "CPU usage over time", "%")
plot_lines(["MEM"], "RAM usage over time", "GB")
plot_lines(["disk_used"], "Chain data disk size over time", "GB")
plot_lines(["Reads", "Writes"], "Disk I/O over time", "MB per second")
plot_lines(["Sent", "Received"], "Network traffic over time", "MB per second")
