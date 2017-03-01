from ckan.controllers.api import ApiController

import ckan.plugins.toolkit as toolkit

import logging


# shortcuts
_ = toolkit._

log = logging.getLogger(u'ckanext.battlesnake.controllers.api')


class BSApiController(ApiController):
	def __init__(self):
		self.test = "Hallo?"

	def index(self, ver=None):
		data_dict = {
			'test': self.test
		}
		return toolkit.render('battlesnake/index.html', extra_vars=data_dict)

	def start(self, ver=None):
		data_dict = {
        	'color': "#6751AE",
    		'taunt': "TODO taunt",
        	'head_url': "TODO",
        	'name': "00buddies"
		}
		return self._finish_ok(data_dict)

	def move(self, ver=None):
		data_dict = {
			'move': "up",
			'taunt': "TODO taunt"
		}
		return self._finish_od(data_dict)