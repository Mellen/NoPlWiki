#! /usr/bin/env python
import cherrypy
from classes.book import book
from mako.template import Template
import markdown
import os
import shutil

current_dir = os.path.dirname(os.path.abspath(__file__))
books_dir = os.path.join(current_dir, 'books')
if not os.path.isdir(os.path.join(current_dir, 'books')):
    os.mkdir(os.path.join(current_dir, 'books'))

class Server(object):
    def __init__(self):
        self.book = book(current_dir)

    exposed = True

    @cherrypy.expose
    def index(self):
        template = Template(filename=os.path.join(current_dir,'templates/index.html'))
        return template.render(book_list=os.listdir(books_dir))

    @cherrypy.expose
    def deleteBook(self, bookTitle):
        currentBooks = os.listdir(books_dir)
        if bookTitle in currentBooks:
            shutil.rmtree(os.path.join(books_dir, bookTitle))
        template = Template(filename=os.path.join(current_dir,'templates/booklist.html'))
        return template.render(book_list=os.listdir(books_dir))

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
        },
    '/css':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_dir, 'css'),
        },
    '/img':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_dir, 'img'),
        }
}



cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(Server(), '/', conf)
