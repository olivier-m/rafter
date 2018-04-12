# -*- coding: utf-8 -*-
"""
.. autoclass:: Blueprint
"""

from sanic.blueprints import Blueprint as BaseBlueprint, FutureRoute

__all__ = ('Blueprint',)


class Blueprint(BaseBlueprint):
    """Create a new blueprint.

    :param name: unique name of the blueprint
    :param url_prefix: URL to be prefixed before all route URLs
    :param strict_slashes: strict to trailing slash

    .. automethod:: add_resource
    .. automethod:: resource
    """

    def __init__(self, *args, **kwargs):
        super(Blueprint, self).__init__(*args, **kwargs)

        self.resources = []

    def register(self, app, options):
        super(Blueprint, self).register(app, options)

        url_prefix = options.get('url_prefix', self.url_prefix)

        for future, kwargs in self.resources:
            future.handler.__blueprintname__ = self.name
            uri = url_prefix + future.uri if url_prefix else future.uri
            version = future.version or self.version

            app.resource(uri=uri[1:] if uri.startswith('//') else uri,
                         methods=future.methods,
                         host=future.host or self.host,
                         strict_slashes=future.strict_slashes,
                         stream=future.stream,
                         version=version,
                         name=future.name,
                         **kwargs)(future.handler)

    def resource(self, uri, methods=frozenset({'GET'}), host=None,
                 strict_slashes=None, stream=False, version=None, name=None,
                 **kwargs):
        """
        Create a blueprint resource route from a decorated function.

        :param uri: endpoint at which the route will be accessible.
        :param methods: list of acceptable HTTP methods.
        :param host:
        :param strict_slashes:
        :param version:
        :param name: user defined route name for url_for
        :return: function or class instance

        Accepts any keyword argument that will be passed to the app resource.
        """
        if strict_slashes is None:
            strict_slashes = self.strict_slashes

        def decorator(handler):
            self.resources.append((
                FutureRoute(handler, uri, methods, host, strict_slashes,
                            stream, version, name),
                kwargs))

            return handler
        return decorator

    def add_resource(self, handler, uri, methods=frozenset({'GET'}),
                     host=None, strict_slashes=None, version=None, name=None,
                     **kwargs):
        """
        Create a blueprint resource route from a function.

        :param uri: endpoint at which the route will be accessible.
        :param methods: list of acceptable HTTP methods.
        :param host:
        :param strict_slashes:
        :param version:
        :param name: user defined route name for url_for
        :return: function or class instance

        Accepts any keyword argument that will be passed to the app resource.
        """
        self.resource(uri=uri, methods=methods, host=host,
                      strict_slashes=strict_slashes, version=version,
                      name=name, **kwargs)(handler)
