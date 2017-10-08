import xml.etree.ElementTree as ET 
import requests

startcity = input("Enter the origin city ")
endcity = input("Enter the end city ")
# Use a request on the url. TODO: Find a way to change the url to use specific cities
response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/xml?units=imperial&origins='+startcity+'&destinations='+endcity)
# Save the XML to an ET
tree = ET.fromstring(response.content)
# Navigate through the tree using indices
hours = tree[3][0][1][1].text

miles = tree[3][0][2][1].text

print(hours, miles)
