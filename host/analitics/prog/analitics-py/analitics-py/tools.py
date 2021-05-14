import numpy as np
import matplotlib.pyplot as plt
import os
import configuration as conf


def die(msg):
    print(msg)
    exit(1)


class Data:
    ods = None  # original data set
    pds = None  # prepared data set

    def __init__(self, path, dtype):
        if not os.path.exists(path):
            die('Data: root path does not exists: ' + path)
        self.path = path
        self.dtype = dtype

    def add_dataset_from_file(self, subdir, name, filetype):
        if filetype == 'csv':
            name += '.csv'
        elif filetype == 'npy':
            name += '.npy'

        full_path = self.path + subdir + name
        if not os.path.exists(full_path):
            die('Data: dataset does not exists: ' + full_path)

        if filetype == 'csv':
            arr = np.loadtxt(full_path, delimiter=conf.csv_delimiter, dtype=self.dtype)
            if self.ods is None:
                self.ods = arr
            else:
                self.ods = np.append (self.ods, arr, axis=0)
        print(self.ods)

    def prepare_dataset(self):
        self.pds = np.array((self.ods['Temp'], self.ods['Power']))


def prepare_dataset(ds, cut_pos, cut_length, mode):
    if mode == 'diff':
        x = np.zeros(cut_length)
        for pos in range(1, cut_length):
            x[pos] -= ds[cut_pos + pos - 1] - ds[cut_pos + pos]
        return x
    if mode == 'cut':
        x = ds[cut_pos: cut_pos + cut_length].copy()
        return x


def plot_series(series, cuts_position, cuts_length, cuts_count=1, vline_space=None, move=True):
    plot_config = cuts_count * 100 + 11
    plt.figure(figsize=(8, cuts_count * 3))

    for i in range(cuts_count):
        plt.subplot(plot_config)
        plot_config += 1
        if vline_space is not None:
            for x in range(cuts_position, cuts_position + cuts_length, vline_space):
                plt.axvline(x=x, ls='--', lw=0.5, color=(0.1, 0.5, 0.1))

        if move:
            x = range(cuts_position, cuts_position + cuts_length)
        else:
            x = range(0, cuts_length)
        plt.plot(
            x,
            series[cuts_position: cuts_position + cuts_length: 1],
            linewidth=1.0)

        cuts_position += cuts_length




def bar_series(series):
    plt.figure(figsize=(8, 9))
    plt.subplot(111)

    sub_columns_fix = 1
    sub_columns_count = np.shape(series)[0]
    columns_count = np.shape(series)[1]
    columns_width = sub_columns_fix * (sub_columns_count + 2)

    x = np.arange(0, columns_width * columns_count, columns_width)

    sub_column_index = 0
    for r in series:
        plt.bar(x + sub_column_index * sub_columns_fix, r, linewidth=0.1)
        sub_column_index += 1


def show_all_plots():
    plt.show()


def print_list_in_columns(data):
    if not data:
        return
    print(np.array(data).T)


def parse_data(subdir, name, write=False):
    path = conf.path + subdir
    source_file = open(path + name + '.txt', "r")
    data_set_type = conf.data_set_type
    arr = []

    i = 0
    for line in source_file:
        string_values = line.split(" ")
        # time_value = time.strptime(string_values[0], '%H:%M:%S.%f')
        # timestamp = int(time.mktime(time_value))
        # print(timestamp)
        # print(string_values)
        arr.append((string_values[0], string_values[1][:-1]))

    # print(arr)

    data_set = np.array(arr, dtype=data_set_type)  # .T

    if write:
        np.savetxt(path + name + '.csv', data_set,
               newline=conf.csv_newline, delimiter=conf.csv_delimiter,
               fmt=conf.csv_fmt)

    print(data_set)
    print(np.shape(data_set))

    print("done")