# -*- coding:utf-8 -*-

import uuid

import httpagentparser

from django.http import HttpResponse, HttpResponseForbidden

from rico.apps.system.models import AccessLog

CLIENTID_MAX_AGE = 86400 * 3650 # 10 years


class ClientIdentifyMiddleware(object):
    # your desired cookie will be available in every django view
    def process_request(self, request):
        # will only add cookie if request does not have it already
        if request.COOKIES.get('clientid', None):
            request.clientid_exists = True
        else:
            request.COOKIES['clientid'] = uuid.uuid4().hex
            request.clientid_exists = False

    # your desired cookie will be available in every HttpResponse parser like browser but not in django view
    def process_response(self, request, response):
        if not request.clientid_exists and request.COOKIES.get('clientid', None):
            response.set_cookie('clientid', request.COOKIES.get('clientid'), max_age=CLIENTID_MAX_AGE)
        return response


class AccessLogMiddleware(object):
    
    def process_response(self, request, response):
        log = AccessLog()
        log.client_id = request.COOKIES.get('clientid', '')
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
        log.os, log.browser = httpagentparser.simple_detect(log.user_agent)
        log.status_code = response.status_code
        try:
            log.session_id = request.session.session_key
        except:
            pass
        log.save()
        return response