#!/usr/bin/env python

import sys


inputfile = sys.argv[1]
prefix = sys.argv[2]

groupsets = sys.argv[3:]
ngroups = len(groupsets)

if ngroups < 2:
	print "Usage: class-lister.py INPUT.csv PREFIX Tag,g1,g2,g3 Tag,g4,g5 ..."
	print "e.g. class-lister.py users.csv 'Prac' Alice,1,2,3 Bob,4,5,6,7"
	exit()

groups = {}

for i in range(ngroups):
	groups[i] = []

def get_groupset(group):
	for i, s in enumerate(groupsets):
		for g in s.split(','):
			gp = group.split(' ')[0]
			gn = group.split(' ')[1]
			if gp == prefix and gn == g:
				return i

	return None

def get_group(groups, prefix):
	for g in groups.split(';'):
		if g.startswith(prefix):
			return g

	return None

with open(inputfile, 'r') as f:
	header_row = f.readline().strip().lower().split(',')
	group_idx = header_row.index('groups')
	id_idx = header_row.index('uni id')
	fn_idx = header_row.index('first name')
	ln_idx = header_row.index('surname')

	for r in f:
		row = r.split(',')
		group = get_group(row[group_idx], prefix)
		uid = row[id_idx].strip()
		fn = row[fn_idx].strip()
		ln = row[ln_idx].strip()

		if group is None:
			print("User %s has no matching group" % uid)
			continue

		gs = get_groupset(group)
		if gs is None:
			print("No groupset for %s" % group)
			continue

		groups[gs].append("%s, %s (%s)" % (ln, fn, uid))


for s in groups:
	with open("groupsets-" + groupsets[s].split(',')[0] + ".txt", 'w') as f:
		for n in sorted(groups[s]):
			f.write(n)
			f.write('\n')