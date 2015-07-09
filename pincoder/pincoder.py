#!/usr/bin/python
# coding: utf8

import json
from urllib2 import Request, urlopen, URLError
from geocoder import google
from keys import datagov_key

api_url = 'https://data.gov.in/api/datastore/resource.json'
#resource_id is predefined in API
resource_id = '6176ee09-3d56-4a3b-8115-21841576b2f6'

def postoffice_all(pincode):
	"""
	Returns list of post office name for specified pincode.
	Yes! One pincode is associated with multiple offices 
	(SO/BO) nearby.
	"""

	request = Request('{0}?resource_id={1}&api-key={2}&filters[pincode]={3}'.format(api_url,resource_id, datagov_key, pincode))
	postofficenames = []

	try:
		response = urlopen(request)
		recieved_data = json.loads(response.read())
		for r in recieved_data['records']:
			postofficenames.append(r['officename'])


	except URLError, e:
		print 'No data. Got an error:', e

	return postofficenames


