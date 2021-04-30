import pyts.transformation as transformation
import numpy as np

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

