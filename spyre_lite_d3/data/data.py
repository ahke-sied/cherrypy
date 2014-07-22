import nbsutils.imp as imp
import nbsutils.sql as sql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import simplejson as json
from time import sleep
import string
import random
import os 

def generateRandomString(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def clearOutTmpDir():
	folder = ROOT_DIR+'/public/images/tmp/'
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception, e:
			print e

def getLittleData(params):
	ex_first = int(params['ex_first'])
	max_incl = int(params['max_incl'])
	upper_limit = ex_first+max_incl
	sqldb = sql.Connection('meta')
	query = """select c.name, count(*) AS count from categories c
			inner join x_artists_categories xac 
			on c.id=xac.category_id
			group by c.name
			order by count(*) desc
			limit {},{};""".format(ex_first, upper_limit)
	mets = sqldb.fetchAll(query,returnType="data.frame")
	return json.loads(mets.to_json(orient='records'));
