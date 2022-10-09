# imports ------------------------------------------------------------------------
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from bs4 import BeautifulSoup as bs
import datetime as dt

# scrape_all ---------------------------------------------------------------------
def scrape_all():

    # init splinter browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser=Browser('chrome', **executable_path, headless = False)

    # call for news information
    title, preview = scrape_news(browser)

    mars_data = {
        'title': title,
        'preview': preview,
        'image_link': scrape_image(browser),
        'facts' : scrape_facts(browser),
        'hemis' : scrape_hemis(browser),
        'lastUpdated' : dt.datetime.now()
    }

    browser.quit()
    return mars_data

# scrape_news --------------------------------------------------------------------
def scrape_news(browser):

    url='https://redplanetscience.com/'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=2)
    response = browser.html

    # parse html for headline card
    soup = bs(response, 'html.parser')
    card = soup.find('div','list_text')

    title = card.find('div','content_title').get_text()
    preview = card.find('div','article_teaser_body').get_text()
    return title, preview

# scrape_image -------------------------------------------------------------------
def scrape_image(browser):

    url='https://spaceimages-mars.com'
    browser.visit(url)
    image_button = browser.find_by_tag('button')[1]
    image_button.click()
    response = browser.html

    # parse html for image link
    soup = bs(response, 'html.parser')
    image_link = soup.find('img', class_= 'fancybox-image').get('src')

    image_link = f'https://spaceimages-mars.com/{image_link}'
    return image_link

# scrape_facts -------------------------------------------------------------------
def scrape_facts(browser):
    
    url='https://galaxyfacts-mars.com'
    browser.visit(url)
    response = browser.html

    # parse for html table
    soup = bs(response, 'html.parser')
    html_table = soup.find('table')
    facts = '' + str(html_table)
    return facts

# scrape_hemis -------------------------------------------------------------------
def scrape_hemis(browser):

    url='https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_list = []

    # parse html for image links
    hemisphere_links = browser.find_by_css('a.product-item img')

    # navigate through hemisphere links
    for link_idx in range(len(hemisphere_links)):

        browser.find_by_css('a.product-item img')[link_idx].click()
        sample = browser.links.find_by_text('Sample').first
        
        hemisphere = {}
        hemisphere['img_url'] = sample ['href'] 
        hemisphere['title']  = browser.find_by_css('h2.title').text
        hemisphere_list.append(hemisphere)

        # go back
        browser.back()
        
    return hemisphere_list
# --------------------------------------------------------------------------------

if __name__ == "__main__":
    print(scrape_all())