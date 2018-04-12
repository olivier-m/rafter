# -*- coding: utf-8 -*-
import plistlib

from sanic.exceptions import abort
from sanic.response import text, HTTPResponse

from rafter import Rafter

# Our primary Rafter App
app = Rafter()


# Input filter
def basic_filter(get_response, params):
    # This filter changes the response according to the
    # request's GET parameter "action".
    async def decorated_filter(request, *args, **kwargs):
        # When ?action=abort
        if request.args.get('action') == 'abort':
            abort(500, 'Abort!')

        # When ?action=text
        if request.args.get('action') == 'text':
            return text('test response')

        # Go on with the request
        return await get_response(request, *args, **kwargs)

    return decorated_filter


# Output filter
def output_filter(get_response, params):
    # This filter is going to serialize our data into a plist value
    # and send the result as a application/plist+xml response
    # if the request's Accept header is correctly set.
    async def decorated_filter(request, *args, **kwargs):
        response = await get_response(request, *args, **kwargs)

        # Don't do it like that please!
        accept = request.headers.get('accept', '*/*')
        if accept != 'application/plist+xml':
            return response

        # Actually, here you should check if you have a Response instance
        # In this example we don't really need to.

        # You accept plist? Here you go!
        return HTTPResponse(plistlib.dumps(response.data).decode('utf-8'),
                            content_type='application/plist+xml')

    return decorated_filter


@app.resource('/input', validators=[basic_filter])
async def filtered_in(request):
    # See what happens when we add a filter in "validators"
    return request.args


@app.resource('/output', methods=['POST'], validators=[output_filter])
async def filtered_out(request):
    # Return what we received in json
    return request.json


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
