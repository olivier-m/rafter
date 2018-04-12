# -*- coding: utf-8 -*-
from sanic.exceptions import abort

from rafter import Rafter, ApiError

app = Rafter()


@app.resource('/')
async def main_view(request):
    # Raising any type of exception
    raise ValueError('Something is wrong!')


@app.resource('/api')
async def api_error(request):
    # Raising an ApiError with custom code, a message
    # and extra arguments
    raise ApiError('Something went very wrong.', 599, xtra=12,
                   explanation='http://example.net/')


@app.resource('/sanic')
async def sanic_error(request):
    # Using Sanic's abort function
    abort(599, 'A bad error.')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
