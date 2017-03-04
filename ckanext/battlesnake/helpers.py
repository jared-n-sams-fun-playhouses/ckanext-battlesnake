import random

from functools import wraps
from time import time

try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(te-ts)
        print('func:%r took: %0.5f msec' % \
            (f.__name__, (te-ts) * 1000.0))
        return result
    return wrap


def get_bs_config():
    """
    Not setup, todo
    """
    namespace = 'ckanext.battlesnake.'
    return dict([(k.replace(namespace, ''), v) for k, v in config.iteritems()
                 if k.startswith(namespace)])


def get_taunt():
    return random.choice([
        "O-oooooooooo",
        "AAAAE-A-A-I-A-U-",
        "JO-oooooooooooo",
        "AAE-O-A-A-U-U-A-",
        "E-eee-ee-eee AAAAE-A-E-I-E-A-",
        "JO-ooo-oo-oo-oo",
        "EEEEO-A-AAA-AAAA",
        ])


def get_invalid_points(data):
    bad_coords = []

    if 'snakes' not in data:
        print('Missing Snakes')
        return bad_coords

    for snake in data['snakes']:
        bad_coords.extend(snake['coords'])

    if debug:
        print("Invalid Points: %s" % bad_coords)

    return bad_coords


def get_our_snake(data):
    if 'snakes' not in data:
        print('Missing Snakes')
        return {}

    for snake in data['snakes']:
        # TODO: move our snake name to config
        if "00buddies" == snake['name']:
            return snake
    else:
        return {}


def get_direction_from_point(head, point):
    if point[0] == head[0]:
        if (point[1] + 1) == head[1]:
            return 'up'
        if (point[1] - 1) == head[1]:
            return 'down'

    if point[1] == head[1]:
        if (point[0] + 1) == head[0]:
            return 'left'
        if (point[0] - 1) == head[0]:
            return 'right'


def get_point_from_direction(move, point):
    if move == 'up':
        return [point[0], (point[1] - 1)]

    if move == 'down':
        return [point[0], (point[1] + 1)]

    if move == 'left':
        return [(point[0] - 1), point[1]]

    if move == 'right':
        return [(point[0] + 1), point[1]]

    return point


def get_empty_board(empty_symbol, width, height):
    return [[empty_symbol for x in range(width)] for y in range(height)]


def mark_locations(mark, points, board):
    for point in points:
        x = point[0]
        y = point[1]
        board[y][x] = mark

    return board


def print_board(board):
    for row in board:
        print(row)
