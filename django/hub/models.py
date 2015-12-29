from django.db import models

# Create your models here.

class Author(models.Model):
    name  = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

class Project(models.Model):
    name   = models.CharField(max_length=200)
    url    = models.CharField(max_length=200)
    branch = models.CharField(max_length=200)
    query  = models.CharField(max_length=200)

class Commit(models.Model):
    commitid = models.CharField(max_length=200)
    message  = models.CharField(max_length=200)
    author   = models.ForeignKey(Author)
    project  = models.ForeignKey(Project)

class Contribution(models.Model):
    commit   = models.ForeignKey(Commit)
    language = models.CharField(max_length=20)
