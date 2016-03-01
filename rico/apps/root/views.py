# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

from rico.apps.blog.models.post import Post


def index(request):
    posts = Post.objects.filter(published=True, deleted=False).order_by('-pub_time')
    return render(request, 'root/index.html', dict(posts=posts))


def session(request):
    if request.session.get('user_id', False):
        return HttpResponse("You've already commented. %s" % request.session.get('user_id', '233'))
    request.session['user_id'] = '244'
    return HttpResponse('Thanks for your comment!')