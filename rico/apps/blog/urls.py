# -*- coding:utf-8 -*-

from django.conf.urls import url

from views import system, post

urlpatterns = [
    url(r'^$', post.index, name='index'),
    url(r'^view/(?P<slug>.*)$', post.view, name='view'),
    
    # back door for refresh post 
    # converting markdown to html and return to view
    url(r'^refresh/(?P<slug>.*)$', post.refresh),

    # url(r'^edit/(?P<post_id>\d+)$', system.edit, name='edit'),
]