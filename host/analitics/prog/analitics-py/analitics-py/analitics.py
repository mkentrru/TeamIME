import numpy as np
import tools as t
import configuration as conf

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


class SeriesPatterns:
    appearance_counts = []
    bins_row = []

    def __init__(self, ds):
        self.bins = SeriesBins()
        self.ds = ds
        self.values = np.zeros(max(ds) + 1, dtype=np.int32)

    def gather_information(self):
        for value in self.ds:
            self.values[value] += 1

        value_index = 0
        for count in self.values:
            if count != 0:
                self.appearance_counts.append((value_index, count))
                print(' ', value_index, '\t', count)
            value_index += 1
        # print(self.appearance_counts)

    def create_bins(self, count, endings):
        for i in range(count):
            self.bins.append(label=None, e=endings[i])

    def get_bin_label(self, value):
        for bin_node in self.bins.l:
            if bin_node[2] is None or value <= bin_node[2]:
                return bin_node[0]

    def apply_bins(self):
        arr = []
        for value in self.ds:
            arr.append(self.get_bin_label(value))
        self.bins_row = arr




pure_data = t.Data(conf.path, conf.data_set_type)
pure_data.add_dataset_from_file('r3/', 'v', 'csv')


sp = SeriesPatterns(pure_data.ods['Voltage'])
sp.gather_information()
sp.create_bins(3, [12, 24, None])
sp.apply_bins()
