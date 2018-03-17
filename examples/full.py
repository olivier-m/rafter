# -*- coding: utf-8 -*-
from sanic.exceptions import abort
from sanic.response import text
from rafter import Rafter, Response, ApiError, model_node
from schematics import Model, types

# Let's start our app
app = Rafter()


class InputSchema(Model):
    @model_node()
    class body(Model):
        # This schema is for our input data (json or form url encoded body)
        # - The name takes a default value
        # - The id has a different name than what will be return in the
        #   resulting validated data
        name = types.StringType(default='')  # Change the default value
        id_ = types.IntType(required=True, serialized_name='id')


class TagSchema(Model):
    @model_node()
    class path(Model):
        # For the sake of the demonstration, because it would be easier
        # to set the type in the route URL.
        tag = types.IntType()

    @model_node()
    class params(Model):
        sort = types.StringType(default='asc', choices=('asc', 'desc'))
        page = types.IntType(default=1, min_value=1)


class ReturnSchema(Model):
    name = types.StringType(required=True, min_length=1)

    @model_node(serialized_name='options')  # Let's change the name!
    class params(Model):
        xray = types.BooleanType(default=False)


def basic_filter(get_response, params):
    async def decorated_filter(request, *args, **kwargs):
        if request.args.get('action') == 'abort':
            abort(500, 'Abort!')

        if request.args.get('action') == 'text':
            return text('test response')

        return await get_response(request, *args, **kwargs)

    return decorated_filter


@app.route('/')
async def main(request):
    # Classic Sanic route returning a text/plain response
    return text('Hi mate!')


@app.resource('/post', ['POST'],
              request_schema=InputSchema)
async def post(request):
    # A resource which data are going to be validated before processing
    # Then, we'll return the raw body and the validated data
    # We'll return a response with a specific status code
    return Response({
        'raw': request.form or request.json,
        'validated': request.validated
    }, 201)


@app.resource('/tags/<tag>', ['GET'],
              request_schema=TagSchema)
async def tag(request, tag):
    # Validation and returning data directly
    return {
        'args': request.args,
        'tag': tag,
        'validated': request.validated
    }


@app.resource('/filter', validators=[basic_filter])
async def filtered(request):
    return request.args


@app.resource('/return', ['POST'],
              response_schema=ReturnSchema)
async def return_schema(request):
    return request.json


@app.resource('/error', methods=['GET'])
def error_sync(request):
    raise ApiError('Error', 599, info='Something really bad!')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
