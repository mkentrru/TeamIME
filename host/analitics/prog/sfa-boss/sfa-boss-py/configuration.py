import numpy as np

data_set_type = [('Time', (np.str, 12)), ('Voltage', np.int32)]
classifier_set_type = [('Pos', np.int32), ('Dist', np.float64)]

csv_newline = '\n'
csv_delimiter = ' '
csv_fmt = ['%s', '%d']

path = '../../data/sets/'
