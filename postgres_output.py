import psycopg2

DBCONF = {
   "database": "ehub",
}

def langFromName(name):
   if name.endswith('.h'):
      return "C"
   if name.endswith('.c'):
      return "C"
   if name.endswith('.cpp'):
      return "C++"
   if name.endswith('.cc'):
      return "C++"
   if name.endswith('.hpp'):
      return "C++"
   if name.endswith('.rb'):
      return "Ruby"
   if name.endswith('.exp'):
      return "Expect"
   if name.endswith('.py'):
      return "Python"
   if name.endswith('.R'):
      return "R"
   if name.endswith('.erl'):
      return "Erlang"
   return "Other"

def testCode(name):
   return name.count("test") != 0

class DbOutput:
   def __init__(self, argv):
      self.repoName = ""
      self.conn = psycopg2.connect(**DBCONF)
      self.curr = self.conn.cursor()

   def __call__(self, c):
       self.curr.execute("SELECT id FROM hub_author WHERE email =  %s", (c.authorEmail,))
       row = self.curr.fetchone()
       if not row:
           self.curr.execute("INSERT INTO hub_author VALUES (DEFAULT, %s, %s) RETURNING id",
                   (c.authorName, c.authorEmail))
           row = self.curr.fetchone()
       person_id = row[0]

       self.curr.execute("SELECT id FROM hub_project WHERE name =  %s", (self.repoName,))
       row = self.curr.fetchone()
       project_id = row[0]

       self.curr.execute("SELECT commitid FROM hub_commit WHERE commitid =  %s", (c.commitid,))
       row = self.curr.fetchone()
       if not row:
          self.curr.execute(
                "INSERT INTO hub_commit\
                      VALUES (DEFAULT, %s, %s, %s, %s, %s) RETURNING id",
                      (c.commitid, c.message, person_id, project_id, c.date)
                      )
          row = self.curr.fetchone()
          commit_id = row[0]
          for f, updates in c.file_list:
             print c.commitid, f,updates
             self.curr.execute(
                   "INSERT INTO hub_contribution\
                         VALUES (DEFAULT, %s, %s, %s, %s)",
                         (langFromName(f), commit_id, updates, testCode(f))
                         )

   def __del__(self):
      self.conn.commit()
      self.conn.close()

   def getRepos(self):
      self.curr.execute("SELECT url, branch, name, query FROM hub_project")
      return self.curr.fetchall()
