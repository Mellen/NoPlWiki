import os
import cherrypy

class gitInterface(object):
    
    def init(self, directory):
        os.popen('git init '+escape(directory))

    def add(self,filename):
        os.popen('git add '+escape(filename))

    def commit(self, filename, message):
        os.popen('git commit %s -m "%s"'%(escape(filename), message))

    def rm(self, filename):
        filename = escape(filename)
        cherrypy.log(filename)
        os.popen('git rm '+filename)

def escape(filename):
    return '\''+filename.replace('\'', '\\\'')+'\''#.replace(' ', '\\ ').replace('"','\\"')+'\'' 
