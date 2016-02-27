# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

from rico.apps.blog.models.post import Post


def index(request):
    posts = Post.objects.filter(published=True, deleted=False).order_by('-pub_time')
    return render(request, 'root/index.html', dict(posts=posts))