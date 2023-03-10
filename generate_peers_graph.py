import sys
import psutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from thesis_configs import CONFIGS, CONFIG_ALL

INTERVAL = 120   # in seconds
LOGS_DIR = './logs/'


@mticker.FuncFormatter
def hours_formatter(seconds, pos=None):
    # As opposed to strftime format, it supports h > 23
    m, _ = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return str(h)


def plot_col_multidf(config, df_list, col, title, ylabel, client):
    longest_df = max(df_list, key=lambda x: len(x))
    fig, ax = plt.subplots(constrained_layout=True)
    fig.set_size_inches(7.5, 5.25)
    fig.set_dpi(100)
    ax.xaxis.set_major_formatter(hours_formatter)
    ax.set_xticks(
        [sec for sec in longest_df.index[::config['time_ticks_step']]])
    for run, df in zip(config['runs'], df_list):
        ax.plot(df.index, df[col], label=run['name'], zorder=5)
        for event in run['events']:
            x_index = event['x'] // INTERVAL
            if client == "ALL":
                if event == run['events'][-1]:
                    marker_label = "Initial sync completed" if run == config['runs'][-1] else "_nolegend_"
                    ax.scatter(df.index[x_index], df.iloc[x_index][col], marker='*',
                            color='crimson', s=100, label=marker_label, zorder=10)
            else:
                marker_label = event['config']['name'] if run == config['runs'][-1] else "_nolegend_"
                ax.scatter(df.index[x_index], df.iloc[x_index][col], marker=event['config']['marker'],
                        color=event['config']['color'], s=event['config']['size'], label=marker_label, zorder=10)

    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Time (hours)")
    plt.grid('on', linestyle='--')
    plt.legend()
    # plt.legend(loc=4)
    # plt.savefig(f"{client}_{col}.png")
    # plt.savefig(f"{col}.png")
    plt.show()


def load_df(run_config):
    df = pd.read_csv(LOGS_DIR + run_config['logs'], usecols=['Peers'])
    if run_config['trim_rows'] is not None:
        df = df[:-run_config['trim_rows']]

    # Index df with timedeltas and average rows by INTERVAL
    df['seconds_delta'] = pd.to_timedelta(df.index, unit="S").total_seconds()
    df = df.groupby(df.index // INTERVAL).mean(numeric_only=False)
    df.set_index('seconds_delta', inplace=True)
    return df


if len(sys.argv) != 2 or str(sys.argv[1]) not in [*CONFIGS.keys(), 'ALL']:
    print("Please run like './generate_peers_graph.py <Geth|Nethermind|Besu|Erigon|ALL>'")
    sys.exit()

client = str(sys.argv[1])
config = CONFIG_ALL if client == "ALL" else CONFIGS[client]
df_list = list(map(lambda run_config: load_df(run_config), config['runs']))

# Plots
# sns.set()
plot_col_multidf(config, df_list, 'Peers', "Client peers over time", "Peers", client)
