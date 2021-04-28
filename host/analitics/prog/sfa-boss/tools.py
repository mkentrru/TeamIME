import numpy as np
import matplotlib.pyplot as plt
from pyts.approximation import DiscreteFourierTransform

def die(msg):
    print(msg)
    exit(1)


class Configuration:
    def __init__(self, time_series_size, time_series_length):
        self.time_series_length = time_series_length
        self.time_series_size = time_series_size

class SFA:
    transformed = []
    pd = []

    def __init__(self, ds, pos, length, coefs_count):
        self.ods = ds
        self.cut_pos = pos
        self.cut_length = length
        self.coefs_count = coefs_count
        # self.ods_cut = ds[pos:len:1].copy()

    def calculate_fourier_coefficients(self):
        X = (self.ods[self.cut_pos: self.cut_pos + self.cut_length: 1],
             range(0, self.cut_length))
        dft = DiscreteFourierTransform(
            n_coefs=self.coefs_count, norm_mean=False,
                                       norm_std=False)
        self.transformed = dft.fit_transform(X)[0]
        print(self.transformed)
        self.pd = self.transformed


class Data:
    ds = []
    pd = []  # prepared data (for work and display

    def __init__(self, ds_path, ds_name, ds=None):
        self.ds_path = ds_path
        self.ds_name = ds_name
        self.ds_full_path = ds_path + ds_name
        try:
            self.ds_file = open(self.ds_full_path, "r")
        except FileNotFoundError:
            die('Cannot open dataset file: ' + self.ds_full_path)
        self.ds_file.close()

        if ds is not None:
            self.ds = ds

    def save_dataset(self):
        np.save(self.ds_full_path, self.ds)

    def load_dataset(self):
        self.ds = np.load(self.ds_full_path)

    def simulate_dataset(self, size, length, offsets):
        a = []
        for i in range(size):
            a.append(offsets[i] + np.random.normal(0, 0.1, length))
        self.ds = np.array(a)

    def prepare_dataset(self, type=None):
        if type is None:
            self.pd = self.ds
        if type is 'n':
            self.pd = self.ds / np.linalg.norm(self.ds)
            # self.pds = pp.normalize(self.ds)


def display_data(data_rows, b=None, e=None):
    xmin = 0
    xmax = min([np.shape(s.pd) for s in data_rows])[0]

    if b is not None and b < xmax:
        xmin = b
    if e is not None and e < xmax:
        xmax = e

    ymin = min([min(s.pd[xmin: xmax]) for s in data_rows])
    if ymin < 0:
        ymin *= 1.1
    else:
        ymin /= 1.1

    ymax = max([max(s.pd[xmin: xmax]) for s in data_rows])
    if ymax > 0:
        ymax *= 1.1
    else:
        ymax /= 1.1

    fig, ax = plt.subplots(figsize=(10, 7))
    xaxes = np.arange(xmin, xmax, 1)

    for s in data_rows:
        ax.plot(xaxes, s.pd[xmin:xmax], linewidth=1.0)

    ax.set_xlim(xmin=xmin, xmax=xmax)
    ax.set_ylim(ymin = ymin, ymax = ymax)
    fig.tight_layout()
    plt.show()


def display_data_in_rows(data_rows, length, b, f):
    plot_config = 211
    plt.figure(figsize=(9, 9))
    i = 0
    for set in data_rows:
        plt.subplot(plot_config)
        plot_config += 1
        plt.plot(
            range(b[i], b[i] + length[i]),
            set.pd[b[i]: b[i] + length[i]: 1], f[i], linewidth=1.0)
        i += 1
    plt.show()