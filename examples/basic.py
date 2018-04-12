# -*- coding: utf-8 -*-
from rafter import Rafter

app = Rafter()


@app.resource('/')
async def main_view(request):
    # This simple view returns a JSON response
    # with the following content.
    return {
        'data': 'It works!'
    }


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
