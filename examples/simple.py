# -*- coding: utf-8 -*-
from rafter import Rafter, ApiError, Response

# Our main Rafter App
app = Rafter()


@app.resource('/')
async def main_view(request):
    # Simply return arbitrary data and the response filter
    # will convert it to a sanic.response.json response.
    return {
        'data': 'Hello there!'
    }


@app.resource('/p/<param>')
async def with_params(request, param):
    # Just return the request's param in a list.
    return [param]


@app.resource('/status')
async def status(request):
    # Return a 201 response with some data
    return Response({'test': 'abc'}, 201)


@app.resource('/error')
async def error_response(request):
    # Return an error response with a status code and some extra data.
    raise ApiError('Something bad happened!', 501,
                   extra_data=':(')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
