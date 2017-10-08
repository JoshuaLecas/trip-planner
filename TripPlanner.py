# parse gas data

from urllib.parse import urlencode
import requests
from configparser import ConfigParser
import webbrowser

import XMLParsing as parseXML
import FetchGas as fectchinGas

def main():
	constructURL()

# constructs URL
def constructURL():
	#config = ConfigParser()
	#config.read('config.ini')
	#key = config.get('section1', 'API_KEY')
	#print(key)

	gmapsUrl = 'https://maps.googleapis.com/maps/api/distancematrix/xml?'
	
	originLocation = input('Enter name of Origin City:' )
	destLocation = input('Enter name of Destination City:' )
	
	mydict = {'units' : 'imperial', 'origins' : originLocation, 'destinations' : destLocation}
	url = gmapsUrl + urlencode(mydict)
	hours, miles = parseXML.XML(url)
	if hours is None or miles is None:
		print("Unable to find a route.")
		return
	#r = requests.get(url)
	
	#print(r)
	#print(url)
	print(hours, miles)
	gasAvg = fectchinGas.gasParse()
	#print(gasAvg) 
	price = gasAvg * miles
	print("%.2f"%price)

if __name__ == '__main__':
		main()