#!/usr/bin/env python

CONFIG_STRING = """#Basic settings
DYNACONF_CNPJ="00000000000000"
DYNACONF_PASSWORD="uP455wD"

# Dev
DYNACONF_EVENTS_MOCK="12345678901234"
"""

# Writing our configuration file to '.env'
with open('.env', 'w') as configfile:
    configfile.write(CONFIG_STRING)
