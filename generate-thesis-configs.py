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


# def plot_lines(cols, title, ylabel):
#     fig, ax = plt.subplots(constrained_layout=True)
#     ax.xaxis.set_major_formatter(TIME_FORMATTER)
#     if len(cols) > 1:
#         for col in cols:
#             ax.plot(df.index, df[col])
#     else:
#         ax.plot(df.index, df[cols[0]], label='_nolegend_')
#     ax.set_xticks([sec for sec in df.index[::TIME_TICKS_STEP]])
#     for event, val_dict in EVENTS[client].items():
#         plt.axvline(label=event, **val_dict)

#     plt.title(title)
#     plt.ylabel(ylabel)
#     plt.xlabel(TIME_LABEL)
#     # plt.xticks(rotation=45)
#     plt.legend([*cols, *EVENTS[client].keys()] if len(cols)
#                > 1 else [*EVENTS[client].keys()])
#     plt.grid('on', linestyle='--')
#     plt.savefig(cols[0])
#     plt.show()


def plot_col_multidf(config, df_list, col, title, ylabel):
    longest_df = max(df_list, key=lambda x: len(x))
    fig, ax = plt.subplots(constrained_layout=True)
    ax.xaxis.set_major_formatter(hours_formatter)
    for df in df_list:
        ax.plot(df.index, df[col])
    ax.set_xticks([sec for sec in longest_df.index[::config['time_ticks_step']]])
    # for event, val_dict in client.items():
    #     plt.axvline(label=event, **val_dict)

    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Time (hours)")
    plt.legend(list(map(lambda run: run['name'], config['runs'])))
    plt.grid('on', linestyle='--')
    # plt.savefig('fig')
    plt.show()


def load_df(run_config, sys_memory):
    df = pd.read_csv(run_config['filename'], delim_whitespace=True, usecols=[
                     '%CPU', '%MEM', 'kB_rd/s', 'kB_wr/s', 'kbps_sent', 'kbps_rec', 'disk_used'])
    if run_config['row_cutoff'] is not None:
        df = df[:run_config['row_cutoff']]

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
    df['disk_used'] = df['disk_used'].map(
        lambda val: convert_bytes(val, "GB", "KB"))
    return df


ROW_CUTOFF = None  # if not None, use df[:ROW_CUTOFF] for everything
INTERVAL = 60   # in seconds
ROOT_DIR = './csv/'

# Hard-coded events (based on clients' log outputs in ROOT_DIR)
CONFIGS = {
    'Geth': {
        'runs': [{
            'name': 'Geth_1',
            'filename': ROOT_DIR + 'metrics_20_01_geth.csv',
            'row_cutoff': 90000,
            'events': {
                # 22:16:47
                'Began state heal (22:21)': dict({'x': 80469, 'color': 'green', 'linestyle': ':'}),
                # 22:36:53
                'Sync competed (22:41)': dict({'x': 81625, 'color': 'gray', 'linestyle': '-'})
            }
        }, {
            'name': 'Geth_2',
            'filename': ROOT_DIR + 'metrics_24_01_geth_128_def.csv',
            'row_cutoff': None,
            'events': {
                # 22:16:47
                'Began state heal (22:21)': dict({'x': 80469, 'color': 'green', 'linestyle': ':'}),
                # 22:36:53
                'Sync competed (22:41)': dict({'x': 81625, 'color': 'gray', 'linestyle': '-'})
            }
        }],
        'time_ticks_step': 180,
    },
    'Nethermind': {
        'time_ticks_step': 60,
    },
    'Besu': {
        'time_ticks_step': 180,
    },
    'Erigon': {
        'time_ticks_step': 60,
    },
}
CONFIG_ALL = {
    'runs': [CONFIGS['Geth']['runs'][0]],
    'TIME_TICKS_STEP': 60,
}

if len(sys.argv) != 2 or str(sys.argv[1]) not in [*CONFIGS.keys(), '*']:
    print("Please run like './generate-thesis-config.py <Geth|Nethermind|Besu|Erigon|*>'")
    sys.exit()

client = str(sys.argv[1])
config = CONFIG_ALL if client == '*' else CONFIGS[client]
sys_memory = psutil.virtual_memory().total
sns.set()

df_list = list(map(lambda run: load_df(run, sys_memory), config['runs']))
# print(df_list)

# Plots
plot_col_multidf(config, df_list, '%CPU', "CPU usage over time", "%")
# plot_lines(["MEM"], "RAM usage over time", "GB")
# plot_lines(["disk_used"], "Chain data disk size over time", "GB")
# plot_lines(["Reads", "Writes"], "Disk I/O over time", "MB per second")
# plot_lines(["Sent", "Received"], "Network traffic over time", "MB per second")
