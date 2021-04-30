import numpy as np
import tools as t
import time

name = 'v'
path = '../../../data/sets/r2/'  # ../data/sets/r2/

source_file = open(path + name + '.txt', "r")
data_set_type = [('Time', (np.str, 12)), ('Voltage', np.int32)]
arr = []

i = 0
for line in source_file:
	string_values = line.split(" ")
	# time_value = time.strptime(string_values[0], '%H:%M:%S.%f')
	# timestamp = int(time.mktime(time_value))
	# print(timestamp)
	arr.append((string_values[0], string_values[2][:-1]))

data_set = np.array(arr, dtype=data_set_type)  # .T

# np.savetxt(path + name + '.csv', data_set,
# 		newline='\n', delimiter=' ', fmt=['%s', '%d'], comments='жопа')

np.savetxt(path + name + '.csv', data_set,
		newline='\n', delimiter=' ', fmt=['%s', '%d'], comments='')

print(data_set)
print(np.shape(data_set))

# d = t.Data(path, name + '.npy', data_set)
# d.save_dataset()


# d = t.Data('../data/sets/r0/', name + '.npy')
# d.load_dataset()
#
# print(d.ds)
# print("done")