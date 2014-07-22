import os, os.path
import random
import string
import simplejson

import cherrypy

class Index(object):
	@cherrypy.expose
	def index(self):
		return file('index.html')

class GetName(object):
	exposed = True

	@cherrypy.tools.accept(media='text/plain')
	def POST(self, name="adam"):
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return simplejson.dumps({'greeting':"Hello, %s" % name})

class GetData(object):
	exposed = True

	@cherrypy.tools.accept(media='text/plain')
	def POST(self, length=2):
		n = int(length)
		v = [1,1]
		while len(v)<n:
			v.append(v[-1]+v[-2])
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return simplejson.dumps({'values':v})

if __name__=='__main__':
	conf = {
		'/': {
			'tools.sessions.on':True,
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
			'/data': {
			'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
			'tools.response_headers.on':True,
			'tools.response_headers.headers': [('Content-Type', 'text/plain')],
		},
			'/name': {
			'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
			'tools.response_headers.on':True,
			'tools.response_headers.headers': [('Content-Type', 'text/plain')],
		},
		'/static': {
			'tools.staticdir.on':True,
			'tools.staticdir.dir':'./public'
		}
	}
	webapp = Index()
	webapp.data = GetData()
	webapp.name = GetName()
	cherrypy.quickstart(webapp, '/', conf)
