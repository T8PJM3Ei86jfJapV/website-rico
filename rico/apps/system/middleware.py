# -*- coding:utf-8 -*-

from importlib import import_module
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware

from django.http import HttpResponse, HttpResponseForbidden
from rico.apps.system.models import AccessLog


class AccessLogMiddleware(object):
    
    def process_response(self, request, response):
        log = AccessLog()
        # get remote address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            log.remote_addr = x_forwarded_for.split(',')[0]
        else:
            log.remote_addr = request.META.get('REMOTE_ADDR', '')
        log.path = request.path
        log.method = request.method
        log.query_string = request.GET.urlencode()
        log.request_body = request.body
        log.referer = request.META.get('HTTP_REFERER', '')
        log.user_agent = request.META.get('HTTP_USER_AGENT', '')
        log.status_code = response.status_code
        try:
            log.session_id = request.session.session_key
        except:
            pass
        log.save()
        return response


class CustomSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        engine = import_module(settings.SESSION_ENGINE)
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        request.session = engine.SessionStore(session_key)
        if not request.session.exists(request.session.session_key):
            request.session.create()