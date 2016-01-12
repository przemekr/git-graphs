from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^author/(?P<id>[0-9]+)/$', views.author, name='author'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search_result/(?P<q>.+)/$', views.search_result, name='search_result'),
    url(r'^project/(?P<id>[0-9]+)/$', views.project, name='project'),
#    url(r'^review/(?P<id>[0-9]+)/$', views.review, name='review'),
#    url(r'^newbook/$', views.newbook, name='newbook'),
    url(r'^about/$', views.about, name='about'),
#    url(r'^login/$', views.login, name='login'),
#    url(r'^logout/$', views.logoutview, name='logoutview'),
#    url(r'^(?P<book_id>[0-9]+)/newreview/$', views.newreview, name='newreview'),
]
