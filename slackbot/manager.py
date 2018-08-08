# -*- coding: utf-8 -*-

import os
import logging
from glob import glob
from six import PY2
from importlib import import_module
from slackbot.utils import to_utf8

logger = logging.getLogger(__name__)


class PluginsManager(object):
    __instance = None

    def __init__(self, settings):
        ''' PluginManager singleton constructor.
            This method should only execute once and not be called directly.
            All calls to make a connection to the PluginManager should use
            PluginManager.get_instance().'''
        if Plugins.__instance != None:
            raise "Plugins is a Singleton, but was reinitialized"
        else:
            self.settings = settings
            PluginManager.__instance = self

    @staticmethod
    def get_instance(settings=None):
        ''' get_instance(settings=None): (singleton reference)
            The get_instance() method is the way to get a reference to the
            singleton reference of PluginManager. The first call to
            get_instance() needs to send a reference to the Settings
            instance. All calls afterward do not need to call with the
            Settings instance.'''
        if PluginsManager.__instance == None:
            if settings == None:
                raise "PluginsManager requires a Settings object on first invocation"
            PluginsManager(settings)
        return PluginsManager.__instance

    commands = {
        'respond_to': {},
        'listen_to': {},
        'default_reply': {}
    }

    # Shouldn't init_plugins() be called when __init__() is fired?
    def init_plugins(self):
        if hasattr(self.settings, 'PLUGINS'):
            plugins = self.settings.PLUGINS
        else:
            plugins = 'slackbot.plugins'

        for plugin in plugins:
            self._load_plugins(plugin)

    def _load_plugins(self, plugin):
        logger.info('loading plugin "%s"', plugin)
        path_name = None

        if PY2:
            import imp

            for mod in plugin.split('.'):
                if path_name is not None:
                    path_name = [path_name]
                _, path_name, _ = imp.find_module(mod, path_name)
        else:
            from importlib.util import find_spec as importlib_find

            path_name = importlib_find(plugin)
            try:
                path_name = path_name.submodule_search_locations[0]
            except TypeError:
                path_name = path_name.origin

        module_list = [plugin]
        if not path_name.endswith('.py'):
            module_list = glob('{}/[!_]*.py'.format(path_name))
            module_list = ['.'.join((plugin, os.path.split(f)[-1][:-3])) for f
                           in module_list]
        for module in module_list:
            try:
                import_module(module)
            except:
                # TODO Better exception handling
                logger.exception('Failed to import %s', module)

    def get_plugins(self, category, text):
        has_matching_plugin = False
        if text is None:
            text = ''
        for matcher in self.commands[category]:
            m = matcher.search(text)
            if m:
                has_matching_plugin = True
                yield self.commands[category][matcher], to_utf8(m.groups())

        if not has_matching_plugin:
            yield None, None
