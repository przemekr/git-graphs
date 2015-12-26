import psycopg2

DBCONF = {
   "database": "github",
}

class DbOutput:
   def __init__(self, argv):
      self.conn = psycopg2.connect(**DBCONF)
      self.curr = self.conn.cursor()

   def __call__(self, c):
       self.curr.execute("SELECT id FROM person WHERE name =  %s", (c.author,))
       row = self.curr.fetchone()
       if not row:
           self.curr.execute("INSERT INTO person VALUES (DEFAULT, %s, %s, %s, %s) RETURNING id",
                   (c.author, "", 0, 0))
           row = self.curr.fetchone()
       person_id = row[0]

       self.curr.execute("SELECT id FROM project WHERE name =  %s", (c.repo,))
       row = self.curr.fetchone()
       if not row:
           self.curr.execute("INSERT INTO project VALUES (DEFAULT, %s, %s, %s, %s) RETURNING id",
                   (c.repo, "", 0, 0))
           row = self.curr.fetchone()
       project_id = row[0]
       self.curr.execute(
              "INSERT INTO commits\
                      VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)",
                      (c.commitid, project_id, person_id, c.inserts, c.nofiles, c.message)
                      )

   def __del__(self):
      self.conn.commit()
      self.conn.close()
