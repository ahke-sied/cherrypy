import os, os.path
import random
import string
import simplejson
import jinja2

ROOT_DIR = os.path.abspath(os.getcwd())

templateLoader = jinja2.FileSystemLoader( searchpath=ROOT_DIR )
templateEnv = jinja2.Environment( loader=templateLoader )

execfile('data/data.py') 

import cherrypy

class Root(object):

	@cherrypy.expose
	def index(self):
		templateVars = {"shared_fields" : [
									{"label": 'Exclude First', "value": 0, "variable_name": 'ex_first', "input_type":'text'},
									{"label": 'Max Return', "value": 15, "variable_name": 'max_incl', "input_type":'text'},
							],
						"controls" : [
						{"output_type" : "image",
							"button_label" : "Make Bar Plot",
							"button_id" : "submit-plot",
							"text_fields" : []
						},
						{"output_type" : "table",
							"button_label" : "Load Table",
							"button_id" : "load-table",
							"text_fields" : []
						}
						]
					}
		template = templateEnv.get_template( "index.html" )
		return template.render( templateVars )

	def plot(self, *args, **kw):
		img_path = getPlot(kw)
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return simplejson.dumps({'img_path':img_path})
	plot.exposed = True

	def data(self, env=None, *args, **kw):
		if env=='tst':
			data = getLittleData(kw)
		else:
			data = getData(kw)
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return simplejson.dumps({'data':data,'kw':kw})
	data.exposed = True


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
	webapp = Root()
	cherrypy.quickstart(webapp, '/', conf)
