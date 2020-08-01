from splinter import Browser
from flask import jsonify
from bs4 import BeautifulSoup as bs
import pandas as pd 
import time

def initBrowser(): 
	executable_path = {'executable_path': 'chromedriver.exe'}
	browser = Browser('chrome', **executable_path, headless=False)

	return browser

def scrapeMars():
	browser = initBrowser()


	# Scrape Mars news article
	url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
	browser.visit(url)
	time.sleep(1)
	

	html = browser.html
	soup = bs(html, "html.parser")
	latestArticle = soup.find("ul", class_="item_list")

	title = latestArticle.find("div", class_="content_title")
	paragraphText = latestArticle.find("div", class_="article_teaser_body").text

	#scrap Featured image
	url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(url)

	time.sleep(1)

	fullImage = browser.find_by_id("full_image")
	fullImage.click()
	moreInfo = browser.links.find_by_partial_text('more info')
	moreInfo.click()

	html = browser.html
	soup = bs(html, 'lxml')

	imgTag = soup.find("figure", class_="lede").a["href"]
	featuredImgUrl = f"https://www.jpl.nasa.gov{imgTag}"

	# Scrape Twitter
	url = "https://twitter.com/marswxreport?lang=en"
	browser.visit(url)


	#Scrap Mars Facts
	url = "https://space-facts.com/mars/"
	tables = pd.read_html(url)

	statsTable = tables[0]
	statsTable.columns = (["Description", "Value"])
	#statsTable.set_index("Description", inplace=True)
	marsTable = statsTable.values.tolist()
	print(marsTable)

	#Scrap USGS Astrogeology
	url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(url)

	time.sleep(1)

	links = browser.find_by_css("a.product-item h3")

	imgList = []

	for link in range(len(links)):
	    imgDict = {}
	    
	    browser.find_by_css('a.product-item h3')[link].click()
	    
	    title = browser.find_by_css("h2.title").text
	    imgDict["title"] = title
	    
	   
	    imgUrl = browser.find_link_by_text("Sample")
	    imgDict["img_url"] = imgUrl["href"]

	    imgList.append(imgDict)
	    browser.back()

	marsData = {"title": title, 
				"paragraph": paragraphText, 
				"featuredImgUrl": featuredImgUrl,
				"statsTable": marsTable,
				"imgList" : imgList
				}

	print(marsData)
	browser.quit()
	return marsData