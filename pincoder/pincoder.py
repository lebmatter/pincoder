#!/usr/bin/python
# coding: utf8

import json
from urllib2 import Request, urlopen, URLError
from geocoder import google
from keys import datagov_key

api_url = 'https://data.gov.in/api/datastore/resource.json'
#resource_id is predefined in API
resource_id = '6176ee09-3d56-4a3b-8115-21841576b2f6'

def postoffice_names(pincode):
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


def postoffice_location(pincode):
	"""
	Returns list of latitude and longitude of Post Office.
	If there are more than post offices then S.O. name will be returned.
	Uses geocoder google api by default.
	"""

	request = Request('{0}?resource_id={1}&api-key={2}&filters[pincode]={3}'.format(api_url,resource_id, datagov_key, pincode))
	
	#We need PO name, district name, state name to get correct geolocation.
	#ALso need to strip trailing B.O/S.O
	po_address = []
	po_location  = []

	try:
		response = urlopen(request)
		recieved_data = json.loads(response.read())
		# print recieved_data

		if len(recieved_data['records']) > 1:
			# print recieved_data['records']
			for r in recieved_data['records']:
				if r['officeType'] == 'S.O':
					po_address.append(r['officename'])
					po_address.append(r['Districtname'])
					po_address.append(r['statename'])
		else:
			po_address.append(recieved_data['records'][0]['officename'])
			po_address.append(recieved_data['records'][0]['Districtname'])
			po_address.append(recieved_data['records'][0]['statename'])


		#Trim trailing B.O/S.O
		if po_address[0][-4:] == ' B.O' or ' S.O':
			po_address[0] = po_address[0][:-4]
		# print po_address

		po_location = google(po_address[0]+','+po_address[1]+','+po_address[2])
		# po_location = google(po_address[0]+' '+pincode)
		# po_location


	except URLError, e:
		print 'No data. Got an error:', e

	return po_location.latlng


def demo():
	print postoffice_location('682025')

demo()