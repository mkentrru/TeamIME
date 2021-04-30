import numpy as np
import matplotlib.pyplot as plt
import pyts.transformation as transformation
# import pyts.approximation as approximation

def die(msg):
	print(msg)
	exit(1)


class Configuration:
	def __init__(self, time_series_size, time_series_length):
		self.time_series_length = time_series_length
		self.time_series_size = time_series_size


class SFAAlg:
	transformed = []

	def __init__(self, ds):  # , coefficients_count):
		self.ods = ds.copy()
		# self.tran = approximation.DiscreteFourierTransform(
		# 	n_coefs=coefficients_count, drop_sum=True)
		self.approx = transformation.BOSS(
			drop_sum=True, n_bins=4, word_size=2
		)

	# def calculate_fourier_coefficients(self):
	#     sig = self.ods[self.cut_pos: self.cut_pos + self.cut_length: 1]
	#     c = np.fft.rfft(sig)
	#     self.apml = c.real
	#     self.phase = c.imag

	def transform(self, cut_position, row_length, time_series_length, time_series_count):
		X = self.ods[cut_position: cut_position + row_length]. \
			reshape(
			time_series_count,
			time_series_length)
		# self.transformed = self.tran.fit_transform(X)
		self.transformed = self.approx.fit_transform(X)
		print(sorted(self.approx.vocabulary_.values()))
		print(len(self.approx.vocabulary_))

	def display_bars(self):
		avarage = np.array((24, 15, 21, 20, 20, 20, 22, 14, 14, 20, 15, 20, 20, 19, 18, 20))

		plt.figure(figsize=(9, 9))
		plt.subplot(111)
		a = self.transformed.toarray()
		column_width = 2
		sub_column_count = np.shape(a)[0]
		sub_column_fix = column_width / sub_column_count
		column_count = np.shape(a)[1]
		x = np.arange(0, (column_width + 0.5) * column_count, column_width + 0.5)

		sub_coumn_index = 0
		for r in a:
			plt.bar(x + sub_coumn_index * sub_column_fix, r, linewidth=sub_column_fix/2)
			sub_coumn_index += 1
		plt.bar(x, avarage, linewidth=0.1)
		# plt.bar(,
		#         a)


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
			self.pd = self.ds.copy()
		if type == 'n':
			self.pd = self.ds / np.linalg.norm(self.ds)
			# self.pds = pp.normalize(self.ds)
		if type == 'sfa-p':
			self.pd = self.ds.copy()
			m = 32
			d = 10

			for i in range(np.shape(self.pd)[0]):
				if abs(m - self.pd[i]) < d:
					self.pd[i] = 0
				else:
					self.pd[i] -= m
			self.pd /= 130

	def plots_show(self):
		plt.show()


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


def display_data_in_rows(data_rows, length, b):
	plot_config = len(data_rows) * 100 + 11
	plt.figure(figsize=(9, 9))
	i = 0
	for set in data_rows:
		plt.subplot(plot_config)
		plot_config += 1
		plt.plot(
			range(b[i], b[i] + length[i]),
			set[b[i]: b[i] + length[i]: 1], linewidth=1.0)
		i += 1
	plt.show()


def display_single_data_in_rows(ds, cut_pos, cut_length, cut_count):
	plot_config = cut_count * 100 + 11
	plt.figure(figsize=(9, 9))

	for i in range(cut_count):
		plt.subplot(plot_config)
		plot_config += 1
		plt.plot(
			range(cut_pos, cut_pos + cut_length),
			ds[cut_pos: cut_pos + cut_length: 1],
			linewidth=1.0)
		cut_pos += cut_length
