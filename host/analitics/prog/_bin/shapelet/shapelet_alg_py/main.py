import numpy as np
import matplotlib.pyplot as plt
import sklearn.preprocessing as pp


def die(msg):
    print(msg)
    exit(1)


class Configuration:
    def __init__(self, time_series_size, time_series_length):
        self.time_series_length = time_series_length
        self.time_series_size = time_series_size


class Shapelet:
    distance = 0
    quality = 0
    shape = 0

    def __init__(self, size, length):
        self.length = length

    def update_pos(self, pos, ds):
        print(ds[0:1][0: 2].copy())



class ShapeletsAlg:
    sh = []

    def __init__(self, ds, lmin, lmax):
        self.ds = ds
        self.lmin = lmin
        self.lmax = lmax

    # def calculate_distance(self, s):
    #     for pos in range(len(self.ds[0])):
    #         d = self.ds[0][pos:pos + 50, 1] -

    def calculate_shaplets(self):
        l = self.lmin
        s = Shapelet(len(self.ds), l)
        for pos in range(0, len(self.ds[0]) - l, 1):
            s.update_pos(pos, self.ds)
            print(s.shape)



class Data:
    ds = []
    pds = []  # prepared dataset

    def __init__(self, ds_path, ds_name):
        self.ds_path = ds_path
        self.ds_name = ds_name
        self.ds_full_path = ds_path + ds_name
        try:
            self.ds_file = open(self.ds_full_path, "r")
        except FileNotFoundError:
            die('Cannot open dataset file: ' + self.ds_full_path)
        self.ds_file.close()

    def save_dataset(self):
        np.save(self.ds_full_path, self.ds)

    def load_dataset(self):
        self.ds = np.load(self.ds_full_path)

    def simulate_dataset(self, size, length, offsets):
        a = []
        for i in range(size):
            a.append(offsets[i] + np.random.normal(0, 0.1, length))
        self.ds = np.array(a)

    def prepare_dataset(self):
        self.pds = pp.normalize(self.ds)


if __name__ == '__main__':
    c = Configuration(2, 10)
    d = Data('data/sets/bin/', 'normal_spread.npy')

    d.simulate_dataset(c.time_series_size, c.time_series_length, [30, 0.5])
    d.save_dataset()
    # d.load_dataset()

    d.prepare_dataset()

    S = ShapeletsAlg(d.pds, 5, 7)

    S.calculate_shaplets()



    gr_x = np.arange(0, c.time_series_length, 1)
    fig, ax = plt.subplots(figsize=(10, 5))

    # ax.plot(gr_x, d.ds[0, :])
    # ax.plot(gr_x, d.ds[1, :])

    # ax.plot(gr_x, d.pds[0, :])
    ax.plot(gr_x, S.ds[1, :])

    # ax.plot(gr_x, d.ds[0, :])
    ax.plot(gr_x, d.pds[1, :])

    ax.set_xlim(xmin=gr_x[0], xmax=gr_x[-1])
    # ax.set_ylim(ymin = 0, ymax = 100)
    fig.tight_layout()

    plt.show()




