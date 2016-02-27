# -*- coding:utf-8 -*-

from django.http import HttpResponse, HttpResponseForbidden
from rico.apps.system.models import AccessLog

class AccessLogMiddleware(object):
    def process_request(self, request):
        log = AccessLog()
        log.session_id = request.META.get('COOKIES', '')
        log.user_agent = request.META.get('HTTP_USER_AGENT', '')
        log.path = request.path
        log.method = request.method
        log.query_string = request.GET.urlencode()
        log.request_body = request.body
        # get remote address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            log.remote_addr = x_forwarded_for.split(',')[0]
        else:
            log.remote_addr = request.META.get('REMOTE_ADDR', '')
        log.save()
