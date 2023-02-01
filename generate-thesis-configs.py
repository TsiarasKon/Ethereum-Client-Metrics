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
            marker_label = event['name'] if run == config['runs'][-1] else "_nolegend_"
            ax.scatter(df.index[x_index], df.iloc[x_index][col], marker=event['marker'],
                       color=event['color'], s=event['size'], label=marker_label, zorder=10)

    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Time (hours)")
    plt.grid('on', linestyle='--')
    plt.legend()
    # plt.savefig(f"{client}_{col}.png")
    plt.savefig(f"{col}.png")
    # plt.show()


def load_df(run_config, sys_memory):
    df = pd.read_csv(run_config['filename'], delim_whitespace=True, usecols=[
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


INTERVAL = 120   # in seconds
ROOT_DIR = './csv/'

# Hard-coded events (based on clients' log outputs in ROOT_DIR)
CONFIGS = {
    'Geth': {
        'time_ticks_step': 90,
        'runs': [{
            'name': 'Geth_1',
            'filename': ROOT_DIR + 'metrics_24_01_geth_128_def.csv',
            'trim_rows': None,
            'events': [{
                'name': 'Began state heal',
                'time': '22:16:47',
                'delta_time': '22:21',
                'x': 80469,
                'marker': 'x',
                'color': 'green',
                'size': 50
            }, {
                'name': 'Sync competed',
                'time': '22:36:53',
                'delta_time': '22:41',
                'x': 81625,
                'marker': '|',
                'color': 'black',
                'size': 50
            }]
        }, {
            'name': 'Geth_2',
            'filename': ROOT_DIR + 'metrics_20_01_geth.csv',
            'trim_rows': 22000,
            'events': [{
                'name': 'Began state heal',
                'time': '22:16:47',
                'delta_time': '22:21',
                'x': 70469,
                'marker': 'x',
                'color': 'green',
                'size': 80
            }, {
                'name': 'Sync competed',
                'time': '22:36:53',
                'delta_time': '22:41',
                'x': 71625,
                'marker': '|',
                'color': 'black',
                'size': 100
            }]
        }]
    },
    'Nethermind': {
        'time_ticks_step': 120,
        'runs': [{
            'name': 'Nethermind_1',
            'filename': ROOT_DIR + 'metrics_23_01_nethermind_snap_128_4096.csv',
            'trim_rows': 10800,
            'events': {}
        }, {
            'name': 'Nethermind_2',
            'filename': ROOT_DIR + 'metrics_28_01_nethermind_fast_128_4096.csv',
            'trim_rows': 7200,
            'events': {}
        }]
    },
    'Besu': {
        'time_ticks_step': 60,
        'runs': [{
            'name': 'Besu_1',
            'filename': ROOT_DIR + 'metrics_18_01_besu.csv',
            'trim_rows': 8000,
            'events': {}
        }, {
            'name': 'Besu_2',
            'filename': ROOT_DIR + 'metrics_21_01_besu_checkpoint.csv',
            'trim_rows': 20000,
            'events': {}
        }, {
            'name': 'Besu_3',
            'filename': ROOT_DIR + 'metrics_29_01_besu_snap_noBonsai.csv',
            'trim_rows': 2500,
            'events': {}
        }, {
            'name': 'Besu_4',
            'filename': ROOT_DIR + 'metrics_25_01_besu_noBonsai.csv',
            'trim_rows': 65000,
            'events': {}
        }]
    },
    'Erigon': {
        'time_ticks_step': 240,
    },
}
CONFIG_ALL = {
    'time_ticks_step': 120,
    'runs': [
        CONFIGS['Geth']['runs'][1],
        CONFIGS['Nethermind']['runs'][0],
        CONFIGS['Besu']['runs'][3]
    ]
}

if len(sys.argv) != 2 or str(sys.argv[1]) not in [*CONFIGS.keys(), 'ALL']:
    print("Please run like './generate-thesis-config.py <Geth|Nethermind|Besu|Erigon|ALL>'")
    sys.exit()

client = str(sys.argv[1])
config = CONFIG_ALL if client == "ALL" else CONFIGS[client]
sys_memory = psutil.virtual_memory().total
df_list = list(map(lambda run: load_df(run, sys_memory), config['runs']))

# Plots
sns.set()
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
