"""Application configuration file.

Load by 'import config', not 'from config import *'
Access properties as 'config.property'
"""

import os, json

exiftool_path = '/usr/local/bin/exiftool'

project_directory = os.path.dirname(os.path.realpath(__file__))

log = True
debug = False