# -*- coding: utf-8 -*-
import pytest

from rafter import App
from rafter.http import Request


def test_app():
    App(name='plop')

    # No positional arguments
    with pytest.raises(TypeError):
        App('name')


def test_app_request_class():
    class Req(Request):
        pass

    App(request_class=Req)

    class Req2(object):
        pass

    with pytest.raises(RuntimeError):
        App(request_class=Req2)


def test_app_resource():
    app = App()

    @app.resource('/')
    def test(request):
        pass
