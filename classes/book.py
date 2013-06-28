import cherrypy
from mako.template import Template
import markdown
import os
import codecs
from gitInterface import gitInterface

class book(object):
    def __init__(self, root_path):
        self.root_path = root_path
        self.git = gitInterface()

    exposed = True

    def GET(self, title=None, page_name='main_page'):
        if cherrypy.request.path_info.count('/') != 3:
            raise cherrypy.HTTPRedirect('/book/{0}/{1}'.format(title, page_name))
        pageData = None

        if os.path.exists(os.path.join(self.root_path, 'books', title, page_name)):
            with codecs.open(os.path.join(self.root_path, 'books', title, page_name), mode='r', encoding='utf-8') as f: 
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
            cherrypy.log('making dirs')
            os.makedirs(curDir)
            cherrypy.log('git init')
            self.git.init(curDir)
            cherrypy.log('git init done.')

        os.chdir(curDir)

        with codecs.open(page_name, mode='w', encoding='utf-8') as f:
            f.write('')

        self.git.add(page_name)
        self.git.commit(page_name, 'inital commit for '+page_name)

        os.chdir(self.root_path)

        return data

    def buildContents(self, title):
        contents = os.listdir(os.path.join(self.root_path, 'books', title))
        pages = [item for item in contents if item != 'main_page' and not os.path.isdir(item)]
        return pages

    def POST(self, title, page_name='main_page', page_body_text=None, change_message=None):
        curDir = os.path.join(self.root_path, 'books', title)
        os.chdir(curDir)
        if change_message is None:
            change_message = 'made a change to '+page_name
        with codecs.open(page_name, mode='w', encoding='utf-8') as f:
            f.write(page_body_text)
        self.git.commit(page_name, change_message)
        os.chdir(self.root_path)
        return self.GET(title, page_name)

    def DELETE(self, title=None, page_name=None):
        if page_name != 'main_page':
            curDir = os.path.join(self.root_path, 'books', title)
            os.chdir(curDir)
            self.git.rm(page_name)
            self.git.commit(page_name, 'removed '+page_name)
            os.chdir(self.root_path)
            pages = self.buildContents(title)
            template = Template(filename=os.path.join(self.root_path,'templates/pagelist.html'))
            return template.render(pages=pages, title=title)
        return self.GET(title, 'main_page')
