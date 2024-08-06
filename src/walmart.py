from bs4 import BeautifulSoup as bs
import requests
import webbrowser
import pandas as pd

HEADERS = {
    # 'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
    #                 'AppleWebKit/537.36 (KHTML, like Gecko)'
    #                 'Chrome/44.0.2403.157 Safari/537.36'),
    # 'Accept-Language': 'en-US, en;q=0.5'
       
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    # 'accept-language': 'en-GB,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}
def walmart_tings(product_name):
    walmart_url = 'https://www.walmart.com/search?q='

    product_name = product_name.replace(' ', '+')

    walmart_url = walmart_url.replace('search?q=', 'search?q=' + product_name)

    r3 = requests.get(walmart_url, headers = HEADERS)

    walmart_soup = bs(r3.content, features="html.parser")

    walmart_further_links = list()
    walmart_search_links = walmart_soup.find_all('a', attrs={'class' : 'absolute w-100 h-100 z-1 hide-sibling-opacity'})
    walmart_item_desc = list()

    for element in walmart_search_links:
        walmart_further_links.append('https://www.walmart.com/' + element.get('href'))

    for it in range(len(walmart_further_links)):
        detailed_w = requests.get(walmart_further_links[it], headers=HEADERS)
        new_walmart_soup = bs(detailed_w.content, "html.parser")
        specific_item = list()

        try:
            specific_item.append(new_walmart_soup.find('h1', attrs= {'class' : 'lh-copy dark-gray mv1 f3 mh0-l mh3 f4 black b'}).text)
        except:
            specific_item.append('None')

        try:
            specific_item.append(new_walmart_soup.find('span', attrs= {'class' : 'inline-flex flex-column'}).text)
        except:
            specific_item.append('None')

        try:
            specific_item.append(new_walmart_soup.find('span', attrs= {'class' : 'f7 rating-number'}).text) 
        except:
            specific_item.append('None')
            
        walmart_item_desc.append(specific_item)
    
    return walmart_item_desc

#gets user input
# item = input("Enter the item you would like: ")
# print(item)
# print(walmart_tings(item))

# print(walmart_soup)
# print(len(walmart_search_links))
# print(walmart_further_links)
# print(len(walmart_further_links))
# webbrowser.open(walmart_url, new = 2)