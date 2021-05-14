import numpy as np
import tools as t
import configuration as conf
import statistics


class SeriesBins:
    current_label = ord('a')

    def __init__(self):
        self.l = list()

    def new_label(self):
        a = chr(self.current_label)
        self.current_label += 1
        return a

    def append(self, label=None, b=None, e=None):
        if label is None:
            label = self.new_label()
        self.l.append((label, b, e))
        # print((label, b, e))


class SeriesBinsPatterns:
    bins_row = []
    appearance_counts = []

    def __init__(self, ds, endings):
        self.bins = SeriesBins()
        self.ds = ds
        for i in range(len(endings)):
            self.bins.append(label=None, e=endings[i])
        self.appearance_counts = np.zeros(len(endings))

    # def gather_information(self):
    #     for value in self.ds:
    #         self.values[value] += 1
    #
    #     value_index = 0
    #     for count in self.values:
    #         if count != 0:
    #             self.appearance_counts.append((value_index, count))
    #             print(' ', value_index, '\t', count)
    #         value_index += 1
    #     print(self.appearance_counts)

    def get_bin_label(self, value):
        for bin_node in self.bins.l:
            if bin_node[2] is None or value <= bin_node[2]:
                return bin_node[0]

    def apply_bins(self, step):
        arr = []
        for value in range(0, len(self.ds), step): # self.ds:
            bin_label = self.get_bin_label(self.ds[value])
            arr.append(bin_label)
            bin_index = ord(bin_label) - ord('a')
            self.appearance_counts[bin_index] += 1

        self.bins_row = arr


def calculate_patterns(ds, length, step):
    d = {}
    for pattern_index in range(0, len(ds) - length, step):
        key = ''
        for c in range(0, length):
            key += ds[pattern_index + c]

        current_value = d.get(key, None)
        if current_value is None:
            new_value = 1
        else:
            new_value = current_value + 1
        d.update({key: new_value})
    print('Patterns appearance:')
    for key, value in d.items():
        print(key, value)


def get_pattern_distances(ds, pattern):
    pattern_length = len(pattern)
    current_length = 0
    approximated = []
    X = []
    for pos in range(len(ds) - pattern_length):
        s = ''.join(ds[pos: pos + pattern_length])
        current_length += 1
        if s == pattern:
            X.append(current_length)
            current_length = 0
            approximated.append(1)
        else:
            approximated.append(0)
    print('Pattern: \'', pattern, '\'')
    print('Values: ', X)
    return X, approximated


def gather_in_range_info(ds, bottom, up):
    print('\n', '[', bottom, ';', up, ']')
    X = []
    X_distances = []
    X_distance = 0
    for value in ds:
        X_distance += value
        if bottom <= value <= up:
            X.append(value)
            X_distances.append(X_distance)
            X_distance = 0
    length = len(X)
    data_mean = statistics.mean(X)
    # data_variance = statistics.variance(X, xbar=None)
    print('Size: ', length)
    print('Values:\n', X)
    print('Values offsets:\n', X_distances)
    # t.print_list_in_columns([X, X_distances])

    print('Mean: ', data_mean)
    # print('Variance: ', data_variance)

# def get_periods_info(ds, length_start, length_end, length_diff, epsilon, pattern):


def count_distribution(ds, index_range, step=1, scale=1):
    lower, upper = np.min(ds), np.max(ds)
    # if lower < 0:
    #     index_range = int((int(upper-lower) + 1) / step)
    # else:
    # index_range = int((upper + 1) / step)

    x = np.zeros(index_range)
    for value in ds:
        value_index = int(value * scale / step)
        x[value_index] += 1
    return x


def calculate_windows_average(ds, length):
    x = []
    for pos in range(len(ds) - length):
        av = np.average(ds[pos:pos + length])
        x.append(av)
    return x


def count_words(ds):
    counter = {}
    for w in ds:
        if w in counter.keys():
            counter[w] += 1
        else:
            counter[w] = 1
    return sorted(counter.items(), key=lambda x: x[1])


def calculate_windows_sum(ds, length):
    x = []
    for pos in range(len(ds) - length):
        sv = np.sum(ds[pos:pos + length])
        x.append(sv)
    return x


def get_information(ds):
    values_range = ds.max - ds.min
    print(values_range)

# old
# # pure_data = t.Data(conf.path, conf.data_set_type)
# # pure_data.add_dataset_from_file('r1/', 'timeout', 'csv')
# # pure_data.prepare_dataset()
# #
# # t.plot_series(pure_data.ods['Power'], 70, 450, 2)


# normal = t.Data(conf.path, conf.data_set_type)
# normal.add_dataset_from_file('r1/', 'normal', 'csv')
#
# timeout = t.Data(conf.path, conf.data_set_type)
# timeout.add_dataset_from_file('r1/', 'timeout', 'csv')
#
# attack = t.Data(conf.path, conf.data_set_type)
# attack.add_dataset_from_file('r1/', 'attack', 'csv')
#
# windows_size = 20
#
#
# windows_average = calculate_windows_average(timeout.ods['Power'], windows_size)
# average_distribution = count_distribution(windows_average, 100)
#
# t.plot_series(windows_average, 0, 1000, 1)
# t.plot_series(average_distribution, 0, len(average_distribution), 1)
#
# # t.plot_series(timeout.ods['Power'], 0, 1000, 1)
#
# windows_average = calculate_windows_average(attack.ods['Power'], windows_size)
# average_distribution = count_distribution(windows_average, 100)
#
# t.plot_series(windows_average, 0, 1000, 1)
# t.plot_series(average_distribution, 0, len(average_distribution), 1)

# t.plot_series(attack.ods['Power'], 0, 1000, 1)

# # get_information(pure_data.pds)
#
#
# # sp = SeriesPatterns(pure_data.ods['Voltage'])
# # sp.gather_information()
# # sp.create_bins(3, [30, 31, None])
# # sp.apply_bins()
# #
# # ds_pos = 0
# # ds_length = 10000
# #
# # calculate_patterns(sp.bins_row[ds_pos: ds_pos + ds_length], 3, 1)
# #
# # distances, pattern_appearance = \
# #     get_pattern_distances(sp.bins_row[ds_pos: ds_pos + ds_length], 'aba')
# # gather_in_range_info(distances, 0, 15)
# # gather_in_range_info(distances, 19, 24)
# # gather_in_range_info(distances, 25, 55)
# # gather_in_range_info(distances, 56, 120)
# #
# # t.plot_series(distances, 0, len(distances), 1)
#
t.show_all_plots()

