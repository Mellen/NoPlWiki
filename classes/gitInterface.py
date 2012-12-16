import os

class gitInterface(object):
    
    def init(self, directory):
        os.popen('git init '+directory)

    def add(self,filename):
        os.popen('git add '+filename)

    def commit(self, filename, message):
        os.popen('git commit %s -m "%s"'%(filename, message))

    def rm(self, filename):
        os.popen('git rm '+filename)
