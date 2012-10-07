#! /usr/bin/env python
import cherrypy
from pymongo import Connection
from classes.book import book
from mako.template import Template
import markdown
import os

class Server(object):
    def __init__(self):
        self.connection = Connection()
        self.book = book(self.connection)

    exposed = True

    @cherrypy.expose
    def index(self):
        template = Template(filename='templates/index.html')
        books = self.connection.books
        books_md = ''
        for book in books.collection_names():
            if book == 'system.indexes':
                continue
            books_md += ' - [{0}](book/{0})\n'.format(book)
        return template.render(book_list=markdown.markdown(books_md))

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
