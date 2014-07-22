import os, os.path

import cherrypy

class Index(object):
	@cherrypy.expose
	def index(self):
		return file('index.html')


if __name__=='__main__':
	conf = {
		'/': {
			'tools.sessions.on':True,
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/static': {
			'tools.staticdir.on':True,
			'tools.staticdir.dir':'./public'
		}
	}
	webapp = Index()
	cherrypy.quickstart(webapp, '/', conf)