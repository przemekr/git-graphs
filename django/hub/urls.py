from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^author/(?P<id>[0-9]+)/$', views.author, name='author'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search_result/(?P<q>.+)/$', views.search_result, name='search_result'),
    url(r'^project/(?P<id>[0-9]+)/$', views.project, name='project'),
    url(r'^commit/(?P<id>[0-9]+)/$', views.commit, name='commit'),
    url(r'^about/$', views.about, name='about'),
]
