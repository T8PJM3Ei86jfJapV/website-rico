# -*- coding:utf-8 -*-

import logging

from rico.apps.blog.models.post import Post


POSTS_PER_PAGE = 5

# maximum of unsigned bigint: 2^64-1
MYSQL_MAX_OFFSET = 18446744073709551615


def query_post_by_page(page):
    # check if all characters in the string are digits
    if page.isdigit() is False:
        raise Exception('Illegal page number, it must be an integer!')

    offset = int(page)

    if offset > MYSQL_MAX_OFFSET:
        raise Exception('Oops, integer number too large!')
    elif offset < 0:
        raise Exception('Oops, negative integer is not supported!')

    start = POSTS_PER_PAGE * (offset - 1)
    end = start + POSTS_PER_PAGE

    return Post.objects.filter(published=True, deleted=False).order_by('-pub_time')[start:end]

    
def query_recent_posts(limit=10):
    return Post.objects.filter(published=True, deleted=False).values('title', 'slug').order_by('-pub_time')[:limit]


def get_page_count():
    total = Post.objects.filter(published=True, deleted=False).count()
    return total / POSTS_PER_PAGE + 1


def get_post_by_slug(slug):
    post = Post.objects.get(slug=slug, published=True, deleted=False)
    if not post:
        raise Exception('Oops, page not found!')
    return post