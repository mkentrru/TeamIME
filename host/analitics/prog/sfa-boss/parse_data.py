import numpy as np
import tools as t

name = 'v'

source_file = open('../data/sets/r1/' + name + '.txt', "r")
data_offset = 15
arr = []

i = 0
for line in source_file:
    str_value = line[data_offset:-1:1]
    # print(str_value)
    value = float(str_value)
    # print(value)
    arr.append(value)
print(arr)
data_set = np.array(arr)
print(data_set)
d = t.Data('../data/sets/r1/', name + '.npy', data_set)
d.save_dataset()


# d = t.Data('../data/sets/r0/', name + '.npy')
# d.load_dataset()
#
# print(d.ds)
# print("done")