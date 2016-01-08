#!/usr/bin/python

import os
import sys
import re

from csv_output import CsvOutput
from postgres_output import DbOutput

pattern = r"""(.*)
Author: (.*)
Date:   (.*)

    (.*)

 (.*)
 (\d*) files? changed, (\d*) insertions\(\+\)(, (\d*) deletions\(-\))?
"""

class Commit:
    def __init__(self, s):
        global RepoName
        commit = re.match(pattern, s, re.MULTILINE | re.DOTALL).groups()
        self.commitid = commit[0]
        author        = commit[1]
        self.date     = commit[2]
        self.message  = commit[3]
        self.files    = commit[4]
        self.nofiles  = int(commit[5] or 0)
        self.inserts  = int(commit[6] or 0)
        self.removes  = int(commit[8] or 0)
        self.file_list = []
        for f in re.finditer("(.*) \|\s*(\d+) \+", self.files):
            self.file_list.append((f.group(1).strip(), int(f.group(2))))

        m = re.match("(.*) <([^@]+@[^@]+\.[^@]+)>", author)
        if m:
           self.authorName, self.authorEmail = m.groups()
        else:
           self.authorName, self.authorEmail = ("", author)

    def str():
        return "Commit %s a:%s f:%s i:%s d:%s" % (self.commit, self.authorName,
                self.nofiles, self.inserts, self.removes)

def entry(s):
    try:
        return Commit(s)
    except (Exception), e:
        return []

def getHandler(argv):
    if len(argv) < 1:
        return CsvOutput(argv)
    if argv[1] ==  "csv":
        return CsvOutput(argv)
    if argv[1] ==  "db":
        return DbOutput(argv)
    return CsvOutput(argv)

def main(argv):

    handler = getHandler(argv)
    repos   = handler.getRepos()

    for url, branch, handler.repoName, query in repos:
        d = "workdir/"+handler.repoName
        if not os.path.exists(d):
           os.makedirs(d)
           os.popen("cd %s && git clone --bare %s .git" % (d, url)).read()
           prev_head = ""
        else:
           prev_head = os.popen("cd %s && git log -1 --format=%%H" % d).read().strip() + ".."
           print prev_head
           os.popen("cd %s && git fetch %s" % (d, url)).read()

        log = os.popen("cd %s && git log %s --date=iso --stat %s"% (d, prev_head, query)).read();
        entries = log.split("commit ")
        entries = map(entry, entries)
        entries = filter(lambda x:x, entries)
        map(handler, entries)

if __name__ == '__main__':
   main(sys.argv)
