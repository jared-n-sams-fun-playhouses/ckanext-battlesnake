from ckan.controllers.api import ApiController

from ckan.common import c
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.model as model
import ckan.plugins.toolkit as toolkit

import logging
import random
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
            #pprint(game)
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
        print(game)
        data_dict = {
            'color': "#6751AE",
            'taunt': bs_h.get_taunt(),
            'head_url': "https://i.makeagif.com/media/8-12-2016/QOEcU-.gif",
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

        board = bs_h.get_empty_board(9000, width, height)

        board = bs_h.mark_locations(1, game['food'], board)

        for snake in game['snakes']:
            board = bs_h.mark_locations(0, snake['coords'], board)

        flood_fill(board, game['food'], width, height)

        #print("snakes")
        #bs_h.print_board(board)

        head = us['coords'][0]

        moves = available_moves(head, width, height)

        next_move = find_nearest_food(board, head, moves, False, width, height, game)

        data_dict = {
            'move': next_move,
            'taunt': bs_h.get_taunt()
        }
        print(next_move)
        return self._finish_ok(data_dict)

def find_nearest_food(board, head, available, stuck, width, height, game):
    us = bs_h.get_our_snake(game)

    if us['health_points'] > 65 and len(us['coords']) > 6 and stuck == False:
        board = bs_h.mark_locations(9000, game['food'], board)
        board = bs_h.mark_locations(1, [head], board)
        flood_fill(board, head, width, height)
        available = available_moves(head, width, height)


    move_dict = {}
    for move in available:
        turn = board[move[1]][move[0]]
        if turn != 0:
            direction = bs_h.get_direction_from_point(head, move)
            move_dict.update({direction:turn})
        sorted_moves = sorted(move_dict.items(),key=lambda x:x[1])

    if sorted_moves[0][1] == 9000 and stuck == False:
        return make_smart_move(board, head, width, height, game)

    if stuck == True:
        return sorted_moves[0][0]

    return sorted_moves[0][0]

def make_smart_move(board, head, width, height, game):
    print("building smart move...")
    board = bs_h.get_empty_board(9000, width, height)
  
    for snake in game['snakes']:
        board = bs_h.mark_locations(0, snake['coords'], board)

    board = bs_h.mark_locations(1, [head], board)
    flood_fill(board, head, width, height)
    moves = available_moves(head, width, height)

    return find_nearest_food(board, head, moves, True, width, height, game)

def available_moves(point, width, height):
    available = [
        [point[0], point[1] - 1],
        [point[0], point[1] + 1],
        [point[0] - 1, point[1]],
        [point[0] + 1, point[1]]
        ]

    valid = []

    for move in available:
        if move[0] < 0 or move[0] >= width:
            continue

        if move[1] < 0 or move[1] >= height:
            continue

        valid.append(move)

    return valid


def mark_point(turn, point, board, width, height):
    available = available_moves([point[0], point[1]], width, height)
    for move in available:
        if board[move[1]][move[0]] == 0 or board[move[1]][move[0]] <= turn:
            continue

        if width > 20 and turn > 29:
            continue

        board[move[1]][move[0]] = turn
        mark_point(turn + 1, move, board, width, height)


def flood_fill(board, goals, width, height):
    for y_i, y_v in enumerate(board):
        for x_i, x_v in enumerate(y_v):
            if x_v == 1:
                mark_point(2, [x_i, y_i], board, width, height)
