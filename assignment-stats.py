#!/usr/bin/env python
import sys
import numpy
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
	print "One argument, the score sheet."
	exit()

class Assignment:
	def __init__(self, name, skip_zeros=True):
		self.name = name
		self.skip_zeros = skip_zeros
		self._data = []

	def add_score(self, score):
		if self.skip_zeros and int(score) == 0:
			return

		self._data.append(score)

	def mean(self):
		return numpy.average(self._data)

	def stdev(self):
		return numpy.std(self._data)

	def min(self):
		return min(self._data)

	def max(self):
		return max(self._data)

	def median(self):
		return numpy.median(self._data)

	def grades(self):
		f = filter(lambda x: x < 50, self._data)
		p = filter(lambda x: x < 60 and x >= 50, self._data)
		c = filter(lambda x: x < 70 and x >= 60, self._data)
		d = filter(lambda x: x < 80 and x >= 70, self._data)
		hd = filter(lambda x: x > 80, self._data)

		return (len(f), len(p), len(c), len(d), len(hd))

	def within_std(self):
		return len(filter(
			lambda x: x > self.mean() - self.stdev() and x < self.mean() + self.stdev(),
			self._data))

	def above_std(self, stds=1):
		return len(filter(
			lambda x: x > self.mean() + stds * self.stdev(),
			self._data))

	def below_std(self, stds=1):
		return len(filter(
			lambda x: x < self.mean() - stds * self.stdev(),
			self._data))

	def valid(self):
		return len(self._data) > 0

	def show_histogram(self):
		plt.hist(self._data)
		plt.title(self.name)
		plt.show()

assignments = []

with open(sys.argv[1], 'r') as f:
	header_row = f.readline().strip().split(',')
	group_idx = header_row.index('Groups')
	ahdr = header_row[group_idx + 1:]

	for a in ahdr:
		assignments.append(Assignment(a))

	for r in f:
		row = r.split(',')
		marks = row[group_idx + 1:]

		for a, m in zip(assignments,marks):
			try:
				a.add_score(float(m))
			except ValueError:
				pass

for a in assignments:
	if not a.valid() or 'course total' in a.name.lower():
		continue

	print ''
	print '---'
	print a.name
	print '{:.2f} +- {:.2f}  ({:.2f})'.format(a.mean(), a.stdev(), a.median())
	print '{:.2f} - {:.2f}'.format(a.min(), a.max())
	print a.grades()
	print '{} {} ({}) {} {}'.format(a.below_std(2), a.below_std(), a.within_std(), a.above_std(), a.above_std(2))
	a.show_histogram()

print ''
