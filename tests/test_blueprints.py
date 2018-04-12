# -*- coding: utf-8 -*-
from rafter import Blueprint, Rafter, Response


def test_blueprints_resource():
    bp = Blueprint(name='test')
    app = Rafter()

    @bp.resource('/')
    async def main(request):
        return {'test': 'abc'}

    app.blueprint(bp)

    request, response = app.test_client.get('/')
    assert response.status == 200
    assert response.json == {'test': 'abc'}


def test_blueprints_add_resource():
    bp = Blueprint(name='test')
    app = Rafter()

    async def main(request):
        return {'test': 'abc'}

    bp.add_resource(main, '/')
    app.blueprint(bp)

    request, response = app.test_client.get('/')
    assert response.status == 200
    assert response.json == {'test': 'abc'}


def test_blueprint_extra_kwargs():
    bp = Blueprint('test', url_prefix='/prefix')
    app = Rafter()

    def simple_filter(get_response, params):
        async def decorated_filter(request, *args, **kwargs):
            if request.args.get('a') == '1':
                return Response([1, 2, 3])

            return await get_response(request, *args, **kwargs)

        return decorated_filter

    @bp.resource('/test', validators=[simple_filter])
    async def main(request):
        return {'test': 'abc'}

    app.blueprint(bp)

    request, response = app.test_client.get('/test')
    assert response.status == 404
    assert response.json == {'status': 404,
                             'message': 'Requested URL /test not found'}

    request, response = app.test_client.get('/prefix/test')
    assert response.status == 200
    assert response.json == {'test': 'abc'}

    request, response = app.test_client.get('/prefix/test?a=1')
    assert response.status == 200
    assert response.json == [1, 2, 3]
