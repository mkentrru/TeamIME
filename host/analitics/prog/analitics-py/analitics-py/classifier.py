import pyts.transformation as transformation
import numpy as np
import scipy.spatial as sp

import analitics as a
import tools as t


class ClassifierPreprocessing:

    def __init__(self, n_bins, word_size):
        self.transformation = transformation.BOSS(
            drop_sum=True, n_bins=n_bins, word_size=word_size
        )

    def apply_transformation(self, series, cuts_position, cuts_length, cuts_count):
        X = series[cuts_position: cuts_position + cuts_length * cuts_count].reshape(
            cuts_count, cuts_length
        )
        return self.transformation.fit_transform(X)

    def get_vocabulary(self):
        return self.transformation.vocabulary_


class ClassifierLearning:
    def __init__(self, set_type):
        self.dtype = set_type

    def pick_learning_dataset(self, ods, index,
                              cuts_position, cuts_length,
                              cuts_step, cuts_count,
                              preprocessing):
        ds = ods[index]
        max_cuts_count = int(len(ds) / (cuts_length - cuts_step))
        cuts_count = min(cuts_count, int(len(ds) / (cuts_length - cuts_step)))
        print(cuts_count)


class SeriesClass:
    average = []

    def __init__(self, length, ds, label):
        self.length = length
        self.items = ds
        self.average = self.items
        self.label = chr(label)

    def distance(self, ds):
        return sp.distance.euclidean(self.average, ds)

    def add(self, ds):
        self.items = np.vstack([self.items, ds])
        self.average = np.mean(self.items, axis=0)
        # print(self.average)


def find_class(row, classes, dist):
    local_class_index = 0
    min_distance = None
    min_class_index = -1
    found = False

    for local_class in classes:
        local_distance = local_class.distance(row)
        if local_distance < dist: # self.power_classes_distance_barrier:
            found = True

            if min_distance is None or local_distance < min_distance:
                min_distance = local_distance
                min_class_index = local_class_index

        local_class_index += 1
    # print(min_distance)
    return found, min_class_index


class ClassificationTools:
    last_label = ord('a')

    area_window_size = 100

    power_window_size = 20
    power_classes_distance_barrier = 70
    power_classes = []
    power_labels = []

    temp_window_size = area_window_size
    temp_classes_distance_barrier = 0.1
    temp_labels = []
    temp_bins = [-50, -1, -0.5, 0, 0.5, 1, 50]

    def __init__(self, pds, sds):
        self.pds = pds.copy()
        self.sds = sds.copy()
        self.power_series = a.calculate_windows_average(self.pds, self.power_window_size)
        self.temp_series = a.calculate_windows_sum(self.sds, self.temp_window_size)

        self.power_values_range = int(max(self.pds) + 10)
        self.temp_values_range = int(max(self.temp_series) + 1) * 10

    def define_power_classes(self, start_pos, end_pos, step):
        areas_checked = 0

        t.plot_series(self.power_series, start_pos, end_pos, 1)

        for pos in range(start_pos, start_pos + end_pos - self.area_window_size - step, step):
            row = a.count_distribution(self.power_series[pos: pos + self.area_window_size],
                                       self.power_values_range)

            row_fits, row_class_index = find_class(row, self.power_classes,
                                                        self.power_classes_distance_barrier)
            # print('class index', row_class_index)
            if row_fits:
                self.power_classes[row_class_index].add(row)
            else:
                self.power_classes.append(SeriesClass(step, row, self.last_label))
                self.last_label += 1
            areas_checked += 1
            if pos % 100 == 0:
                print(end_pos, ' (', len(self.power_classes), ') ', '< ', pos)
        print('Checked: ', areas_checked)
        print('Classes count: ', len(self.power_classes))
        print('Sizes:')
        for lc in self.power_classes:
            print(len(lc.items))

        average_to_display = []
        idx = 0
        for lc in self.power_classes:
            average_to_display = np.append(average_to_display, lc.average)
            # print('===', idx, '(', lc.label, ')')
            # for cb in self.power_classes:
            #     print(sp.distance.euclidean(lc.average, cb.average))
            idx += 1
        t.plot_series(average_to_display, 0, self.power_values_range,
                      len(self.power_classes))

    def define_temp_classes(self, start_pos, end_pos, step):
        x = self.temp_series[start_pos: end_pos: step]
        bins_series = a.SeriesBinsPatterns(x, self.temp_bins)

        bins_series.apply_bins(self.area_window_size)
        self.temp_labels = bins_series.bins_row.copy()
        # print(bins_series.bins_row)
        # print(bins_series.appearance_counts)

    def apply_classes(self, start_pos, end_pos):

        for pos in range(start_pos, end_pos, self.area_window_size):
            power_row = a.count_distribution(self.power_series[pos: pos + self.area_window_size],
                                       self.power_values_range)
            # print(pos)
            # t.plot_series(power_row, 0, self.power_values_range, 1)
            # t.show_all_plots()

            _, row_class_index = find_class(power_row, self.power_classes,
                                                   self.power_classes_distance_barrier)
            self.power_labels.append(self.power_classes[row_class_index].label)

        new_row = [x+y for x, y in zip(self.power_labels, self.temp_labels)]

        return new_row


class ClassesAnalytics:

    classes = {}

    def __init__(self, row):
        new_id = 0
        for lc in row:
            if lc not in self.classes.keys():
                self.classes[lc] = new_id
                new_id += 1
        self.count = len(self.classes)
        self.row = row.copy()

    def count_followings(self):
        m = np.zeros((self.count, self.count))

        for pos in range(len(self.row) - 1):
            id_from, id_to = self.classes[self.row[pos]], self.classes[self.row[pos + 1]]
            m[id_from][id_to] += 1

        for line in m:
            print(line)
            line_sum = np.sum(line)
            line /= line_sum
            print(line)
        print(m)
        print(self.classes)