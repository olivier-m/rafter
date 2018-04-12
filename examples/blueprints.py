# -*- coding: utf-8 -*-
from rafter import Blueprint, Rafter

bpv1 = Blueprint('v1', url_prefix='/v1')
bpv2 = Blueprint('v2')


def header_filter(get_response, params):
    async def decorated_filter(request, *args, **kwargs):
        response = await get_response(request, *args, **kwargs)
        response.headers['x-test'] = 'abc'
        return response

    return decorated_filter


@bpv1.resource('/')
async def v1_root(request):
    return {'version': 1}


@bpv1.resource('/test')
async def v1_test(request):
    return [3, 2, 1]


@bpv2.resource('/', validators=[header_filter])
async def v2_root(request):
    return {'version': 2}


app = Rafter()
app.blueprint(bpv1)
app.blueprint(bpv2, url_prefix='/v2')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
