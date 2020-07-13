"""Here's where we'll put all the data for what obstacles will
be in each level, and when they'll appear.
"""

# Note: I don't think the 9's are ever used.
LEVEL_DATA = ['dummy', \
    {'start_fire': 3, '9': '', '8': 'ship_s', '7': '', \
        '6': 'ship_n', '5': 'event', '4': '', '3': 'ship_s', \
        '2': 'ship_n', '1': '', '0': ''}, \
    {'start_fire': 5, '9': '', '8': 'ast_nw', '7': 'ship_n', \
        '6': 'ast_se', '5': 'event', '4': '', '3': 'ship_s ast_ne', \
        '2': 'ast_sw ast_nw', '1': '', '0': ''}, \
    {'start_fire': 8, '9': '', '8': 'ship_n ast_se', '7': 'repair_sn', \
        '6': 'ship_s ship_n', '5': 'event', '4': 'ast_ne repair_rd', '3': '', \
        '2': 'ship_s repair_sh', '1': 'ast_nw ast_ne ast_sw ast_se', '0': ''} \
]
