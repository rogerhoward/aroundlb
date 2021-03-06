import os, sys, string, random, pipes, requests

from django.conf import settings
from celery import shared_task

from pprint import pprint

try: import simplejson as json
except ImportError: import json

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def urlexists(path):
    try:
        r = requests.head(path)
        return r.status_code == requests.codes.ok
    except:
        return False

def urlsize(path):
    try:
        r = requests.head(path)
    except:
        return False
        
    if r.status_code == requests.codes.ok:
        try:
            return int(r.headers['Content-Length'])
        except:
            return False
    else:
        return False


def mkdirp(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)


def get_extension(path):
    return path.split(".")[-1].lower()


def random_string(strlen):
    import random
    import string
    return ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(strlen))
