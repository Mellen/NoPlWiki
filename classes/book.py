import cherrypy
from mako.template import Template
import markdown
import os
from git import Repo

class book(object):
    def __init__(self, root_path):
        self.root_path = root_path

    exposed = True

    def GET(self, title=None, page_name='main_page'):
        if cherrypy.request.path_info.count('/') != 3:
            raise cherrypy.HTTPRedirect('/book/{0}/{1}'.format(title, page_name))
        pageData = None

        if os.path.exists(os.path.join(self.root_path, 'books', title, page_name)):
            with open(os.path.join(self.root_path, 'books', title, page_name), 'r') as f: 
                pageData = {}
                pageData['page_name'] = page_name
                pageData['page_body_raw'] = f.read()

        if page_name == 'main_page':
            template = Template(filename=os.path.join(self.root_path, 'templates/book.html'))
        else:
            template = Template(filename=os.path.join(self.root_path,'templates/page.html'))

        if pageData is None:
            pageData = self.createPage(title, page_name)
            if page_name == 'main_page':
                pageData['pages'] = []
            pageData['page_body'] = ''
        else:
            if page_name == 'main_page':
                pageData['pages'] = self.buildContents(title)
            pageData['page_body'] = markdown.markdown(pageData['page_body_raw'])

        pageData['title'] = title
        pageData['page_name'] = page_name

        return template.render(**pageData)

    def createPage(self, title, page_name='main_page'):
        data = {'page_name': page_name
               ,'page_body_raw': ''}
        curDir = os.path.join(self.root_path, 'books', title)

        if not os.path.exists(curDir):
            os.makedirs(os.path.join(curDir, '.git'))
            r = Repo(curDir)
            r.git.init()
        else:
            r = Repo(curDir)
        #     r = Repo.init(os.path.join(curDir, '.git'), bare=True)
        # else:
        #     r = Repo(curDir)

        with open(os.path.join(curDir, page_name), 'w') as f:
            f.write('')

        r.git.add('.')
        r.git.commit('-m inital commit for '+page_name)

        return data

    def buildContents(self, title):
        contents = os.listdir(os.path.join(self.root_path, 'books', title))
        pages = [item['page_name'] for item in contents if item != 'main_page']
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
