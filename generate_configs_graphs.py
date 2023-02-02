import sys
import psutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from thesis_configs import CONFIGS, CONFIG_ALL

INTERVAL = 120   # in seconds
ROOT_DIR = './csv/'

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


def plot_col_multidf(config, df_list, col, title, ylabel):
    longest_df = max(df_list, key=lambda x: len(x))
    fig, ax = plt.subplots(constrained_layout=True)
    ax.xaxis.set_major_formatter(hours_formatter)
    ax.set_xticks(
        [sec for sec in longest_df.index[::config['time_ticks_step']]])
    for run, df in zip(config['runs'], df_list):
        ax.plot(df.index, df[col], label=run['name'], zorder=5)
        for event in run['events']:
            x_index = event['x'] // INTERVAL
            marker_label = event['config']['name'] if run == config['runs'][-1] else "_nolegend_"
            # TODO: labels if client == ALL?
            ax.scatter(df.index[x_index], df.iloc[x_index][col], marker=event['config']['marker'],
                       color=event['config']['color'], s=event['config']['size'], label=marker_label, zorder=10)

    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Time (hours)")
    plt.grid('on', linestyle='--')
    plt.legend()
    # plt.savefig(f"{client}_{col}.png")
    plt.savefig(f"{col}.png")
    # plt.show()


def load_df(run_config, sys_memory):
    df = pd.read_csv(ROOT_DIR + run_config['filename'], delim_whitespace=True, usecols=[
                     '%CPU', '%MEM', 'kB_rd/s', 'kB_wr/s', 'kbps_sent', 'kbps_rec', 'disk_used'])
    if run_config['trim_rows'] is not None:
        df = df[:-run_config['trim_rows']]

    # Index df with timedeltas and average rows by INTERVAL
    df['seconds_delta'] = pd.to_timedelta(df.index, unit="S").total_seconds()
    df = df.groupby(df.index // INTERVAL).mean(numeric_only=False)
    df.set_index('seconds_delta', inplace=True)

    # Convert columns to MB or GB accordingly
    df['MEM'] = df['%MEM'] * convert_bytes(sys_memory, "GB") / 100
    df['Reads'] = df['kB_rd/s'].map(lambda val: convert_bytes(val, "MB", "KB"))
    df['Writes'] = df['kB_wr/s'].map(
        lambda val: convert_bytes(val, "MB", "KB"))
    df['Sent'] = df['kbps_sent'].map(
        lambda val: convert_bytes(val, "MB", "KB"))
    df['Received'] = df['kbps_rec'].map(
        lambda val: convert_bytes(val, "MB", "KB"))
    df['Disk'] = df['disk_used'].map(
        lambda val: convert_bytes(val, "GB", "KB"))
    df.rename(columns={'%CPU': 'CPU'}, inplace=True)
    return df


if len(sys.argv) != 2 or str(sys.argv[1]) not in [*CONFIGS.keys(), 'ALL']:
    print("Please run like './generate-thesis-config.py <Geth|Nethermind|Besu|Erigon|ALL>'")
    sys.exit()

client = str(sys.argv[1])
config = CONFIG_ALL if client == "ALL" else CONFIGS[client]
sys_memory = psutil.virtual_memory().total
df_list = list(map(lambda run: load_df(run, sys_memory), config['runs']))

# Plots
sns.set()   # TODO - keep?
plot_col_multidf(config, df_list, 'CPU', "CPU usage over time", "%")
plot_col_multidf(config, df_list, 'MEM', "RAM usage over time", "GB")
plot_col_multidf(config, df_list, 'Disk',
                 "Chain data disk size over time", "GB")
plot_col_multidf(config, df_list, 'Reads',
                 "Disk Reads over time", "MB per second")
plot_col_multidf(config, df_list, 'Writes',
                 "Disk Writes over time", "MB per second")
plot_col_multidf(config, df_list, 'Sent',
                 "Network - Sent data over time", "MB per second")
plot_col_multidf(config, df_list, 'Received',
                 "Network - Received data over time", "MB per second")
