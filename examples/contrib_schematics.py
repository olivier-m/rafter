# -*- coding: utf-8 -*-
from sanic.response import text
from rafter import Response
from rafter.contrib.schematics import RafterSchematics, model_node
from schematics import Model, types

# Let's create our app
app = RafterSchematics()


# -- Schemas
#
class InputSchema(Model):
    @model_node()
    class body(Model):
        # This schema is for our input data (json or form url encoded body)
        # - The name takes a default value
        # - The id has a different name than what will be return in the
        #   resulting validated data
        name = types.StringType(default='')  # Change the default value
        id_ = types.IntType(required=True, serialized_name='id')

    @model_node()
    class headers(Model):
        # This schema defines the request's headers.
        # It this case, we ensure x-test is a positive integer
        # and we provide a default value.
        x_test = types.IntType(serialized_name='x-test', min_value=0,
                               default=0)


class TagSchema(Model):
    @model_node()
    class path(Model):
        # For the sake of the demonstration, because it would be easier
        # to do that in the route definition.
        tag = types.StringType(regex=r'^[a-z]+$')

    @model_node()
    class params(Model):
        # Request's GET parameters validation
        sort = types.StringType(default='asc', choices=('asc', 'desc'))
        page = types.IntType(default=1, min_value=1)


class ReturnSchema(Model):
    @model_node()
    class body(Model):
        # This schema defines the response data format
        # for the return_schema resource.
        name = types.StringType(required=True, min_length=1)

        @model_node(serialized_name='options')  # Let's change the name!
        class params(Model):
            xray = types.BooleanType(default=False)

    @model_node()
    class headers(Model):
        # Validate and set a default returned header
        x_response = types.IntType(serialized_name='x-response', default=5)


# -- API Endpoints
#
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


@app.resource('/return', ['POST'],
              response_schema=ReturnSchema)
async def return_schema(request):
    # Returns the provided data, so you can see what's going on
    # with the response_schema and data transformation
    return request.json


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
