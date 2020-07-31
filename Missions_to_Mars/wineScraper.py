from splinter import Browser 
from bs4 import BeautifulSoup 

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url = "https://www.winespectator.com/vintage-charts/region/united-states"
browser.visit(url)

html = browser.html 
soup = BeautifulSoup(html, "html.parser")

wineTypes = soup.find_all("h3", class_="m-0")

wineList = []

for wine in range(len(wineTypes)): 
	wineDict = {}

	
	browser.find_by_css("h3.m-0 a")[wine].click()

	rows = browser.find_by_tag("td[valign=top]")
	
	for row in rows:
		wineType = browser.find_by_css("h1")[1].text
		#wineDict["wine type"]: wineType
		print(wineType)
		print(row.text)
	# for row in range(len(rows)): 
	# 	wineType = browser.find_by_css("h1")[1].text
	# 	wineDict["wine type"]: wineType

	# 	rowData = browser.find_by_tag("td")[row].text
	# 	print(wineType)
	# 	print(rowData)

	
	browser.back()



