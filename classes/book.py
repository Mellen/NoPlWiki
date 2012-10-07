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
        collection = self.db[title]
        page_data = collection.find_one({'page_name':page_name})
        if page_name == 'main_page':
            template = Template(filename='templates/book.html')
        else:
            template = Template(filename='templates/page.html')

        if page_data is None:
            if page_name == 'main_page':
                page_data = self.createPage(collection)
                page_data['contents'] = ''
            else:
                page_data = self.createPage(collection, page_name)
            page_data['page_body'] = ''
        else:
            if page_name == 'main_page':
                page_data['contents'] = self.buildContents(collection, title)
            page_data['page_body'] = markdown.markdown(page_data['page_body_raw'])

        page_data['title'] = title
        page_data['page_name'] = page_name

        return template.render(**page_data)

    def createPage(self, collection, page_name='main_page'):
        data = {'page_name': page_name
               ,'page_body_raw': ''}
        collection.insert(data)
        return data

    def buildContents(self, collection, title):
        contents = collection.find({}, {'_id':0, 'page_name':1})
        contents_md = ''
        extra = ''
        if 'title' in cherrypy.request.params:
            extra = 'book/'+title+'/'
        for item in contents:
            if item['page_name'] != 'main_page':
                contents_md += ' - [{0}]({1}{0})\n'.format(item['page_name'], extra)
        return markdown.markdown(contents_md)

    def POST(self, title=None, page_name='main_page', page_body_text=None):
        collection = self.db[title]
        where = {'page_name':page_name}
        what = {'page_name':page_name, 'page_body_raw':page_body_text}
        collection.update(where, what, False, False)
        return self.GET(title, page_name)
