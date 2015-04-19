Moodle Hurder
-------------

A collection of Python scripts designed to manipulate CSV files to/from Moodle.

Group Marker
------------
Takes a score entered against one student in a group and allocates it to all students in a group.  Especially useful when marking through tools like Turnitin that don't natively support group marking.

```
python group-marks.py --group-prefix "Team: " --score-sheet markfile.csv --assignment-name "Turnitin Assignment: Major Report" --output-name major-report-output.csv
```

*Group Prefix:* Prefix string to match students in the same group. If students are in groups like "Team: Cool kids", "Team: Other guys" then this should be set to "Team:"

*Score Sheet:* File generated using Moodle grade export with grades entered against only one student in each group.

*Assignment Name:* Name of the assignment that's being marked (must match the column heading in the grade export).

*Output Name:* File name of output file. This can be imported back in to Moodle's gradebook.


Class Lister
------------
Generates lists of students in (sets of) groups.

```
python class-lister.py markbook.csv "Prac " Alice,1,2,3 Bob,4,5,6
```

Will generate two output files, the first containing all the students from groups "Prac 1", "Prac 2" etc, the other "Prac 4", "Prac 5". The file names will be marked for Alice and Bob respectively (these labels are optional).

If you don't want a standard prefix, an empty string should be entered instead.

```
python class-lister.py markbook.csv '' Alice,Mechatronics Bob,Software
```

The /markbook.csv/ input file is an export from the Moodle grade book. It may or may not contain any grades, it's only used for names and group allocations.


Assignment Stats
----------------
Summarises the marks from all assignments in a Moodle marks export CSV file.

```
python assignment-stats.py markbook.csv
```

Output in the form

Assignment Name
Average +- Std
Min - Max


Licence
-------
All files released under GPLv3+ unless otherwise specified.
