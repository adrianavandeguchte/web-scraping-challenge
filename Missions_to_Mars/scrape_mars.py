from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    
    # gets recent news title and paragraph snippet
    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"
    # sets browser to visit the url and then wait to ensure all of the page loads
    browser.visit(url)
    time.sleep(5)
    # builds soup object for data scraping
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # this can break from blackmagic, ask gretel
    # pulls the first index in list_text as variable recent
    recent = soup.find_all("div", class_="list_text")[0]
    # finds the title and paragraph text within recent
    news_title = recent.find("div",class_="content_title").text
    news_p = recent.find("div",class_="article_teaser_body").text
    
    # gets mars featured image
    # reassign url variable to next site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # sets browser to visit the url and then wait to ensure all of the page loads
    browser.visit(url)
    time.sleep(5)
    # builds soup object for data scraping
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # locates .jpg link from feature image 
    fancy_href = soup.find_all("a", class_="button fancybox")[0].get("data-fancybox-href")
    # completes link url
    featured_image_url = 'https://www.jpl.nasa.gov' + fancy_href
    
    # gets the most recent mars weather report from twitter
    # reassign url variable to next site
    url = "https://twitter.com/marswxreport?lang=en"
    # sets browser to visit the url and then wait to ensure all of the page loads
    # this sleep step is longer to account for twitter restrictions
    browser.visit(url)
    time.sleep(30)
    # builds soup object for data scraping
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # pulls all possible tweets
    tweets = soup.find_all("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    # sets up empty weather update tweet list
    update_tweets = []
    # filters possible tweets to just those that include marker signifying an update
    for tweet in tweets:
        if "InSight sol" in tweet.text:
            update_tweets.append(tweet.text)
    # assigns latest update to new variable
    mars_weather = update_tweets[0]
    
    # gets a mars facts table
    # reassign url variable to next site
    url = "https://space-facts.com/mars/"
    # sets browser to visit the url and then wait to ensure all of the page loads
    browser.visit(url)
    time.sleep(5)
    # builds soup object for data scraping
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find_all("table", class_="tablepress tablepress-id-p-mars")
    mars_df = pd.read_html(str(table))[0]
    mars_df = mars_df.set_index(0)
    mars_df = mars_df.rename(columns={1:"value"})
    mars_df = mars_df.rename_axis(None)
    mars_table = mars_df.to_html()
    
    # gets high quality images of the four hemispheres of mars
    # reassign url variable to next site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # sets browser to visit the url and then wait to ensure all of the page loads
    browser.visit(url)
    time.sleep(5)
    # builds soup object for data scraping
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # pulls urls for enhanced hemisphere images
    results = soup.find_all("a", class_="itemLink product-item")
    for result in results:
        if result.text == 'Cerberus Hemisphere Enhanced':
            cerb_url = 'https://astrogeology.usgs.gov' + result.get("href")
        if result.text == 'Schiaparelli Hemisphere Enhanced':
            schia_url = 'https://astrogeology.usgs.gov' + result.get("href")
        if result.text == 'Syrtis Major Hemisphere Enhanced':
            syrtm_url = 'https://astrogeology.usgs.gov' + result.get("href")
        if result.text == 'Valles Marineris Hemisphere Enhanced':
            vallm_url = 'https://astrogeology.usgs.gov' + result.get("href")
    # sets browser to visit the url and then wait to ensure all of the page loads
    browser.visit(cerb_url)
    time.sleep(5)

    # builds soup object for data scraping
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # collects url of full size image
    results = soup.find_all("a")
    for result in results:
        if result.text == 'Sample':
            cerb_url = result.get("href")
    # sets browser to visit the url and then wait to ensure all of the page loads
    browser.visit(schia_url)
    time.sleep(5)

    # builds soup object for data scraping
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # collects url of full size image
    results = soup.find_all("a")
    for result in results:
        if result.text == 'Sample':
            schia_url = result.get("href")
    # sets browser to visit the url and then wait to ensure all of the page loads
    browser.visit(syrtm_url)
    time.sleep(5)

    # builds soup object for data scraping
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # collects url of full size image
    results = soup.find_all("a")
    for result in results:
        if result.text == 'Sample':
            syrtm_url = result.get("href")
    # sets browser to visit the url and then wait to ensure all of the page loads
    browser.visit(vallm_url)
    time.sleep(5)

    # builds soup object for data scraping
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # collects url of full size image
    results = soup.find_all("a")
    for result in results:
        if result.text == 'Sample':
            vallm_url = result.get("href")
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": vallm_url},
        {"title": "Cerberus Hemisphere", "img_url": cerb_url},
        {"title": "Schiaparelli Hemisphere", "img_url": schia_url},
        {"title": "Syrtis Major Hemisphere", "img_url": syrtm_url},
    ]   
            
    # stores all data in a dictionary
    mars_data = {
        "news_title":news_title,
        "news_p":news_p,
        "featured":featured_image_url,
        "weather":mars_weather,
        "table":mars_table,
        "hemispheres":hemisphere_image_urls
    }

    return mars_data