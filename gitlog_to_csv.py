#!/usr/bin/python
import os
import sys
import re

pattern = r"""(.*)
Author: (.*)
Date:   (.*)

    (.*)

 (.*)
 (\d*) files? changed, (\d*) insertions\(\+\)(, (\d*) deletions\(-\))?
"""

def entry(s):
    try:
        commit = re.match(pattern, s, re.MULTILINE| re.DOTALL).groups()
        files = commit[4]
        for f in re.finditer(" (.*) \| (\d*)", files):
            pass # process file name.
        return commit[0:3]+commit[5:7]+commit[8:9]
    except (Exception), e:
        return []

def printrow(l):
    n = ",%s,%s,%s"%l[-3:]
    n = n.replace("None", "0")
    escaped = map(lambda x:"'%s'"%x.replace("'", "#"), l[:-3])
    output.write(name+','+",".join(escaped)+n+"\n")

execfile("repos")

if not os.path.exists("workdir"):
   os.makedirs("workdir")
   os.popen("cd workdir && git init").read()

output = open("data.csv", "w")
output.write("Repo,Commit,Author,Date,Message,Files,Insert,Delete"+"\n")
for url, branch, name, query in repos:
    os.popen("cd workdir && git fetch %s %s"% (url, branch)).read();
    log = os.popen("cd workdir && git log FETCH_HEAD --date=iso --stat %s"% query).read();
    entries = log.split("commit ")
    entries = map(entry, entries)
    entries = filter(lambda x:x, entries)
    map(printrow, entries)
