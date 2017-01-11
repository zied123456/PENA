#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json
import argparse
import socket

from tinydb import TinyDB
from flask import Flask, request, redirect

from .pena import Pena

app = Flask(__name__, static_url_path='')

@app.route('/api/v1/pena/ask', methods=['POST'])
def ask_pena():
    decision, data = pena.process(
        request.json, 'ASK', request.args.get('limit'))

    return json.dumps({'decision': decision, 'data': data})


@app.route('/api/v1/pena/tell', methods=['POST'])
def tell_pena():
    decision, data = pena.process(request.json, 'TELL')

    return json.dumps({'decision': decision, 'data': data})

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/play')
def redirect_play():
    return redirect('/#!/play')

@app.route('/about')
def redirect_about():
    return redirect('/#!/about')

def main():
    global pena

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="PENA's an Entirely New Akinator")

    parser.add_argument('questions_file', type=str,
        help="A JSON file containing a list of questions.")
    parser.add_argument('database_file', type=str,
        help="A file to store characters PENA already knows about.")
    parser.add_argument('ip_address', type=str,
        help="The IP address to listen to for incoming requests.")
    parser.add_argument('port', type=int,
        help="The port to bind the listener to.")

    args = parser.parse_args()

    # Load questions file
    try:
        with open(str(args.questions_file)) as questions_file:
            questions = json.load(questions_file)
    except ValueError:
        questions = []

    # Load database file
    database = TinyDB(str(args.database_file))

    # Create new Pena engine
    try:
        pena = Pena(questions, database)
    except TypeError:
        print "Can't initiate engine"
        sys.exit(1)

    # Validate IP address
    try:
        socket.inet_aton(args.ip_address)
        host = args.ip_address
    except socket.error:
        host = '127.0.0.1'

    # Validate port number
    if isinstance(args.port, int):
        port = args.port
    else:
        port = 5000

    app.run(host=host, port=port)
