import tools as t
import classifier as c
import configuration as conf

import matplotlib.pyplot as plt

if __name__ == '__main__':
	pure_data = t.Data(conf.path, conf.data_set_type)
	pure_data.add_dataset_from_file('r1/', 'v', 'csv')
	class_prepr = c.ClassifierPreprocessing(n_bins=4, word_size=2)

	# coefs = class_prepr.apply_transformation(pure_data.ods['Voltage'], 0, 500, 5)
	# print(len(class_prepr.get_vocabulary()), ': ', class_prepr.get_vocabulary().values())
	# print(coefs)
	#
	# t.plot_series(pure_data.ods['Voltage'], 0, 500, 5)
	# t.bar_series(coefs.toarray())

	class_learn = c.ClassifierLearning(conf.classifier_set_type)
	class_learn.pick_learning_dataset(pure_data.ods, 'Voltage',
									  0, 500, 250, 10000000, class_prepr)
	# plt.show()
# import tools as t
# import configuration as conf
# import numpy as np
# pure_data = t.Data(conf.path, conf.data_set_type)