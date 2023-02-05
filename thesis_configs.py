# Hard-coded events (based on clients' log outputs in ROOT_DIR)
EVENT_CONFIGS = {
    'Geth': {
        'HeaderSync': {
            'name': 'Headers chain synced',
            'marker': '^',
            'color': 'darkgreen',
            'size': 50
        },
        'BlocksDownloaded': {
            'name': 'Blocks downloaded',
            'marker': 'v',
            'color': 'lightgreen',
            'size': 50
        },
        'StateSync': {
            'name': 'State sync completed',
            'marker': 'x',
            'color': 'blue',
            'size': 50
        },
        'StateHeal': {
            'name': 'State heal competed',
            'marker': '*',
            'color': 'red',
            'size': 100
        }
    },
    'Nethermind': {
        'HeaderSync': {
            'name': 'Headers chain synced',
            'marker': '^',
            'color': 'darkgreen',
            'size': 50
        },
        'StateSync': {
            'name': 'State sync completed',
            'marker': 'x',
            'color': 'blue',
            'size': 50
        },
        'BlocksDownloaded': {
            'name': 'Blocks bodies downloaded',
            'marker': 'v',
            'color': 'lightgreen',
            'size': 50
        },
        'ReceiptsDownloaded': {
            'name': 'Receipts bodies downloaded',
            'marker': '*',
            'color': 'red',
            'size': 100
        }
    },
    'Besu': {
        'StateSync': {
            'name': 'World state downloaded',
            'marker': 'x',
            'color': 'blue',
            'size': 50
        },
        'BlocksDownloaded': {
            'name': 'Blocks downloaded',
            'marker': 'v',
            'color': 'lightgreen',
            'size': 50
        },
        'StateHeal': {
            'name': 'State heal competed',
            'marker': '*',
            'color': 'red',
            'size': 100
        }
    },
    'Erigon': {
        '1': {
            'name': 'Snapshots',
            'marker': '$1$',
            'color': 'black',
            'size': 50
        },
        '7': {
            'name': 'Execution',
            'marker': '$7$',
            'color': 'black',
            'size': 50
        },
        '8': {
            'name': 'HashState',
            'marker': '$8$',
            'color': 'black',
            'size': 50
        },
        '9': {
            'name': 'IntermediateHashes',
            'marker': '$9$',
            'color': 'black',
            'size': 50
        },
        '13': {
            'name': 'LogIndex',
            'marker': '$13$',
            'color': 'black',
            'size': 100
        }
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
                'config': EVENT_CONFIGS['Geth']['HeaderSync'],
                'time': '11:29:26',
                'x': 1007,
            }, {
                'config': EVENT_CONFIGS['Geth']['BlocksDownloaded'],
                'time': '00:01:10',
                'x': 46111,
            }, {
                'config': EVENT_CONFIGS['Geth']['StateSync'],
                'time': '08:57:54',
                'x': 77737,
            }, {
                'config': EVENT_CONFIGS['Geth']['StateHeal'],
                'time': '09:18:52',
                'x': 78110,
            }]
        }, {
            'name': 'Geth_2',
            'filename': 'metrics_20_01_geth_128_16384.csv',
            'trim_rows': 22000,
            'events': [{
                'config': EVENT_CONFIGS['Geth']['HeaderSync'],
                'time': '01:00:11',
                'x': 1030,
            }, {
                'config': EVENT_CONFIGS['Geth']['BlocksDownloaded'],
                'time': '13:26:07',
                'x': 45786,
            }, {
                'config': EVENT_CONFIGS['Geth']['StateSync'],
                'time': '20:08:24',
                'x': 69869,
            }, {
                'config': EVENT_CONFIGS['Geth']['StateHeal'],
                'time': '20:26:35',
                'x': 69976,
            }]
        }]
    },
    'Nethermind': {
        'time_ticks_step': 120,
        'runs': [{
            'name': 'Nethermind_1',
            'filename': 'metrics_23_01_nethermind_snap_128_4096.csv',
            'trim_rows': 10800,
            'events': [{
                'config': EVENT_CONFIGS['Nethermind']['HeaderSync'],
                'time': '14:49:36',
                'x': 1605,
            }, {
                'config': EVENT_CONFIGS['Nethermind']['StateSync'],
                'time': '16:59:08',
                'x': 9286,
            }, {
                'config': EVENT_CONFIGS['Nethermind']['BlocksDownloaded'],
                'time': '22:49:23',
                'x': 30301,
            }, {
                'config': EVENT_CONFIGS['Nethermind']['ReceiptsDownloaded'],
                'time': '02:20:01',
                'x': 42939,
            }]
        }, {
            'name': 'Nethermind_2',
            'filename': 'metrics_28_01_nethermind_fast_128_4096.csv',
            'trim_rows': 7200,
            'events': [{
                'config': EVENT_CONFIGS['Nethermind']['HeaderSync'],
                'time': '01-28 01:38:05',
                'x': 3982,
            }, {
                'config': EVENT_CONFIGS['Nethermind']['StateSync'],
                'time': '01-28 20:29:53',
                'x': 71890,
            }, {
                'config': EVENT_CONFIGS['Nethermind']['BlocksDownloaded'],
                'time': '01-29 02:39:09',
                'x': 94046,
            }, {
                'config': EVENT_CONFIGS['Nethermind']['ReceiptsDownloaded'],
                'time': '01-29 08:38:20',
                'x': 115594,
            }]
        }]
    },
    'Besu': {
        'time_ticks_step': 60,
        'runs': [{
            'name': 'Besu_1',
            'filename': 'metrics_18_01_besu.csv',
            'trim_rows': 8000,
            'events': [{
                'config': EVENT_CONFIGS['Besu']['StateSync'],
                'time': '01-18 07:59:27',
                'x': 27465,
            }, {
                'config': EVENT_CONFIGS['Besu']['BlocksDownloaded'],
                'time': '01-19 07:58:25',
                'x': 113798,
            }, {
                'config': EVENT_CONFIGS['Besu']['StateHeal'],
                'time': '01-19 08:01:13',
                'x': 113966,
            }]
        }, {
            'name': 'Besu_2',
            'filename': 'metrics_21_01_besu_checkpoint.csv',
            'trim_rows': 20000,
            'events': [{
                'config': EVENT_CONFIGS['Besu']['StateSync'],
                'time': '01-21 18:59:04',
                'x': 30186,
            }, {
                'config': EVENT_CONFIGS['Besu']['BlocksDownloaded'],
                'time': '01-22 10:57:06',
                'x': 87668,
            }, {
                'config': EVENT_CONFIGS['Besu']['StateHeal'],
                'time': '01-21 20:06:45',
                'x': 34247,
            }]
        # }, {
        #     'name': 'Besu_3',
        #     'filename': 'metrics_29_01_besu_snap_noBonsai.csv',
        #     'trim_rows': 2500,
        #     'events': []
        # }, {
        #     'name': 'Besu_4',
        #     'filename': 'metrics_25_01_besu_noBonsai.csv',
        #     'trim_rows': 65000,
        #     'events': []
        }]
    },
    'Erigon': {
        'time_ticks_step': 360,
        'runs': [{
            'name': 'Erigon',
            'filename': 'metrics_30_01_erigon.csv',
            'trim_rows': 10800,
            'events': [{
                'config': EVENT_CONFIGS['Erigon']['1'],
                'time': '01-31 11:06:43',
                'x': 43197,
            }, {
                'config': EVENT_CONFIGS['Erigon']['7'],
                'time': '02-04 05:17:08',
                'x': 367581,
            }, {
                'config': EVENT_CONFIGS['Erigon']['8'],
                'time': '02-04 06:49:55',
                'x': 373147,
            }, {
                'config': EVENT_CONFIGS['Erigon']['9'],
                'time': '02-04 07:36:32',
                'x': 375944,
            }, {
                'config': EVENT_CONFIGS['Erigon']['13'],
                'time': '02-04 11:19:02',
                'x': 389292,
            }]
        }]
    },
}
CONFIG_ALL = {
    'time_ticks_step': 120,
    'runs': [
        CONFIGS['Geth']['runs'][1],
        CONFIGS['Nethermind']['runs'][0],
        CONFIGS['Besu']['runs'][1]
    ]
}
