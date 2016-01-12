from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from models import *


def index(request):
    active_project_list = Project.topProjects(5)
    active_author_list = Author.topCommiters(5)
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
          'commits': author.commit_set.order_by('-date')[:10],
          'author_commit_per_month': author.commits_per_week(),
          'author_commit_per_proj': author.commits_per_proj()
          }
    return render(request, 'hub/author.html', context)

def project(request, id):
    project = Project.objects.get(pk=id)
    project_contrib= filter(lambda c:c.language != "Other", Project.commitProject(id))
    context = {
          'project': project,
          'project_contrib': project_contrib,
          'commits': project.commit_set.order_by('-date')[:10]
          }
    return render(request, 'hub/project.html', context)

def about(request):
    context = { }
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

