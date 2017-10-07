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
	gasState = input("Enter Shortened State Name: ")

	# parses the html to find the information for that particular state
	gasText = gasSoup.find_all(id=gasState)

	print(gasText)
	# TODO: Search through gasText to find the price, and save it using regular expressions



if __name__ == '__main__':
	main()