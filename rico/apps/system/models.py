# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import uuid

from django.db import models


class User(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    password = models.CharField(max_length=60)
    email = models.CharField(max_length=254)
    active = models.BooleanField(default=True)
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField()
    deleted = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'system'
        db_table = 'sys_user'

class AccessLog(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    client_id = models.CharField(max_length=150, blank=True)
    remote_addr = models.CharField(max_length=150)
    user_agent = models.TextField()
    os = models.CharField(max_length=150)
    browser = models.CharField(max_length=150)
    path = models.CharField(max_length=500)
    method = models.CharField(max_length=50)
    query_string = models.TextField()
    request_body = models.TextField()
    ctime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'system'
        db_table = 'sys_access_log'
