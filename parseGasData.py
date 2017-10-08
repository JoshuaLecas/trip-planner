# parse gas data

from urllib.parse import urlencode
import requests
from configparser import ConfigParser
import webbrowser

import XMLParsing as parseXML

def main():
	constructURL()

# constructs URL
def constructURL():
	#config = ConfigParser()
	#config.read('config.ini')
	#key = config.get('section1', 'API_KEY')
	#print(key)

	gmapsUrl = 'https://maps.googleapis.com/maps/api/distancematrix/xml?'
	
	originLocation = print('Enter name of Origin City': )
	destLocation = print('Enter name of Destination City:' )
	
	mydict = {'units' : 'imperial', 'origins' : originLocation, 'destinations' : destLocation}
	url = gmapsUrl + urlencode(mydict)
	hours, miles = parseXML.XML(url)
	#r = requests.get(url)
	
	#print(r)
	#print(url)
	print(hours, miles)

if __name__ == '__main__':
		main()
