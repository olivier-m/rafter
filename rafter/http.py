# -*- coding: utf-8 -*-
from sanic.request import Request as BaseRequest
from sanic.response import json

__all__ = ('Response',)


class Request(BaseRequest):
    __slots__ = BaseRequest.__slots__ + ('validated',)

    def __init__(self, *args, **kwargs):
        super(Request, self).__init__(*args, **kwargs)
        self.validated = {}


class Response(object):
    def __init__(self, data, status: int=200, headers: dict={}):
        self.data = data
        self.status = status
        self.headers = headers

    def response(self):
        return json(self.data, status=self.status, headers=self.headers)
