#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-g', "--group-prefix", help="Prefix of group name to group by. e.g. 'Team' if the groups are called 'Team 1', 'Team 2' etc.")
parser.add_argument('-s', "--score-sheet", help="CSV file containing partial marks to distribute amongst groups")
parser.add_argument('-a', "--assignment-name", help="The assignment name, as listed in the score sheet header row, to work over")
parser.add_argument('-o', "--output-name", help="Output filename (should end in .csv)")
args = parser.parse_args()

scores = {}

unmarked = []
ungrouped = []
groups = []
users = []

if args.output_name is None:
	args.output_name = args.score_sheet + '.out'

def get_group(groups, prefix):
	groups = groups.strip(' ,"\'"')
	for g in groups.split(';'):
		if g.startswith(prefix):
			return g

	return None

with open(args.score_sheet, 'r') as f:
	header_row = f.readline().strip().lower().split(',')
	header_row = [ x.strip(' ,"\'"') for x in header_row ]
	group_idx = header_row.index('groups')
	id_idx = header_row.index('uni id')
	mark_idx = header_row.index(args.assignment_name.lower())

	for r in f:
		row = r.split(',')
		group = get_group(row[group_idx], args.group_prefix)
		mark = row[mark_idx].strip()
		uid = row[id_idx].strip()

		users.append(uid)

		if group is None:
			print("User %s has no matching group" % uid)
			if not uid in ungrouped:
				ungrouped.append(uid)

			continue

		# Ignore no marks or spreadsheet equation errors (which start with '#')
		if mark.startswith(('-','#')):
			continue

		if group in scores:
			print("Duplicate marks for group %s (%s, %s)" % (group, mark, scores[group]))
			continue

		scores[group] = mark
		print("Group %s got %s" % (group, mark))

	with open(args.output_name, 'w') as fo:

		# Go back to the beginning of input file, write out header row
		f.seek(0)
		fo.write(f.readline())

		for r in f:
			row = r.split(',')
			row[mark_idx] = row[mark_idx].strip()
			group = get_group(row[group_idx], args.group_prefix)

			if group is not None:
				if group in scores:
					row[mark_idx] = scores[group]
				else:
					print("Group %s is unmarked" % group)
					if not group in unmarked:
						unmarked.append(group)

			fo.write(','.join(row))
			fo.write('\n')

print "---"
print "%d ungrouped: %s" % (len(ungrouped), ', '.join(ungrouped))
print "%d unmarked: %s" % (len(unmarked), ', '.join(unmarked))
print "---"
print "%d grouped students" % (len(users) - len(ungrouped))
print "%d marked groups" % len(scores)
print "Average %d" % (sum([float(x) for x in scores.values()]) / len(scores))