class CsvOutput:
   def __init__(self, argv):
      self.output = open("data.csv", "w")
      self.output.write("Repo,Commit,Author,Date,Message,Files,Insert,Delete"+"\n")

   def __call__(self, c):
      self.output.write("%s,%s,'%s','%s','%s',%s,%s,%s\n" % (
         c.repo, c.commitid, c.author, c.date,
         c.message.replace("'", "#"),
         c.nofiles, c.inserts, c.removes))
