import os
import sys
import re

log = os.popen("git log --date=iso --stat %s"% " ".join(sys.argv[1:])).read();
entries = log.split("commit ")

pattern = r"""(.*)
Author: (.*)
Date:   (.*)

    (.*)
 (\d*) files changed, (\d*) insertions\(\+\), (\d*) deletions\(-\)
"""


def entry(s):
    try:
        m = re.match(pattern, s, re.MULTILINE| re.DOTALL)
        return m.groups()
    except:
        return []

def printrow(l):
    n = ",%s,%s,%s"%l[-3:]
    escaped = map(lambda x:"'%s'"%x.replace("'", "#"), l[:-3])
    print ",".join(escaped)+n
    fn.write(",".join(escaped)+n+ "\n")

fn = open("/tmp/mygit.csv", "w")
entries = map(entry, entries)
entries = filter(lambda x:x, entries)
print "Commit,Author,Date,Message,Files,Insert,Delete"
fn.write("Commit,Author,Date,Message,Files,Insert,Delete" + "\n")
map(printrow, entries)
