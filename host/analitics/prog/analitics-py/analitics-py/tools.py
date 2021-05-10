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


def plot_series(series, cuts_position, cuts_length, cuts_count):
    plot_config = cuts_count * 100 + 11
    plt.figure(figsize=(8, cuts_count * 3))

    for i in range(cuts_count):
        plt.subplot(plot_config)
        plot_config += 1
        plt.plot(
            range(cuts_position, cuts_position + cuts_length),
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
        arr.append((string_values[0], string_values[2], string_values[3][:-1]))

    # print(arr)

    data_set = np.array(arr, dtype=data_set_type)  # .T

    if write:
        np.savetxt(path + name + '.csv', data_set,
               newline=conf.csv_newline, delimiter=conf.csv_delimiter,
               fmt=conf.csv_fmt)

    print(data_set)
    print(np.shape(data_set))

    print("done")