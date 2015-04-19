#!/usr/bin/env python
import sys
import numpy

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

	def valid(self):
		return len(self._data) > 0

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
	if not a.valid():
		continue

	print ''
	print '---'
	print a.name
	print '{:.2f} +- {:.2f}'.format(a.mean(), a.stdev())
	print '{:.2f} - {:.2f}'.format(a.min(), a.max())
	
print ''
