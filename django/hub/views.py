from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.staticfiles import finders
from models import *
from hub import settings


def index(request):
    MAX_NUM_TO_DISPLAY = 10
    active_project_list = Project.topProjects(MAX_NUM_TO_DISPLAY)
    active_author_list = Author.topCommiters(MAX_NUM_TO_DISPLAY)
    context = {
          'active_project_list': active_project_list,
          'active_author_list': active_author_list
          }
    return render(request, 'hub/index.html', context)

def author(request, id):
    author = Author.objects.get(pk=id)
    author_contrib = filter(lambda c:c.language != "Other", Author.contribAuthor(id))
    context = {
          'author': author,
          'author_contrib': author_contrib,
          'thumbnail': author.thumbnail(),
          'commits': author.commit_set.order_by('-date')[:10],
          'author_commit_per_month': author.commits_per_week(),
          'author_commit_per_proj': author.commits_per_proj(),
          'author_commit_timestamps': author.commits_timestamps()
          }
    return render(request, 'hub/author.html', context)

def project(request, id):
    project = Project.objects.get(pk=id)
    project_contrib= filter(lambda c:c.language != "Other", Project.commitProject(id))
    video = finders.find('hub/%s.mp4' % project.name) and '/static/hub/%s.mp4'%project.name or None
    contributors = Author.topCommitersProj(project, 8)

    context = {
          'project': project,
          'project_contrib': project_contrib,
          'commits': project.commit_set.order_by('-date')[:10],
          'video': video,
          'commit_timestamps': project.commits_timestamps(),
          'contributors': contributors
          }
    return render(request, 'hub/project.html', context)

def about(request):
    context = {
          'settings': settings
          }
    return render(request, 'hub/about.html', context)

def search(request):
    q = request.POST['query']
    return HttpResponseRedirect(reverse('search_result', args=(q,)))

def search_result(request, q):
    authors = (
          Author.objects.filter(name__contains=q) |\
          Author.objects.filter(email__contains=q)
          ).order_by('name')
    projects = (
          Project.objects.filter(name__icontains=q)
          ).order_by('name')

    context = {
          'authors': authors,
          'projects': projects,
          }
    return render(request, 'hub/search_result.html', context)

