# -*- coding: utf-8 -*-
import pytest

from rafter import Rafter
from rafter.http import Request


def test_app():
    Rafter(name='plop')

    # No positional arguments
    with pytest.raises(TypeError):
        Rafter('name')


def test_app_request_class():
    class Req(Request):
        pass

    Rafter(request_class=Req)

    class Req2(object):
        pass

    with pytest.raises(RuntimeError):
        Rafter(request_class=Req2)


def test_app_resource():
    app = Rafter()

    @app.resource('/')
    def test(request):
        pass
