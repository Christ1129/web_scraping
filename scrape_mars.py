# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt

from webdriver_manager.chrome import ChromeDriverManager

# def init_browser():

    
    # browser = init_browser()
def scrape(): # NASA Mars News
    executable_path = {'executable_path': ChromeDriverManager().install()}
    # executable_path = {"executable_path": "C:\webdrivers\chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Parse html with bs
    html = browser.html
    soup = bs(html, "html.parser")

    # Retrieve the latest news title and text
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Save FEATURED SPACE IMAGE URL and visit the page
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Assign the HTML content of the page to a variable
    imgs_html = browser.html
    # Parse HTML with bs
    soup = bs(imgs_html,'html.parser')

    # Use splinter to Click the featured image 
    # to bring up the full resolution image
    image_url = soup.find("img", class_="headerimage fade-in")["src"]
    featured_image_url = url + image_url


    # Save MARS FACTS URL and visit the page
    facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(facts_url)

    #Extract the Facts Table from the URL using pandas
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ["Description","Mars","Earth"]
    idx_df = df.set_index("Description")
    fact_table= idx_df.to_html(classes="table table-striped")
    # html_table= idx_df.to_html(classes="table table-striped")


    # Visit USGS webpage for Mars hemispehere images
    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)

    hemisphere_images=[]
    links=browser.find_by_css("a.product-item img")

    for x in range(len(links)):
        img_info={}
        
        browser.find_by_css('a.product-item img')[x].click()
        
        # Find the Sample image anchor tag and extract the href
        sample=browser.links.find_by_text('Sample').first
        img_info['img_url']=sample['href']
        
        # Add title to the img_info dict
        img_info['title']=browser.find_by_css('h2.title').text
        
        hemisphere_images.append(img_info)
        
        browser.back()



    # url = "https://marshemispheres.com/"
    # browser.visit(url + 'index.html')
    # # html = browser.html

    # Parse HTML with Beautiful Soup
    # soup =bs(html, "html.parser")

    # Create dictionary to store titles & links to images
    # img_title_list=[]
    # # links=browser.find_by_css("a.product-item img")

    # # Retrieve all elements that contain image information
    # # results = soup.find("div", class_ = "collapsible results" )
    # # pics = results.find_all("div", class_="item")

    # # Iterate through each image
    # for x in range(4):
    #     img_info ={}
        
    #     browser.find_by_css('a.product-item img')[x].click()
    
    #     # Find the Sample image anchor tag and extract the href
    #     sample=browser.links.find_by_text('Sample').first
    #     img_info['img_url']=sample['href']
        
    #     # Add title to the img_info dict
    #     img_info['title']=browser.find_by_css('h2.title').text
        
    #     img_title_list.append(img_info)

    scraped_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        # "facts": html_table,
        "facts": fact_table,
        "hemispheres": hemisphere_images,
        "last_modified": dt.datetime.now()
    }

    return scraped_data

if __name__=="__main__":
    print(scrape())
