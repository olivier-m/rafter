# -*- coding: utf-8 -*-
from rafter import Rafter, ApiError, ValidationErrors

app = Rafter()


@app.resource('/')
async def main_view(request):
    # Raising any type of exception
    raise ValueError('Something is wrong!')


@app.resource('/api')
async def api_error(request):
    # Raising an ApiError with custom code, a message
    # and extra arguments
    raise ApiError('Somethin went very wrong', 599, xtra=12,
                   explanation='http://example.net/')


@app.resource('/validation')
async def validation_error(request):
    # Raising a validation error with fake error data
    raise ValidationErrors({
        'body': {
            'options': {
                'val': ['Error message']
            }
        }})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
