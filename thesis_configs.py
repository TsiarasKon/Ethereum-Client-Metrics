# Hard-coded events (based on clients' log outputs in ROOT_DIR)
EVENT_CONFIGS = {
    'Geth': {
        'StateHeal': {
            'name': 'Began state heal',
            'marker': 'x',
            'color': 'blue',
            'size': 50
        },
        'SyncComplete': {
            'name': 'Sync competed',
            'marker': '*',
            'color': 'darkgreen',
            'size': 100
        }
    },
    'Nethermind': {
    },
    'Besu': {
    },
    'Erigon': {
    },
}
CONFIGS = {
    'Geth': {
        'time_ticks_step': 90,
        'runs': [{
            'name': 'Geth_1',
            'filename': 'metrics_24_01_geth_128_def.csv',
            'trim_rows': None,
            'events': [{
                'config': EVENT_CONFIGS['Geth']['StateHeal'],
                'time': '22:16:47',
                'x': 71625,
            }, {
                'config': EVENT_CONFIGS['Geth']['SyncComplete'],
                'time': '22:36:53',
                'x': 83625,
            }]
        }, {
            'name': 'Geth_2',
            'filename': 'metrics_20_01_geth.csv',
            'trim_rows': 22000,
            'events': [{
                'config': EVENT_CONFIGS['Geth']['StateHeal'],
                'time': '20:16:47',
                'x': 60469,
            }, {
                'config': EVENT_CONFIGS['Geth']['SyncComplete'],
                'time': '20:36:53',
                'delta_time': '22:41',
                'x': 71625,
            }]
        }]
    },
    'Nethermind': {
        'time_ticks_step': 120,
        'runs': [{
            'name': 'Nethermind_1',
            'filename': 'metrics_23_01_nethermind_snap_128_4096.csv',
            'trim_rows': 10800,
            'events': []
        }, {
            'name': 'Nethermind_2',
            'filename': 'metrics_28_01_nethermind_fast_128_4096.csv',
            'trim_rows': 7200,
            'events': []
        }]
    },
    'Besu': {
        'time_ticks_step': 60,
        'runs': [{
            'name': 'Besu_1',
            'filename': 'metrics_18_01_besu.csv',
            'trim_rows': 8000,
            'events': []
        }, {
            'name': 'Besu_2',
            'filename': 'metrics_21_01_besu_checkpoint.csv',
            'trim_rows': 20000,
            'events': []
        }, {
            'name': 'Besu_3',
            'filename': 'metrics_29_01_besu_snap_noBonsai.csv',
            'trim_rows': 2500,
            'events': []
        }, {
            'name': 'Besu_4',
            'filename': 'metrics_25_01_besu_noBonsai.csv',
            'trim_rows': 65000,
            'events': []
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
