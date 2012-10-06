import cherrypy
import pymongo
from mako.template import Template
import markdown

class book(object):
    def __init__(self, mongocon):
        self.connection = mongocon
        self.db = self.connection.books

    exposed = True

    def GET(self, title=None, page_name='main_page'):
        self.collection = self.db[title]
        page_data = self.collection.find_one('{\'page_name\':\''+page_name+'\', \'title\':\''+title+'\'}')
        if page_name == 'main_page':
            template = Template(filename='templates/book.html')
        else:
            template = Template(filename='templates/page.html')

        if page_data is None:
            if page_name == 'main_page':
                data = self.createBook(title)
                data['contents'] = ''
                data['page_body'] = ''
            else:
                data = self.createPage(title, page_name)
                data['page_body'] = ''
        else:
            if page_name == 'main_page':
                data['contents'] = ''
            data['page_body'] = markdown.markdown(data['page_body_raw'])
        return template.render(**data)

    def createBook(self, title):
        data = {'title': title
               ,'page_name': 'main_page'
               ,'page_body_raw': ''}
        self.collection.insert(data)
        return data

    def POST(self, title=None, page_name='main_page', page_body_text=None):
        self.collection = self.db[title]
        return self.GET(title)
