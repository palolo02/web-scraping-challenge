# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests
import re
import pymongo

# Open incognito browser tab
def open_browser():
    url_exe = "Missions_to_Mars/chromedriver.exe"
    executable_path = {"executable_path":url_exe }
    return Browser("chrome", **executable_path, headless=False, incognito=True)

def scrape_info():

    # init MongoDB connection
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    # Define database and collection
    db = client.news_web
    collection = db.items

    #### ============================================================================
    # URL to be scraped
    url = 'https://mars.nasa.gov/news'

    # Open browsing
    browser = open_browser()

    # Retrieve page with the requests module
    browser.visit(url)
    # Wait for the page to render
    time.sleep(3)
    # Get response
    response = requests.get(url)

    # Scraping page into Soupas HTML
    html = browser.html
    soup = bs(html, "html.parser")

    # Get latest news from page
    result = soup.find_all('div',class_='list_text')[0]

    # Get title
    news_title = result.find('div', class_='content_title').text
    print(news_title)
    # Get paragraph
    news_paragraph = result.find('div', class_='article_teaser_body').text
    print(news_paragraph)
    # Get date
    news_date = result.find(class_='list_date').text
    print("========================================")

    # Closing the browser after scraping
    browser.quit()


    #### ============================================================================
    # URL to be scraped
    main_url_jpl = "https://www.jpl.nasa.gov/spaceimages/"
    url_jpl_image = f"{main_url_jpl}?search=&category=Mars"
    full_url_jpl = f"{main_url_jpl}images/wallpaper/"

    # Open browsing
    browser = open_browser()

    # Visiting JPL Site
    browser.visit(url_jpl_image)
    time.sleep(3)

    # Scraping page into Soup
    html= browser.html
    soup= bs(html, "html.parser")

    # URL from current featured Image 
    featured_image_info = soup.find('article', class_="carousel_item")['style']

    # Finding the Image Name
    featured_image_name= (featured_image_info.split("wallpaper/")[1]).split(".jpg")[0]

    # Creating the Featured Image URL
    featured_image_url= f"{full_url_jpl}{featured_image_name}.jpg"
    print(featured_image_url)

    # Closing the browser after scraping
    browser.quit()

    #### ============================================================================
    browser = open_browser()

    url_twitter = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_twitter)

    time.sleep(10)

    # Scraping page into Soup
    html= browser.html
    soup= bs(html, "html.parser")

    # Finding the latest Tweet about Mars Weather   
    mars_weather_tweet = soup.find_all('span', text = re.compile(r'(InSight*)'))[0].get_text()
    print(mars_weather_tweet)

    # Closing the browser after scraping
    browser.quit()


    #### ============================================================================
    url_facts ="https://space-facts.com/mars/"

    # Getting the fact table
    tables = pd.read_html(url_facts)
    fact_table = pd.DataFrame(tables[0])

    fact_table = fact_table.rename(columns={
        0 : "Description",
        1 : "Value"
    })

    fact_table.set_index("Description", inplace = True)

    # Creating the html Table
    table_html = fact_table.to_html()
    print(table_html)
    # Cleaning the table
    #table_html= table_html.replace('\n',"")

    #### ============================================================================
    browser = open_browser()
    url_full_img = "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/"
    url_usgs = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_usgs)

    time.sleep(4)

    # Scraping page into Soup
    html= browser.html
    soup= bs(html, "html.parser")

    urls_img = []
    results = soup.find_all("div", class_="item")
    # Finding the URL of each Hemispheres Images
    for result in results:
        title = result.find('h3').get_text().split("Enhanced")[0]
        result = result.find('a')["href"].split("Viking/")[1]
        result = f"{url_full_img}{result}.tif/full.jpg"
        browser.visit(result)
        item_img = {
            'title' : title,
            'img_rul' : result
        }
        
        urls_img.append(item_img)  
        # img validation
        time.sleep(2)

    # Closing the browser after scraping
    browser.quit()

    # Store result as Dictionary into MongoDB

    newItem = {
        'title': news_title,
        'paragraph': news_paragraph,
        'date': news_date,
        'img_rul': featured_image_url,
        'tweet' : mars_weather_tweet,
        'table_data' : table_html,
        'urls_img' : urls_img
    }

    print(newItem)
    # Persist data into MongoDB
    collection.insert_one(newItem)

    return newItem