# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import uuid

from django.db import models


class Post(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    markdown = models.TextField(null=True)
    html = models.TextField(null=True)
    published = models.BooleanField(default=False)
    language = models.CharField(max_length=16)
    meta_title = models.CharField(max_length=150, null=True)
    meta_desc = models.CharField(max_length=200, null=True)
    author_id = models.IntegerField()
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    pub_time = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'blog'
        db_table = 'blog_post'
