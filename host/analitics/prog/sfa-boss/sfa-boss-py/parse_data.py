import numpy as np
import configuration as conf


def parse_data(subdir='r2/', name='v'):
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
		arr.append((string_values[0], string_values[2][:-1]))

	data_set = np.array(arr, dtype=data_set_type)  # .T


	np.savetxt(path + name + '.csv', data_set,
			newline=conf.csv_newline, delimiter=conf.csv_delimiter,
			fmt=conf.csv_fmt)

	print(data_set)
	print(np.shape(data_set))

	print("done")