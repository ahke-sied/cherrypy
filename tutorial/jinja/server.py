import os, os.path
import cherrypy
import jinja2

ROOT_DIR = os.path.abspath(os.getcwd())
# In this case, we will load templates off the filesystem.
# This means we must construct a FileSystemLoader object.
# 
# The search path can be used to make finding templates by
#   relative paths much easier.  In this case, we are using
#   absolute paths and thus set it to the filesystem root.
templateLoader = jinja2.FileSystemLoader( searchpath=ROOT_DIR )

# An environment provides the data necessary to read and
#   parse our templates.  We pass in the loader object here.
templateEnv = jinja2.Environment( loader=templateLoader )

# This constant string specifies the template file we will use.
TEMPLATE_FILE = "index.html"

# Read the template file using the environment object.
# This also constructs our Template object.
template = templateEnv.get_template( TEMPLATE_FILE )

# Specify any input variables to the template as a dictionary.
templateVars = { "my_string" : "Test Example",
                 "my_list" : [0,1,2,3,5,4,5] }

# Finally, process the template to produce our final text.
outputText = template.render( templateVars )

class HelloWorld(object):
	@cherrypy.expose
	def index(self):
		return outputText

if __name__ == '__main__':
	cherrypy.quickstart(HelloWorld())
