# -*- coding: utf-8 -*-

import os

class Settings:

    def __init__(self):
        self.__data = { 'debug':      False,
                        'plugins':    ['slackbot.plugins'],
                        'errors_to':  None,
                        'api_token':  None,
                      }


        # Setup a comma delimited list of aliases that the bot will respond
        # to. Example: if you set ALIASES='!,$' then a bot which would
        # respond to:
        #    'botname hello'
        # will now also respond to
        #    '$ hello'
        self.__data['aliases']   = ''

        # If you use Slack Web API to send messages (with
        # send_webapi(text, as_user=False) or
        # reply_webapi(text, as_user=False)),
        # you can customize the bot logo by providing Icon or Emoji. If you
        # use Slack RTM API to send messages (with send() or reply()), or if
        # as_user is True (default), the used icon comes from bot settings
        # and Icon or Emoji has no effect.

        # self.bot_icon = 'http://lorempixel.com/64/64/abstract/7/'
        # self.emoji    = ':godmode:'

        # Specify a different reply when the bot is messaged with no
        # matching cmd
        self.__data['default_reply'] = None
    

    def _import_env_settings(self):
        ''' _import_env_settings()
            Scan the current environment for any env vars to configure the
            Settings class. All variables are required to start with
            'SLACKBOT_' and can be any of the accepted setting labels in
            uppercase. '''
        for key in os.environ:
            if key[:9] == 'SLACKBOT_':
                name = key[9:]
                self.setattribute(name, os.environ[key])

    def _import_settings_code(self):
        ''' _import_settings()
            Attempt to load settings from slackbot_settings.py or
            local_settings.py if the former is not found. Any variables
            defined in either of these files, will be registered with the
            Settings class. '''
        try:
            from slackbot_settings import *
            for attr_name in ('DEBUG', 'PLUGINS', 'ERRORS_TO', 'API_TOKEN', 'ALIASES', 'DEFAULT_REPLY', 'default_reply'):
                if attr_name in dir(slackbot_settings):
                    self.setattribute(attr_name, vars(slackbot_settings)[attr_name])
        except ImportError:
            try:
                from local_settings import *
                for attr_name in ('DEBUG', 'PLUGINS', 'ERRORS_TO', 'API_TOKEN', 'ALIASES', 'DEFAULT_REPLY', 'default_reply'):
                    if attr_name in dir(local_settings):
                        self.setattribute(attr_name, vars(local_settings)[attr_name])
            except ImportError:
                pass



    def __getattribute__(self, name):
        return self.__data[name.lower()]

    def __setattribute__(self, name, value):
        self.__data[name.lower()] = value
        return self.__data[name.lower()]
