import os, os.path
import random
import string
import simplejson

execfile('data/data.py') 

import cherrypy

class Index(object):
	@cherrypy.expose
	def index(self):
		return file('index.html')

class GetData(object):
	exposed = True

	@cherrypy.tools.accept(media='text/plain')
	def POST(self, arg1=18197, arg2=11, arg3=0):
		if arg3=='tst':
			data = getLittleData()
		else:
			data = getData(arg1, arg2)
		
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return simplejson.dumps({'data':data,'arg3':arg3})

class GetPlot2(object):
	exposed = True

	@cherrypy.tools.accept(media='text/plain')
	def POST(self, arg1=1, arg2=1):
		img_path = getPlot(float(arg1), float(arg2))
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return simplejson.dumps({'img_path':img_path})

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
			'/plot2': {
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
	webapp.plot2 = GetPlot2()
	cherrypy.quickstart(webapp, '/', conf)
