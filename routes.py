#!/usr/bin/env python

import json, os, sys
from flask import Blueprint, jsonify, render_template, abort, request
name = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
api = Blueprint(name, __name__)
import config


# Deploy project
@api.route('/is/int/<value>', methods=['GET'])
def is_int(value):
    """Receives value and returns if it looks and smells
       like an int

    Args:
        value: the value to test for int-ness

    Returns:
        bool: JSON with True or False
    """

    try:
        int(value)
        return jsonify({'response':True})
    except:
        return jsonify({'response':False})


# Static Routes
@api.route('/')
def root():
    return api.send_static_file('index.html')


@api.route('/<path:path>')
def static_proxy(path):
    return api.send_static_file(path)
