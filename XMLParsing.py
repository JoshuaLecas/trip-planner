import xml.etree.ElementTree as ET 
import requests
import re

def XML(url):
	# Use a request on the url. TODO: Find a way to change the url to use specific cities
	response = requests.get(url)
	# Save the XML to an ET
	tree = ET.fromstring(response.content)
	# Navigate through the tree using indices
	hours = tree[3][0][1][1].text

	miles = tree[3][0][2][1].text

	num = re.findall('\d+\.\d+', miles)
	print(float(num[0]))

	return hours, miles
