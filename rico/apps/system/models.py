# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import uuid

from django.contrib.sessions.base_session import AbstractBaseSession
from django.db import models


class FixCharField(models.Field):
    def __init__(self, *args, **kwargs):
        self.max_length = kwargs.get('max_length')
        super(FixCharField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'char(%s)' % self.max_length

    def deconstruct(self):
        name, path, args, kwargs = super(FixCharField, self).deconstruct()
        return name, path, args, kwargs

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
    client_id = FixCharField(max_length=32, blank=True)
    session_id = FixCharField(max_length=32, blank=True)
    remote_addr = models.CharField(max_length=150)
    path = models.CharField(max_length=500)
    method = models.CharField(max_length=50)
    status_code = models.IntegerField(default=0)
    query_string = models.TextField()
    request_body = models.TextField()
    referer = models.CharField(max_length=150, blank=True)
    user_agent = models.TextField()
    ctime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'system'
        db_table = 'sys_access_log'
        
class CustomSession(AbstractBaseSession):
    user_id = models.IntegerField(null=True, db_index=True)

    class Meta:
        app_label = 'system'
        db_table = 'sys_session'

    @classmethod
    def get_session_store_class(cls):
        from rico.apps.system.utils.session import SessionStore
        return SessionStore
