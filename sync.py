#!/usr/bin/env python
import os, pipes, json
import config
import click


def metadata(file, options='groupedsimple', format='json'):
    # if file == '': return False

    if os.path.isfile(file):
        print 'exists'
        exiftool_defaults = ' -m '

        option_string = ''
        if options == 'groupedsimple':
            option_string += '-G -s -s -g '
        if format == 'json':
            option_string += '-json '
        print(option_string)

        command_string = config.exiftool_path + exiftool_defaults + option_string + pipes.quote(file)
        print(command_string)

        exiftool_out = os.popen(command_string).read()
        print(exiftool_out)

        exiftool_dict = json.loads(exiftool_out)
        print(exiftool_dict)

        return exiftool_dict
    else:
        return False


@click.command()
@click.option('--file')
def process_file(file):
    m = metadata(file)
    print(m)
    return m


if __name__ == '__main__':
    m = process_file()
    pprint.pprint(m, width=1)