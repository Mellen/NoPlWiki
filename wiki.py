#! /usr/bin/env python
import cherrypy
from pymongo import Connection
from classes.book import book

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

conf = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
    },
    '/book': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    }
}

cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(Server(), '/', conf)
