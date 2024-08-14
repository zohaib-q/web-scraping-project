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

    ebay_url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=&_sacat=0'

    product_name = product_name.replace(' ', '+')

    ebay_url = ebay_url.replace('nkw=', 'nkw=' + product_name)

    r2 = requests.get(ebay_url, headers = HEADERS)

    ebay_soup = bs(r2.content, features="html.parser")

    e_num_pages = ebay_soup.find_all('a', attrs={'class' : 'pagination__item'})
    ebay_num_len = len(e_num_pages)
    ebay_item_desc = list()
    i = 1

    while i < ebay_num_len:
        new_ebay_links = ebay_url + '&_pgn=' + str(i)
        
        ebay_new_link = requests.get(new_ebay_links, headers = HEADERS)
        new_ebay_soup = bs(ebay_new_link.content,features="html.parser")

        ebay_further_links = list()
        ebay_search_links = new_ebay_soup.find_all('a', attrs={'class' : 's-item__link'})

        for elements in ebay_search_links:
            ebay_further_links.append(elements.get('href'))

        for ite in range(len(ebay_further_links)):
            detailed_e = requests.get(ebay_further_links[ite], headers=HEADERS)
            new_ebay_soup_2 = bs(detailed_e.content, "html.parser")
            specific_item = list()

            try:
                specific_item.append(new_ebay_soup_2.find('h1', attrs= {'class' : 'x-item-title__mainTitle'}).text)
            except:
                specific_item.append('None')

            try:
                specific_item.append(new_ebay_soup_2.find('div', attrs= {'class' : 'x-price-primary'}).text)
            except:
                specific_item.append(0.0)

            try:
                specific_item.append(new_ebay_soup_2.find('span', attrs={'class' : 'ux-summary__start--rating'}).text)    
            except:
                specific_item.append(0.0)
            
            try:
                specific_item.append(new_ebay_soup_2.find('span', attrs = {'class' : 'ux-summary__count'}).text)
            except:
                specific_item.append(0)
                
            ebay_item_desc.append(specific_item)
        i += 1

    for i in range(len(ebay_item_desc)):
        try:
            #price
            ebay_item_desc[i][1] = ebay_item_desc[i][1].replace('US $', '')
            ebay_item_desc[i][1] = ebay_item_desc[i][1].replace('/ea', '')
            ebay_item_desc[i][1] = ebay_item_desc[i][1].replace('None', '0')
            ebay_item_desc[i][1] = float(ebay_item_desc[i][1])
            #reviews
            ebay_item_desc[i][2] = float(ebay_item_desc[i][2])
            #number of reviews
            ebay_item_desc[i][3] = ebay_item_desc[i][3].replace(' product ratings', '')
            ebay_item_desc[i][3] = int(ebay_item_desc[i][3])

            #product score
            ebay_item_desc[i].append(ebay_item_desc[i][2] * ebay_item_desc[i][3])
            # print(ebay_item_desc[i][1])
        except:
            ebay_item_desc[i].append(0)

        

    return ebay_item_desc

#gets user input
# item = input("Enter the item you would like: ")
# print(item)
# print(ebay_tings(item))

# ebay_item_desc.sort(key = lambda x:x[1])


# print(len(ebay_item_desc))

#US $9.99/ea
#US $9.99