import psycopg2

DBCONF = {
   "database": "ehub",
}

class DbOutput:
   def __init__(self, argv):
      self.repoName = ""
      self.conn = psycopg2.connect(**DBCONF)
      self.curr = self.conn.cursor()

   def __call__(self, c):
       self.curr.execute("SELECT id FROM hub_author WHERE name =  %s", (c.authorName,))
       row = self.curr.fetchone()
       if not row:
           self.curr.execute("INSERT INTO hub_author VALUES (DEFAULT, %s, %s) RETURNING id",
                   (c.authorName, c.authorEmail))
           row = self.curr.fetchone()
       person_id = row[0]

       self.curr.execute("SELECT id FROM hub_project WHERE name =  %s", (self.repoName,))
       row = self.curr.fetchone()
       project_id = row[0]
       self.curr.execute(
              "INSERT INTO hub_commit\
                      VALUES (DEFAULT, %s, %s, %s, %s)",
                      (c.commitid, c.message, person_id, project_id)
                      )

   def __del__(self):
      self.conn.commit()
      self.conn.close()

   def getRepos(self):
      self.curr.execute("SELECT url, branch, name, query FROM hub_project")
      return self.curr.fetchall()
