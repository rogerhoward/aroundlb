#!/usr/bin/env python
import os, pipes, json
import config
import click


def metadata(file, options='groupedsimple', format='json'):
    # if file == '': return False

    if config.debug: print file
    if os.path.isfile(file):
        if config.debug: print 'exists'
        exiftool_defaults = ' -m '

        option_string = ''
        if options == 'groupedsimple':
            option_string += '-G -s -s -g '
        if format == 'json':
            option_string += '-json '
        if config.debug: print(option_string)

        command_string = config.exiftool_path + exiftool_defaults + option_string + pipes.quote(file)
        if config.debug: print(command_string)

        exiftool_out = os.popen(command_string).read()
        if config.debug: print(exiftool_out)

        exiftool_dict = json.loads(exiftool_out)
        if config.debug: print(exiftool_dict)

        return exiftool_dict
    else:
        return False

# if __name__ == 'main':
#     metadata()