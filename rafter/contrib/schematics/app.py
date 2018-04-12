# -*- coding: utf-8 -*-
"""
.. autoclass:: rafter.contrib.schematics.app.RafterSchematics
"""

from rafter.app import Rafter
from rafter.contrib.schematics.filters import (
    filter_validate_schemas, filter_validate_response)

__all__ = ('RafterSchematics', )


class RafterSchematics(Rafter):
    """
    .. autoattribute:: default_filters

    .. automethod:: resource

        :param request_schema: Schema for request data
        :param response_schema: Schema for response data

    .. automethod:: add_resource

        :param request_schema: Schema for request data
        :param response_schema: Schema for response data
    """

    default_filters = \
        [filter_validate_schemas] \
        + Rafter.default_filters \
        + [filter_validate_response]
    """
    - Validate request data
    - Pass Rafter's default filters
    - Validate output data
    """
