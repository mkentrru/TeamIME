import numpy as np
import matplotlib.pyplot as plt


def die(msg):
    print(msg)
    exit(1)


class Configuration:
    def __init__(self, time_series_size, time_series_length):
        self.time_series_length = time_series_length
        self.time_series_size = time_series_size


class Data:
    def __init__(self, ds_path, ds_name):
        self.ds_path = ds_path
        self.ds_name = ds_name
        self.ds_full_path = ds_path + ds_name
        try:
            self.ds_file = open(self.ds_full_path, "r")
        except FileNotFoundError:
            die('Cannot open dataset file: ' + self.ds_full_path)
        self.ds_file.close()

    def save_dataset(self, arr):
        np.save(self.ds_full_path, arr)

    def load_dataset(self):
        return np.load(self.ds_full_path)


def simulate_dataset(size, length, offsets):
    a = np.zeros((size, length))
    for i in range(size):
        a[i] = 10 + np.random.normal(0, 0.1, length)
    return a

if __name__ == '__main__':
    c = Configuration(2, 100)
    d = Data('data/sets/bin/', 'normal_spread.npy')

    # a = np.random.normal(0, 0.1, size=(c.time_series_size, c.time_series_length))
    #
    # d.save_dataset(a)

    # a = d.load_dataset()

    a = simulate_dataset(c.time_series_size, c.time_series_length, [32, 10])

    gr_x = np.arange(0, c.time_series_length, 1)

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(gr_x, a[0, :])
    ax.plot(gr_x, a[1, :])
    ax.set_xlim(xmin=gr_x[0], xmax=gr_x[-1])
    # ax.set_ylim(ymin = 0, ymax = 100)
    fig.tight_layout()

    plt.show()




