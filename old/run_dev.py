#!/usr/bin/env python

import json, os, sys
import config
from flask import Flask, Response, send_file, jsonify, abort, request
import api
app = Flask(__name__)


# Deploy project
@app.route('/rounds', methods=['GET'])
def get_rounds_all():
    """Receives value and returns if it looks and smells
       like an int

    Args:
        value: the value to test for int-ness

    Returns:
        bool: JSON with True or False
    """
    all_rounds = api.all()

    return jsonify({'rounds': all_rounds})

# Deploy project
@app.route('/rounds', methods=['POST'])
def add_round():
    """Receives value and returns if it looks and smells
       like an int

    Args:
        value: the value to test for int-ness

    Returns:
        bool: JSON with True or False
    """
    print(request.get_json())
    new_rounds = api.add(request.get_json())

    return jsonify(new_rounds)


# Static Routes
@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)


if __name__ == '__main__':
    app.run(debug=config.debug, host='0.0.0.0', port=5000)