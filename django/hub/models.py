from django.db import models
from django.db import connection
from datetime import datetime
from datetime import date
from django.db.models import Count
from ldap_class import LDAP
from hub import settings

ldap_server = LDAP(settings["ldap_server"], settings["ldap_passwd"], settings["ldap_bind"], settings["ldap_base"], settings["default_avatar"])
lastyear = date.today().year - 1;

# Create your models here.
class Author(models.Model):
    name  = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    def __unicode__(self):
        return self.name

    @staticmethod
    def topCommiters(limit):
        #return Author.objects.raw("SELECT author_id as id, count(id) as commits FROM hub_commit where date > now()-'1 year'::interval  group by author_id order by commits desc")[:limit]
        return Author.objects.filter(commit__date__year=lastyear).annotate(num_commits=Count('commit')).order_by('-num_commits')[:limit]

    @staticmethod
    def topCommitersProj(proj, limit):
        return Author.objects.filter(commit__project_id=proj.id).annotate(num_commits=Count('commit')).order_by('-num_commits')[:limit]

    @staticmethod
    def contribAuthor(authorid):
        return Author.objects.raw('SELECT * FROM hub_contrib_aggr, hub_author\
                WHERE hub_contrib_aggr.author_id = %s AND hub_author.id = %s ORDER BY sum DESC' % (authorid, authorid))

    def commits_per_proj(self):
        return Project.objects.raw('SELECT hub_project.id, count(commitid) AS commit_count\
              FROM hub_commit, hub_project\
              WHERE hub_commit.project_id = hub_project.id\
              AND hub_commit.author_id = %s\
              GROUP BY hub_project.id' % self.id)

    def thumbnail(self):
        return ldap_server.mailToThumb(self.name, self.email)

    def commits_timestamps(self):
       cursor = connection.cursor()
       cursor.execute("""
       SELECT extract(epoch from date)
       FROM hub_commit
       WHERE author_id = %s;
       """,
       [self.id])
       return [x[0] for x in cursor.fetchall()]


    def commits_per_week(self):
        cursor = connection.cursor()

        # This is quite complex SQL... I could not find an easier way. 
        # We would like to get number of commits per week for the last year.
        # The previous simpler version would return only the weeks where number
        # of commits is non-zero. Thats is why here we add a one entry for
        # every week, do the GROUP BY and substract 1 from the count()
        cursor.execute("""
SELECT date, count(message)-1 AS nr_commits
FROM (
      SELECT
         to_char(now() - ( n || ' week')::interval, 'YY-WW') AS date,
         '' AS message
         FROM generate_series(0, 51) n
      UNION
      SELECT
         to_char(hub_commit.date, 'YY-WW'),
         commitid
         FROM hub_commit
         WHERE hub_commit.date > now() - '51 week'::interval
         AND hub_commit.author_id = %s
      ) AS commits
GROUP BY date
ORDER BY date;
""",
        [self.id])
        return cursor.fetchall()

class Project(models.Model):
    name   = models.CharField(max_length=200, unique=True)
    url    = models.CharField(max_length=200)
    branch = models.CharField(max_length=200, default="master")
    query  = models.CharField(max_length=200, default="")
    lastFetch = models.DateTimeField(default=datetime.min)

    def __str__(self):
        return self.name

    def commits_timestamps(self):
       cursor = connection.cursor()
       cursor.execute("""
       SELECT extract(epoch from date)
       FROM hub_commit
       WHERE project_id = %s;
       """,
       [self.id])
       return [x[0] for x in cursor.fetchall()]

    @staticmethod
    def topProjects(limit):
        return Project.objects.filter(commit__date__year=lastyear).annotate(num_commits=Count('commit')).order_by('-num_commits')[:limit]

    @staticmethod
    def commitProject(pid):
        return Author.objects.raw('SELECT * FROM hub_contrib_proj, hub_project \
                WHERE hub_contrib_proj.project_id = %s AND hub_project.id = %s' % (pid, pid))


class Commit(models.Model):
    commitid = models.CharField(max_length=200, unique=True)
    message  = models.CharField(max_length=200)
    author   = models.ForeignKey(Author)
    project  = models.ForeignKey(Project)
    date     = models.DateTimeField(default=datetime.min)
    def __str__(self):
        return self.message.split("\n")[0]

class Contribution(models.Model):
    commit   = models.ForeignKey(Commit)
    language = models.CharField(max_length=20)
    testCode = models.BooleanField(default=False)
    inserts  = models.IntegerField(default=0)
