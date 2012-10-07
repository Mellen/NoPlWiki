#! /usr/bin/env python
import cherrypy
from pymongo import Connection
from classes.book import book
import os

class Server(object):
    def __init__(self):
        self.connection = Connection()
        self.book = book(self.connection)

    exposed = True

    @cherrypy.expose
    def index(self):
        html = ''
        with open(r'static_pages/index.html', 'r') as f:
            for line in f:
                html += line
        return html    

current_dir = os.path.dirname(os.path.abspath(__file__))

conf = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
        },
    '/book': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        },
    '/js':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_dir, 'js'),
        }
}

cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(Server(), '/', conf)
