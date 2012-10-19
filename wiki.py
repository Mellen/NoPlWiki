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
        self.book = book(self.connection, current_dir)

    exposed = True

    @cherrypy.expose
    def index(self):
        template = Template(filename=os.path.join(current_dir,'templates/index.html'))
        books = self.connection.books
        return template.render(book_list=books.collection_names())

    @cherrypy.expose
    def deleteBook(self, bookTitle):
        books = self.connection.books
        books.drop_collection(bookTitle)
        template = Template(filename=os.path.join(current_dir,'templates/booklist.html'))
        return template.render(book_list=books.collection_names())

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
