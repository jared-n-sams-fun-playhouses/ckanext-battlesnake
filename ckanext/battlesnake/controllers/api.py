from ckan.controllers.api import ApiController

from ckan.common import c
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.model as model
import ckan.plugins.toolkit as toolkit

import logging
from functools import wraps
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


def prep_bs_request(endpoint):
    @wraps(endpoint)
    def wrapper(self, ver=None):
        try:
            game = self._get_request_data(False)
            pprint(game)
        except ValueError, e:
            return self._finish_bad_request(unicode(e))

        if 'width' in game and 'height' in game:
            board = bs_h.get_empty_board(0, game['width'], game['height'])
        else:
            return self._finish_bad_request(_('Missing board size parameters'))

        return endpoint(self, game, board, ver)
    return wrapper


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

    @prep_bs_request
    def start(self, game, board, ver=None):
        data_dict = {
            'color': "#6751AE",
            'taunt': bs_h.get_taunt(),
            'head_url': "https://raw.githubusercontent.com/jared-n-sams-fun-playhouses/00buddies-bs/master/static/head.png",
            'name': "00buddies"
        }
        return self._finish_ok(data_dict)

    @prep_bs_request
    def move(self, game, board, ver=None):
        pprint(c)
        us = bs_h.get_our_snake(game)

        board = bs_h.populate_locations(1, game['food'], board)

        pprint(board)

        data_dict = {
            'move': 'right',
            'taunt': bs_h.get_taunt()
        }
        return self._finish_ok(data_dict)
