import cherrypy
import pymongo
from mako.template import Template
import markdown
import os

class book(object):
    def __init__(self, mongocon, root_path):
        self.connection = mongocon
        self.db = self.connection.books
        self.root_path = root_path

    exposed = True

    def GET(self, title=None, page_name='main_page'):
        if cherrypy.request.path_info.count('/') != 3:
            raise cherrypy.HTTPRedirect('/book/{0}/{1}'.format(title, page_name))
        collection = self.db[title]
        page_data = collection.find_one({'page_name':page_name})
        if page_name == 'main_page':
            template = Template(filename=os.path.join(self.root_path, 'templates/book.html'))
        else:
            template = Template(filename=os.path.join(self.root_path,'templates/page.html'))

        if page_data is None:
            page_data = self.createPage(collection, page_name)
            if page_name == 'main_page':
                page_data['pages'] = []
            page_data['page_body'] = ''
        else:
            if page_name == 'main_page':
                page_data['pages'] = self.buildContents(collection)
            page_data['page_body'] = markdown.markdown(page_data['page_body_raw'])

        page_data['title'] = title
        page_data['page_name'] = page_name

        return template.render(**page_data)

    def createPage(self, collection, page_name='main_page'):
        data = {'page_name': page_name
               ,'page_body_raw': ''}
        collection.insert(data)
        return data

    def buildContents(self, collection):
        contents = collection.find({}, {'_id':0, 'page_name':1})
        pages = [item['page_name'] for item in contents if item['page_name'] != 'main_page']
        return pages

    def POST(self, title=None, page_name='main_page', page_body_text=None):
        collection = self.db[title]
        where = {'page_name':page_name}
        what = {'page_name':page_name, 'page_body_raw':page_body_text}
        collection.update(where, what, False, False)
        return self.GET(title, page_name)

    def DELETE(self, title=None, page_name=None):
        if page_name != 'main_page':
            collection = self.db[title]
            page = {'page_name': page_name}
            collection.remove(page)
            pages = self.buildContents(collection)
            template = Template(filename=os.path.join(self.root_path,'templates/page_list.html'))
            return template.render(pages=pages, title=title)
        return self.GET(title, 'main_page')
