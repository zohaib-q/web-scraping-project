from bs4 import BeautifulSoup as bs
import requests
import webbrowser
import pandas as pd

HEADERS = {
    # 'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
    #                 'AppleWebKit/537.36 (KHTML, like Gecko)'
    #                 'Chrome/44.0.2403.157 Safari/537.36'),
    # 'Accept-Language': 'en-US, en;q=0.5'
       
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'accept-language': 'en-GB,en;q=0.9',
}

def ebay_tings(product_name):
    '''
    This function webscrapes ebay for the item information and puts the information into lists using substrings
        Parameters:
        the item the user wants (string)

        Returns:
        a list of all the items containing [item name, price, average review, number of reviews, link, validity score]
    '''
    bad_strings = ['US $', '/ea', 'AU $', 'GBP', 'EUR ', 'JPY ', 'CAD ', 'EGP ', ',']

    #adjusts the url
    ebay_url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=&_sacat=0'
    product_name = product_name.replace(' ', '+')
    ebay_url = ebay_url.replace('nkw=', 'nkw=' + product_name)

    #acesses the webpage
    r2 = requests.get(ebay_url, headers = HEADERS)
    ebay_soup = bs(r2.content, features="html.parser")

    #finds the number of pages of items
    e_num_pages = ebay_soup.find_all('a', attrs={'class' : 'pagination__item'})
    ebay_num_len = len(e_num_pages)
    
    ebay_item_desc = list()
    i = 1

    while i < ebay_num_len:
        #accesses the multiple pages
        new_ebay_links = ebay_url + '&_pgn=' + str(i)
        ebay_new_link = requests.get(new_ebay_links, headers = HEADERS)
        new_ebay_soup = bs(ebay_new_link.content,features="html.parser")

        #accesses the individual item page
        ebay_further_links = [link.get('href') for link in new_ebay_soup.find_all('a', attrs={'class': 's-item__link'})]
        for ite in range(len(ebay_further_links)):
            detailed_e = requests.get(ebay_further_links[ite], headers=HEADERS)
            new_ebay_soup_2 = bs(detailed_e.content, "html.parser")
            specific_item = list()

            #name
            specific_item.append(new_ebay_soup_2.find('h1', attrs={'class': 'x-item-title__mainTitle'}).text if new_ebay_soup_2.find('h1', attrs={'class': 'x-item-title__mainTitle'}) else 'None')
            #price
            specific_item.append(new_ebay_soup_2.find('div', attrs={'class': 'x-price-primary'}).text if new_ebay_soup_2.find('div', attrs={'class': 'x-price-primary'}) else '0.0')
            #average review
            specific_item.append(new_ebay_soup_2.find('span', attrs={'class': 'ux-summary__start--rating'}).text if new_ebay_soup_2.find('span', attrs={'class': 'ux-summary__start--rating'}) else '0.0')
            #number of reviews
            specific_item.append( new_ebay_soup_2.find('span', attrs={'class': 'ux-summary__count'}).text if new_ebay_soup_2.find('span', attrs={'class': 'ux-summary__count'}) else '0')
            
            #gets the item link
            try:
                specific_item.append(ebay_further_links[ite])
            except:
                specific_item.append('no link available')
                
            ebay_item_desc.append(specific_item)
        i += 1

    while i < len(ebay_item_desc):
        #isolates the price to convert it to a float
        try:
            ebay_item_desc[i][1] = ebay_item_desc[i][1].replace('None', '0')
        except:
            pass
        for j in range(len(bad_strings)):
            if bad_strings[j] in ebay_item_desc[i][1]:
                ebay_item_desc[i][1] = ebay_item_desc[i][1].replace(bad_strings[j], '')
        ebay_item_desc[i][1] = float(ebay_item_desc[i][1])

        #converts average review to float
        ebay_item_desc[i][2] = float(ebay_item_desc[i][2])

        #converts number of reviews to int
        try:
            ebay_item_desc[i][3] = ebay_item_desc[i][3].replace(' product ratings', '')
        except:
            pass
        try:
            ebay_item_desc[i][3] = int(ebay_item_desc[i][3])
        except:
            ebay_item_desc[i][3] = 0

        #gets product validity score
        try:
            ebay_item_desc[i].append(ebay_item_desc[i][2] * ebay_item_desc[i][3])
        except:
            ebay_item_desc[i].append(0)
        if ebay_item_desc[i][0] == 'None':
            del ebay_item_desc[i]
        else:
            i += 1

        

    return ebay_item_desc
