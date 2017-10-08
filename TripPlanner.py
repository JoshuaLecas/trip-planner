# parse gas data

import urllib
import requests
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
	
	originLocation = raw_input('Enter name of Origin City: ' )
	destLocation = raw_input('Enter name of Destination City: ' )
	
	mydict = {'units' : 'imperial', 'origins' : originLocation, 'destinations' : destLocation}
	url = gmapsUrl + urllib.urlencode(mydict)
	hours, miles = parseXML.XML(url)
	if hours is None or miles is None:
		print "Unable to find a route."
		return
	#r = requests.get(url)
	
	#print(r)
	#print(url)
	print hours, miles
	gasAvg = fectchinGas.gasParse()
	mpg = raw_input('What is the gas mileage of your car?: ')  
	price = gasAvg * miles * (1.0/float(mpg))
	print "%.2f" % price

if __name__ == '__main__':
		main()
