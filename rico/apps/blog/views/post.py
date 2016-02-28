# -*- coding:utf-8 -*-

from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render

from rico.apps.blog.service.post import query_post_by_page
from rico.apps.blog.service.post import query_recent_posts
from rico.apps.blog.service.post import get_page_count
from rico.apps.blog.service.post import get_post_by_slug
from rico.apps.blog.service.post import refresh_post_by_slug


def index(request):

    current_page = request.GET.get('page', '1')

    try:
        display_posts = query_post_by_page(current_page)
    except Exception as msg:
        return HttpResponseForbidden('<h1>Forbidden: {0}</h1>'.format(msg))
    
    kwags = dict(display_posts = display_posts,
        recent_posts = query_recent_posts(),
        page_count = get_page_count(),
        current_page = current_page,)

    return render(request, 'blog/index.html', kwags)


def view(request, slug):
    try:
        post = get_post_by_slug(slug)
    except Exception as msg:
        raise Http404(msg)
    return render(request, 'blog/view.html', dict(post=post))


def refresh(request, slug):
    try:
        post = refresh_post_by_slug(slug)
    except Exception as msg:
        raise Http404(msg)
    return render(request, 'blog/view.html', dict(post=post))
