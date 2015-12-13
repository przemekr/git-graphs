import psycopg2

DBCONF = {
   "database": "eprzrze",
   "user": "eprzrze",
}

class DbOutput:
   def __init__(self, argv):
      self.conn = psycopg2.connect(**DBCONF)
      self.curr = self.conn.cursor()

   def __call__(self, c):
      self.cur.execute(
            "INSERT INTO commits\
                  VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s)",
                  (c.repo, c.commitid, c.message, c.author, c.date, c.nofiles, c.inserts, c.removes)
                  )

   def __del__(self):
      self.conn.commit()
      self.conn.close()
