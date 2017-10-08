from urllib.parse import urlencode
import requests
import webbrowser
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


from flask import Flask
from flask_ask import Ask, statement, question


app = Flask(__name__)
ask = Ask(app, '/')

inputList = []

# launch message
# global list is reset in case of persistence between sessions
@ask.launch
def launch():
	inputList.clear()
	return question("<speak> <s> Welcome to US Road Trip Planner.</s> <s>Please say your starting city</s> </speak>")

# handles user input for the city they are departing from
# appends the input to the list
@ask.intent("OriginCity")
def originCity(Cities):
	inputList.clear()
	inputList.append(Cities)
	return question("<speak> <s>Please say your starting state</s> </speak>")

# handles user input for the state they are departing from
# adds input to the list
@ask.intent("OriginState")
def originState(States):
	# dictionary mapping state names to abbreviation 
	# for use when parsing GasBuddy.com
	us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
	}
	inputList.append(us_state_abbrev[States])
	return question("<speak> <s>Please say your ending city</s> </speak>")

# handles user input for their destination
# saves it to the list
@ask.intent("DestinationCity")
def destinationCity(Cities):
	inputList.append(Cities)
	return question("<speak> <s>Lastly, please say the fuel efficiency of your car</s> </speak>")

# handles user input for their vehicle's fuel efficiency
@ask.intent("FuelEfficiency")
def fuelEfficiency(mpg):
	inputList.append(mpg)
	return constructURL()


# queries google maps api for travel time and distance
# calls functions to parse the xml response and parse
# the html for average state gas prices
def constructURL():
	gmapsUrl = 'https://maps.googleapis.com/maps/api/distancematrix/xml?'
	
	originLocation = inputList[0]
	destLocation = inputList[2]
	
	mydict = {'units' : 'imperial', 'origins' : originLocation, 'destinations' : destLocation}
	url = gmapsUrl + urlencode(mydict)
	hours, miles = XML(url)
	if hours is None or miles is None:
		return statement("Invalid Location")
	
	miles = int(round(miles))
	gasAvg = gasParse()
	mpg = float(inputList[3]) 
	price = int(round(gasAvg * miles * (1.0/float(mpg))))
	inputList.clear()
	return statement("<speak> <s>It will take {}".format(hours) + " to travel {}".format(miles) + " miles</s>" +
		" <s>The total cost of gas for the trip is approximately {}".format(price) +" dollars</s> </speak>")

# requests html from gasbuddy to fetch average state gas prices
def gasParse():
	# requests the url page to find average gas prices per state
	gasPage = requests.get("https://www.gasbuddy.com/USA")
	
	# turns the page content into a beautiful soup object
	gasSoup = BeautifulSoup(gasPage.content, 'html.parser')

	# stores user input for the state name
	gasState = inputList[1]

	# parses the html to find the information for that particular state
	gasText = gasSoup.find(id=gasState)
	
	# Finds html tags with the listed class and attributes which finds listed gas price
	table = gasText.find_all(class_='col-sm-2 col-xs-3 text-right')

	# Traverse through the set created by table and prints the text within the tags, which is just the 
	# average gas price
	for tag in table:
		gas = float(tag.text.strip())
	return gas

# parses XML output from google maps api
def XML(url):
	# posts an http request to the google maps api formatted url
	response = requests.get(url)
	
	# creates an element tree from the xml response
	tree = ET.fromstring(response.content)
	
	# Navigate through the tree using indices
	if tree[3][0][0].text == 'ZERO_RESULTS':
		hours = None
		miles = None
	else:
		hours = tree[3][0][1][1].text
		miles = tree[3][0][2][1].text
		
		# converts miles to a float from a string and removes commas 
		str1, str2 = miles.split()
		if "," in str1:  
			temp1, temp2 = str1.split(",")
			trans = temp1 + temp2
			miles = float(trans)	
			#return hours, trans
		else:
			miles = float(str1)

	
	return hours, miles

if __name__ == '__main__':
	main()
