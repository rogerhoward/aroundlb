import json, os, sys
import config
from flask import Flask, Response, send_file, jsonify, abort, request
import rethinkdb as r

def all():
    """Get all rounds from database.

    Args:
         none

    Returns:
        bool: result object if successful, False otherwise.
    """

    if config.log: print('getting all...')

    # Setup database variables
    db_name = 'aroundlb'
    table_name = 'rounds'

    # Connect to RethinkDB
    r.connect('localhost', 28015).repl()
    # Insert message into table <name>
    if config.log: print('Getting...')
    # response = r.db(db_name).table(table_name).run()

    documents = []
    cursor = r.db(db_name).table(table_name).run()
    for document in cursor:
        documents.append(document)

    return documents

def add(round):
    """Saves new round to RethinkDB.

    Args:
        round (object): the dictionary representing a single round

    Returns:
        bool: result True if successful, False otherwise.
    """

    if config.log: print('listening...')


    # Setup database variables
    db_name = 'aroundlb'
    table_name = 'rounds'

    # Connect to RethinkDB
    r.connect('localhost', 28015).repl()

    # Create RethinkDB database if it doesn't exist
    if db_name not in r.db_list().run():
        if config.log: print('database {} does not exist'.format(db_name))
        r.db_create(db_name).run()

    # Create RethinkDB table if it doesn't exist
    if table_name not in r.db(db_name).table_list().run():
        if config.log: print('table {} does not exist'.format(table_name))
        r.db(db_name).table_create(table_name).run()
        r.db(db_name).table(table_name).index_create('timestamp').run()
        r.db(db_name).table(table_name).index_create('channel_name').run()

    # Insert round into table <name>
    if config.log: print('Inserting...')
    response = r.db(db_name).table(table_name).insert(round).run()

    return response