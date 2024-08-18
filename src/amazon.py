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
}

def amazon_tings(product_name):
    '''
    This function webscrapes amazon for the item information and puts the information into lists using substrings
        Parameters:
        the item the user wants (string)

        Returns:
        a list of all the items containing [item name, price, average review, number of reviews, link, validity score]
    '''


    # HEADERS = {
    # # 'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
    # #                 'AppleWebKit/537.36 (KHTML, like Gecko)'
    # #                 'Chrome/44.0.2403.157 Safari/537.36'),
    # # 'Accept-Language': 'en-US, en;q=0.5'
       
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    # 'accept-language': 'en-GB,en;q=0.9',
        
    # # "accept-language": "en-US,en;q=0.9","accept-encoding": "gzip, deflate, br","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    # }
    
    #adjusts the url to plug into beautiful soup
    amazon_url = 'https://www.amazon.com/s?k='
    product_name = product_name.replace(' ', '+')
    amazon_url = amazon_url.replace('s?k=', 's?k=' + product_name)

    #acesses the website
    r = requests.get(amazon_url, headers = HEADERS)
    amazon_soup = bs(r.content,features="html.parser")

    #finds the number of pages of items
    a_num_pages = amazon_soup.find('span', attrs={'class' : 's-pagination-item s-pagination-disabled'}).text
    a_num_pages = int(a_num_pages)
    
    #length for the two types of amazon items
    expected_len = 0
    expected_len2 = 0

    #list where the items go
    amazon_products = list()

    #traverses the amazon pages
    for nummms in range(a_num_pages):
        #accesses the various pages of the amazon website
        new_a_link = amazon_url + "&page=" + str(nummms+1)
        amazon_new_link = requests.get(new_a_link, headers = HEADERS)
        new_amazon_soup = bs(amazon_new_link.content,features="html.parser")

        #finds the product information
        a_product_desc = new_amazon_soup.find_all('div', attrs = {'class' : 'a-section a-spacing-small a-spacing-top-small'})
        a_product_desc_2 = new_amazon_soup.find_all('div', attrs = {'class' : 'a-section a-spacing-small puis-padding-left-small puis-padding-right-small'})

        #adjusts the expected length
        expected_len += len(a_product_desc)
        expected_len2 += len(a_product_desc_2)
        
        #Puts the two types of items in one list
        amazon_products.extend(a_product_desc)
        amazon_products.extend(a_product_desc_2)

    for ting in range(len(amazon_products)):
        #only takes the text of the item and not the HTML text associated with it
        try:
            #takes the text and the link associated with the item if the link is available
            amazon_products[ting] = amazon_products[ting].text + 'link: https://www.amazon.com/' + amazon_products[ting].find('a', attrs = {'class' : 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).get('href')
        except:
            amazon_products[ting] = amazon_products[ting].text

    detailed_amazon_products = list()

    for i in range(len(amazon_products)):
        #gets rid of extra unnecessary text
        amazon_products[i] = amazon_products[i].replace('Featured from Amazon brandsFeatured from Amazon brands ', '')
        amazon_products[i] = amazon_products[i].replace('SponsoredSponsored You’re seeing this ad based on the product’s relevance to your search query.Leave ad feedback ', '')

    for i in amazon_products:
        #starts to organize the list
        temp_list = list()
        #index to find average review
        index_num = i.find('out of 5 stars')
        #index to find price
        price_index = i.find('$')
        modified_str = i[price_index+1:]
        price2_index = modified_str.find('$')
        #index to find number of reviews
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
        #gets rid of more unnecessary items from the list and converts price, reviews, num reviews to floats and ints
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
        #gets rid of extra entries to list
        if detailed_amazon_products[i][0] == 'None':
            del detailed_amazon_products[i]
        else:
            i += 1

    return detailed_amazon_products

