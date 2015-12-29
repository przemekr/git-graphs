class CsvOutput:
   def __init__(self, argv):
      self.repoName = ""
      self.output = open("data.csv", "w")
      self.output.write("Repo,Commit,Author,Date,Message,Files,Insert,Delete"+"\n")

   def __call__(self, c):
      self.output.write("%s,%s,'%s','%s','%s',%s,%s,%s\n" % (
         self.repoName, c.commitid, c.authorName, c.date,
         c.message.replace("'", "#"),
         c.nofiles, c.inserts, c.removes))

   def getRepos(self):
      global repos
      execfile("repos")
      return repos


