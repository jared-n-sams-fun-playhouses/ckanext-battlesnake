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

        return endpoint(self, game, ver)
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
    def start(self, game, ver=None):
        data_dict = {
            'color': "#6751AE",
            'taunt': bs_h.get_taunt(),
            'head_url': "https://raw.githubusercontent.com/jared-n-sams-fun-playhouses/00buddies-bs/master/static/head.png",
            'name': "00buddies"
        }
        return self._finish_ok(data_dict)

    @prep_bs_request
    def move(self, game, ver=None):
        us = bs_h.get_our_snake(game)

        if 'width' in game and 'height' in game:
            width = game['width']
            height = game['height']
        else:
            return self._finish_bad_request(_('Missing board size parameters'))

        board = bs_h.get_empty_board(0, width, height)

        board = bs_h.mark_locations('f', game['food'], board)

        for snake in game['snakes']:
            board = bs_h.mark_locations(1, snake['coords'], board)

        board = flood_fill(board, us['coords'][0], game['food'], width, height)

        print("snakes")
        bs_h.print_board(board)

        data_dict = {
            'move': 'up',
            'taunt': bs_h.get_taunt()
        }
        return self._finish_ok(data_dict)


def available_moves(board, point, width, height):
    available = [
        [point[0], point[1] - 1],
        [point[0], point[1] + 1],
        [point[0] - 1, point[1]],
        [point[0] + 1, point[1]]
        ]

    valid = []

    for p in available:
        if p[0] >= width or p[1] >= height:
            continue

        if board[p[1]][p[0]] > 0:
            continue

        valid.append(p)

    return valid


def flood_fill(board, start, goals, width, height):
    for goal in goals:
        available = available_moves(board, goal, width, height)

        for p in available:
            board[p[1]][p[0]] = 2

    return board
