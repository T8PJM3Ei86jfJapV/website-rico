# -*- coding:utf-8 -*-

from django.contrib.sessions.backends.db import SessionStore as DBStore


class SessionStore(DBStore):
    @classmethod
    def get_model_class(cls):
        from rico.apps.system.models import CustomSession
        return CustomSession

    def create_model_instance(self, data):
        obj = super(SessionStore, self).create_model_instance(data)
        try:
            user_id = int(data.get('_sys_user_id'))
        except (ValueError, TypeError):
            user_id = None
        obj.user_id = user_id
        return obj