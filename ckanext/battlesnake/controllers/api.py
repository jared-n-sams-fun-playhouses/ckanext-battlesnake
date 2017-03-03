from ckan.controllers.api import ApiController

import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.model as model
import ckan.plugins.toolkit as toolkit

import logging
from pprint import pformat, pprint

try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config

import ckanext.battlesnake.helpers as bs_h


# shortcuts
_ = toolkit._

log = logging.getLogger(u'ckanext.battlesnake.controllers.api')


class BSApiController(ApiController):
    """
    Battlesnake Snake Controller
    """
    def __init__(self):
        self.test = "Hallo?"

    def index(self, ver=None):
        data_dict = {
            'test_taunt': bs_h.get_taunt(),
        }
        return toolkit.render('battlesnake/index.html', extra_vars=data_dict)

    def start(self, ver=None):
        data_dict = {
            'color': "#6751AE",
            'taunt': bs_h.get_taunt(),
            'head_url': "TODO",
            'name': "00buddies"
        }
        return self._finish_ok(data_dict)

    def move(self, ver=None):
        data_dict = {
            'move': "up",
            'taunt': "TODO taunt"
        }
        return self._finish_ok(data_dict)
