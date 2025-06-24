import requests as req
from bs4 import BeautifulSoup as bs
from bs4.element import Tag
import json 


# add docstring for the module
def fetch_url(url:str) -> str:
    """Fetch the content of a URL and return it as a string.
    Args:
        url (str): The URL to fetch.
    Returns:
        str: The content of the URL.
    
    
    
    """
    try:
        res = req.get(url)
        res.raise_for_status()  # Raise an error for bad responses
        return res.text
    except req.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None





def parse_data(html_content: str) -> json:
    def process_short_info(html:Tag) -> dict:
        container = html.find('div', class_ ='offer__short-description')
        info_items = container.find_all('div', class_ ='offer__info-item')
        info_total = {}
        for item in info_items:
            title = item.find('div', 'offer__info-title').text
            content = item.find('div', 'offer__advert-short-info').text
            print(f'{title}: {content}')
            info_total[title] = content 
        return info_total
    
    def process_long_info(html:Tag) -> dict:
        container_long_info = html.find('div', 'offer__parameters')
        long_info_items = container_long_info.find_all('dl')
        info_total = {}
        for item in long_info_items: 
            title = item.find('dt').text
            content = item.find('dd').text
            print(f'{title}: {content}')
            info_total[title] = content
        description_container = html.find('div', 'js-description a-text a-text-white-spaces')
        description = description_container.text
        info_total['Описание'] = description
        return info_total
        
    soup = bs(html_content, 'html.parser')
    main_tag = soup.find('main')
    
    short_info_with_junk = main_tag.find('div', class_ = 'offer__sidebar')
    long_info_with_junk = main_tag.find('div', class_ = 'offer__description')
    # with open('index.txt', 'w') as f:
    #     f.write(short_info.text + '<hr>' + full_info.text)
    total = dict(process_short_info(short_info_with_junk))
    total.update(process_long_info(long_info_with_junk))
    return json.dumps(total)    



# def scrape_website():
#     if __name__ == "__main__":
#         res = fetch_url("https://krisha.kz/a/show/699217422")
#         parse_data(res)
urls = ['https://krisha.kz/a/show/699217422', 'https://krisha.kz/a/show/699558305', 'https://krisha.kz/a/show/762062147', 'https://krisha.kz/a/show/1002472540', 'https://krisha.kz/a/show/762094841']
for url in urls: 
    res = fetch_url(url)
    data:json = parse_data(res)
    with open('res.txt', 'a') as f:
        f.write(str(data) + '\n')