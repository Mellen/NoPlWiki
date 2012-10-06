import cherrypy
import pymongo

class book(object):
    def __init__(self, mongocon):
        self.connection = mongocon
        self.db = self.connection.books

    exposed = True

    def GET(self, title):
        self.collection = self.db[title]
        return title

    def POST(self, title, page_body_text):
        self.collection = self.db[title]
        return self.GET(title)
