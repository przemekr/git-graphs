from django.db import models
from datetime import datetime
from django.db.models import Count

# Create your models here.

class Author(models.Model):
    name  = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    def __unicode__(self):
        return self.name

    @staticmethod
    def topCommiters(limit):
        return Author.objects.annotate(num_commits=Count('commit')).order_by('-num_commits')[:limit]

    @staticmethod
    def contribAuthor(authorid):
        return Author.objects.raw('SELECT * FROM hub_contrib_aggr, hub_author\
                WHERE hub_contrib_aggr.author_id = %s AND hub_author.id = %s' % (authorid, authorid))

class Project(models.Model):
    name   = models.CharField(max_length=200, unique=True)
    url    = models.CharField(max_length=200)
    branch = models.CharField(max_length=200, default="master")
    query  = models.CharField(max_length=200, default="")
    lastFetch = models.DateTimeField(default=datetime.min)
    def __str__(self):
        return self.name

class Commit(models.Model):
    commitid = models.CharField(max_length=200, unique=True)
    message  = models.CharField(max_length=200)
    author   = models.ForeignKey(Author)
    project  = models.ForeignKey(Project)
    def __str__(self):
        return self.message.split("\n")[0]

class Contribution(models.Model):
    commit   = models.ForeignKey(Commit)
    language = models.CharField(max_length=20)
    testCode = models.BooleanField(default=False)
    inserts  = models.IntegerField(default=0)
