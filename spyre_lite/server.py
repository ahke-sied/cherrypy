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
		templateVars = { "controls" : [
						{"output_type" : "image",
							"button_label" : "Generate Sine Wave",
							"button_id" : "submit-plot",
							"text_fields" : [
									{"label": 'Amplitude', "value": 3, "variable_name": 'amp_val_1', "input_type":'text'},
									{"label": 'Frequency', "value": 5, "variable_name": 'freq_val_1', "input_type":'text'},
									{"label": 'Decay Constant', "value": 1, "variable_name": 'decay_val_1', "input_type":'text'},
									{"label": 'Number of Cycles', "value": 2, "variable_name": 'n_cycle', "input_type":'text'},
							]
						},
# 						{"output_type" : "table",
# 							"button_label" : "Load THE Table",
# 							"button_id" : "load-table",
# 							"text_fields" : []
# 						}
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
			data = getLittleData()
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
