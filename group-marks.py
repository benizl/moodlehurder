#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-g', "--group-prefix", help="Prefix of group name to group by. e.g. 'Team' if the groups are called 'Team 1', 'Team 2' etc.")
parser.add_argument('-s', "--score-sheet", help="CSV file containing partial marks to distribute amongst groups")
parser.add_argument('-a', "--assignment-name", help="The assignment name, as listed in the score sheet header row, to work over")
parser.add_argument('-o', "--output-name", help="Output filename (should end in .csv)")
parser.add_argument('-p', "--peer-file", help="Peer assessment file")
args = parser.parse_args()

scores = {}
feedback_adj = {}

unmarked = []
ungrouped = []
groups = []
users = []

feedback_map = {
	'None'				: -10.0,
	'Little'			: -5.0,
	'About Average' 	: 0.0,
	'More than Average' : 5.0,
	'Most'				: 10.0,
}

if args.output_name is None:
	args.output_name = args.score_sheet + '.out'

def get_group(groups, prefix):
	groups = groups.strip(' ,"\'"')
	for g in groups.split(';'):
		if g.startswith(prefix):
			return g

	return None

def normalise_uid(uid):
	uid = uid.lower().strip()
	if not uid.startswith('u'):
		uid = 'u' + uid

	if len(uid) != 8:
		print "Invalid UID %s" % uid

	return uid

def feedback_to_adj(fb):
	if not len(fb):
		return 0

	try:
		adj = feedback_map[fb]
	except KeyError:
		adj = 0
		print "Unknown feedback value %s" % fb

	return adj

def update_feedback(uid, fb):
	if uid in feedback_adj:
		n, total = feedback_adj[uid]
	else:
		n, total = 0, 0

	adj = feedback_to_adj(fb)
	total += adj
	n += 1

	feedback_adj[uid] = (n, total)

def apply_feedback(uid, score):
	try:
		score = float(score)
	except ValueError:
		return score

	if uid in feedback_adj:
		n, total = feedback_adj[uid]
	else:
		n, total = 1, 0

	adj = total / n

	if abs(adj) > 5:
		print "UID %s net adj %f" % (uid, adj)

	return str(score + adj)

if args.peer_file is not None:
	with open(args.peer_file) as f:
		f.readline() # Throw away header
		for l in f:
			time, u1, f1, u2, f2, u3, f3, u4, f4, u5, f5, _, _ = l.split(',')
			u1 = normalise_uid(u1)
			u2 = normalise_uid(u2)
			u3 = normalise_uid(u3)
			u4 = normalise_uid(u4)
			u5 = normalise_uid(u5)

			update_feedback(u1, f1)
			update_feedback(u2, f2)
			update_feedback(u3, f3)
			update_feedback(u4, f4)
			update_feedback(u5, f5)

with open(args.score_sheet, 'r') as f:
	header_row = f.readline().strip().lower().split(',')
	header_row = [ x.strip(' ,"\'') for x in header_row ]
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
		if not len(mark) or mark.startswith(('-','#')):
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
			row = r.strip().split(',')
			row[mark_idx] = row[mark_idx].strip()
			group = get_group(row[group_idx], args.group_prefix)
			uid = row[id_idx].strip()

			if group is not None:
				if group in scores:
					score = apply_feedback(uid, scores[group])
					row[mark_idx] = score
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

try:
	print "Average %d" % (sum([float(x) for x in scores.values()]) / len(scores))
except ValueError:
	pass
