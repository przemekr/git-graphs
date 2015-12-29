from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from models import *


def index(request):
    active_project_list = Project.objects.order_by('name')[:5]
    active_author_list = Author.objects.order_by('name')[:5]
    context = {
          'active_project_list': active_project_list,
          'active_author_list': active_author_list
          }
    return render(request, 'hub/index.html', context)

def search(request):
    q = request.POST['query']
    return HttpResponseRedirect(reverse('search_result', args=(q,)))

