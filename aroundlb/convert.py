#!/usr/bin/env python

from django.conf import settings
import os
from pipes import quote
import argparse

def make_pano(in_path):
    print 'make_pano: %s'.format(in_path)

    data = {'bin': settings.KRPANO_BIN, 
            'template': settings.KRPANO_TEMPLATE, 
            'input': in_path
            }
            
    command_string =  '{bin} makepano -config={template} {input}'.format(*data)
    metaobj = os.popen(command_string).read()
    print command_string
    return out_path



import argparse
parser = argparse.ArgumentParser()
parser.add_argument("path")
args = parser.parse_args()
make_pano(args.path)