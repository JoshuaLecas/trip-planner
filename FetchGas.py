import requests
from bs4 import BeautifulSoup
import re

# main calls parsing function
def main():
	print("Getting gas info...")
	gasParse()
# parses gas website
def gasParse():
	# requests the url page
	gasPage = requests.get("https://www.gasbuddy.com/USA")
	
	# turns the page content into a beautiful soup object
	gasSoup = BeautifulSoup(gasPage.content, 'html.parser')

	# stores user input for the state name
	gasState = raw_input("Enter Shortened State Name: ")

	# parses the html to find the information for that particular state
	gasText = gasSoup.find(id=gasState)

	# print(gasText)
	
	# Finds html tags with the listed class, which is the class that contains the average gas price
	table = gasText.find_all(class_='col-sm-2 col-xs-3 text-right')
	
	# print(table)

	# Traverse thru the set created by table and prints the text within the tags, which is just the 
	# average gas price
	for tag in table:
		gas = float(tag.text.strip())
	return gas

if __name__ == '__main__':
	main()
