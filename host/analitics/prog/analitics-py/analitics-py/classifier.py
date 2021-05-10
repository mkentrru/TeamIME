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
    items = []
    average = []

    def __init__(self, length):
        self.length = length

    def distance(self, ds):
        return sp.distance.euclidean(self.average, ds)

    def add(self, ds):
        self.items = np.append(self.items, ds)
        self.average = np.mean(self.items, axis=0)


class AverageBasedClassification:
    local_window_size = 20
    area_window_size = 500
    values_range = 100

    primary_classes_distance_barrier = 50
    primary_classes = []

    def __init__(self, ds):
        self.ods = ds.copy()
        self.local_average = a.calculate_windows_average(self.ods, self.local_window_size)
        # t.plot_series(self.local_average, 0, len(self.local_average) - self.local_window_size, 1)
        # t.show_all_plots()
        self.values_range = int(max(self.local_average) * 1.2)

    def find_class(self, row, classes):
        local_class_index = 0
        for local_class in classes:
            if local_class.distance(row) < self.primary_classes_distance_barrier:
                return True, local_class_index
        return False, -1

    def define_primary_classes(self, start_pos, end_pos, step):
        for pos in range(start_pos, start_pos + end_pos - step, step):
            row = a.count_distribution(self.ods[pos: pos + self.area_window_size], self.values_range)

            row_fits, row_class_index = self.find_class(row, self.primary_classes)
            if row_fits:
                self.primary_classes[row_class_index].add(row)
            else:
                self.primary_classes.append(SeriesClass(step))
                self.primary_classes[-1].add(row)
