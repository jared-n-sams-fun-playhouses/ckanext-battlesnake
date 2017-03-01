import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class BattlesnakePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    plugins.implements(plugins.IRoutes, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'battlesnake')

    def before_map(self, map):
        from routes.mapper import SubMapper

        bs_controller = 'ckanext.battlesnake.controllers.api:BSApiController'

        map.connect('battlesnake_index', '/battlesnake', controller=bs_controller, action='index')

        # For mapper method conditions
        POST = {
            "method": ['POST']
        }

        with SubMapper(map, controller=bs_controller) as m:
            m.connect('start', '/start', aciton='start', conditions=POST)
            m.connect('move', '/move', action='move', conditions=POST)