from bs4 import BeautifulSoup as bs
import requests
import webbrowser
import pandas as pd

#need headers in order to webscrape these websites
HEADERS = {
    # 'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
    #                 'AppleWebKit/537.36 (KHTML, like Gecko)'
    #                 'Chrome/44.0.2403.157 Safari/537.36'),
    # 'Accept-Language': 'en-US, en;q=0.5'
       
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'accept-language': 'en-GB,en;q=0.9',

    # "accept-language": "en-US,en;q=0.9","accept-encoding": "gzip, deflate, br","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"

#  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
#  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#  "Accept-Language": "en-US,en;q=0.9"
    
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    # "Accept-Language": "en-US,en;q=0.9",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    # "Connection": "keep-alive",
    # "Upgrade-Insecure-Requests": "1",
    # "DNT": "1",  # Do Not Track Request Header
    # "TE": "Trailers",

    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    # "Accept-Language": "en-US,en;q=0.5",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    # "Connection": "keep-alive",
    # "Referer": "https://www.amazon.com/",
    # "Sec-Fetch-Dest": "document",
    # "Sec-Fetch-Mode": "navigate",
    # "Sec-Fetch-Site": "same-origin",
    # "Sec-Fetch-User": "?1",
    # "Upgrade-Insecure-Requests": "1",
}

def amazon_tings(product_name):
    HEADERS = {
    # 'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
    #                 'AppleWebKit/537.36 (KHTML, like Gecko)'
    #                 'Chrome/44.0.2403.157 Safari/537.36'),
    # 'Accept-Language': 'en-US, en;q=0.5'
       
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'accept-language': 'en-GB,en;q=0.9',
        
    # "accept-language": "en-US,en;q=0.9","accept-encoding": "gzip, deflate, br","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    
#      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
#  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#  "Accept-Language": "en-US,en;q=0.9"
        
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    # "Accept-Language": "en-US,en;q=0.9",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    # "Connection": "keep-alive",
    # "Upgrade-Insecure-Requests": "1",
    # "DNT": "1",  # Do Not Track Request Header
    # "TE": "Trailers",
        
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    # "Accept-Language": "en-US,en;q=0.5",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    # "Connection": "keep-alive",
    # "Referer": "https://www.amazon.com/",
    # "Sec-Fetch-Dest": "document",
    # "Sec-Fetch-Mode": "navigate",
    # "Sec-Fetch-Site": "same-origin",
    # "Sec-Fetch-User": "?1",
    # "Upgrade-Insecure-Requests": "1",
    }
    amazon_url = 'https://www.amazon.com/s?k='


    product_name = product_name.replace(' ', '+')

    amazon_url = amazon_url.replace('s?k=', 's?k=' + product_name)

    r = requests.get(amazon_url, headers = HEADERS)

    amazon_soup = bs(r.content,features="html.parser")

    a_num_pages = amazon_soup.find('span', attrs={'class' : 's-pagination-item s-pagination-disabled'}).text

    a_num_pages = int(a_num_pages)


    expected_len = 0
    expected_len2 = 0
    ting = 0

    amazon_products = list()
    for nummms in range(a_num_pages):
        new_a_link = amazon_url + "&page=" + str(nummms+1)
        amazon_new_link = requests.get(new_a_link, headers = HEADERS)
        new_amazon_soup = bs(amazon_new_link.content,features="html.parser")


        a_product_desc = new_amazon_soup.find_all('div', attrs = {'class' : 'a-section a-spacing-small a-spacing-top-small'})
        a_product_desc_2 = new_amazon_soup.find_all('div', attrs = {'class' : 'a-section a-spacing-small puis-padding-left-small puis-padding-right-small'})

        expected_len += len(a_product_desc)
        expected_len2 += len(a_product_desc_2)
        
        amazon_products.extend(a_product_desc)
        amazon_products.extend(a_product_desc_2)

    for ting in range(len(amazon_products)):
        try:
            amazon_products[ting] = amazon_products[ting].text + 'link: https://www.amazon.com/' + amazon_products[ting].find('a', attrs = {'class' : 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).get('href')
        except:
            amazon_products[ting] = amazon_products[ting].text

    detailed_amazon_products = list()

    for i in range(len(amazon_products)):
        amazon_products[i] = amazon_products[i].replace('Featured from Amazon brandsFeatured from Amazon brands ', '')
        amazon_products[i] = amazon_products[i].replace('SponsoredSponsored You’re seeing this ad based on the product’s relevance to your search query.Leave ad feedback ', '')

    for i in amazon_products:
        temp_list = list()
        index_num = i.find('out of 5 stars')
        price_index = i.find('$')
        modified_str = i[price_index+1:]
        price2_index = modified_str.find('$')
        modified_str_2 = i[index_num+15:]
        index_num -= 4

        number_of_reviews = modified_str_2.find(' ')

        #name of item
        temp_list.append(i[0:index_num-1])
        #item price
        temp_list.append(i[price_index+1:price_index+price2_index+1])
        #item review
        temp_list.append(i[index_num:index_num+3])
        #number of reviews
        temp_list.append(i[index_num+19:index_num+19+number_of_reviews])
        #link to item
        if 'link: https://www.amazon.com/' in i:
            link_index = i.find('link: https://www.amazon.com/') + 6
            modified_str3 = i[link_index:]
            temp_list.append(modified_str3)
        else:
            temp_list.append('No link available')
        #add to list
        detailed_amazon_products.append(temp_list)

    no_good_string = '\n'
    for i in range(len(detailed_amazon_products)):
        if no_good_string in detailed_amazon_products[i][0]:
            detailed_amazon_products[i] = ['None', '0', '0', '0']

        try:
            detailed_amazon_products[i][1] = detailed_amazon_products[i][1].replace(',','')
        except:
            pass
        try:
            detailed_amazon_products[i][3] = detailed_amazon_products[i][3].replace(',','')
        except:
            pass
        try:
            detailed_amazon_products[i][1] = float(detailed_amazon_products[i][1])
        except:
            detailed_amazon_products[i][1] = 0
        try:
            detailed_amazon_products[i][2] = float(detailed_amazon_products[i][2])
        except:
            detailed_amazon_products[i][2] = 0
        try:
            detailed_amazon_products[i][3] = int(detailed_amazon_products[i][3])
        except:
            detailed_amazon_products[i][3] = 0

        if '$' in detailed_amazon_products[i][0]:
            index = detailed_amazon_products[i][0].find('$')
            detailed_amazon_products[i][0] = detailed_amazon_products[i][0][:index]

        #validity score (multiplies number of reviews with average score)
        detailed_amazon_products[i].append(detailed_amazon_products[i][2] * detailed_amazon_products[i][3])
        


        if detailed_amazon_products[i][1] is str:
            detailed_amazon_products[i][1] = 0
        
        if detailed_amazon_products[i][2] is str:
            detailed_amazon_products[i][2] = 0
        
        if detailed_amazon_products[i][3] is str:
            detailed_amazon_products[i][3] = 0

    i = 0
    while i < len(detailed_amazon_products):
        if detailed_amazon_products[i][0] == 'None':
            del detailed_amazon_products[i]
        else:
            i += 1

    return detailed_amazon_products

