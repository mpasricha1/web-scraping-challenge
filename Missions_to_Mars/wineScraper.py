from splinter import Browser 
from bs4 import BeautifulSoup 
import pandas as pd
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url = "https://www.winespectator.com/vintage-charts/region/united-states"
browser.visit(url)

html = browser.html 
soup = BeautifulSoup(html, "html.parser")

wineTypes = soup.find_all("h3", class_="m-0")

wineList = []

for wine in range(len(wineTypes)): 
	
	browser.find_by_css("h3.m-0 a")[wine].click()

	# rows = browser.find_by_css("td[valign=top]")
	rows = browser.find_by_css("tr")

	wineDict = {}
	for row in range(len(rows)):
		

		wineType = browser.find_by_css("h1")[1].text
		rowHeader  = browser.find_by_tag("h5")[row].text
		rowData = browser.find_by_css("td[valign=top]")[row].text

		wineDict["type"] = wineType 
		wineDict[f"{rowHeader}"] = rowData
		wineList.append(wineDict)

		print(wineDict)

	
	browser.back()

wine_df = pd.DataFrame(wineList)
wine_df.to_csv("Data.csv")
print(wine_df)



