from bs4 import BeautifulSoup as bs
import requests
import webbrowser
import pandas as pd

HEADERS = {
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    # 'accept-language': 'en-GB,en;q=0.9',
    "accept-language": "en-US,en;q=0.9","accept-encoding": "gzip, deflate, br","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }
def walmart_tings(product_name):
    '''
    This function webscrapes walmart for the item information and puts the information into lists using substrings
        Parameters:
        the item the user wants (string)

        Returns:
        a list of all the items containing [item name, price, average review, number of reviews, link, validity score]
    '''
    # HEADERS = {
    # #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    # # 'accept-language': 'en-GB,en;q=0.9',
    # "accept-language": "en-US,en;q=0.9","accept-encoding": "gzip, deflate, br","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    # }
    
    #adjusts the website url
    walmart_url = 'https://www.walmart.com/search?q='
    product_name = product_name.replace(' ', '+')
    walmart_url = walmart_url.replace('search?q=', 'search?q=' + product_name)

    #acesses the website
    r3 = requests.get(walmart_url, headers = HEADERS)
    walmart_soup = bs(r3.content, features="html.parser")

    #finds the general item description, name, and price
    walmart_item_desc = walmart_soup.find_all('div', attrs={'class' : 'mb0 ph0-xl pt0-xl bb b--near-white w-25 pb3-m ph1'})
    walmart_names = walmart_soup.find_all('span', attrs={'class' : 'normal dark-gray mb0 mt1 lh-title f6 f5-l lh-copy'})
    walmart_prices = walmart_soup.find_all('div', attrs={'data-automation-id' : 'product-price'})
    walmart_items = list()
    
    #gets rid of extra HTML text
    for i in range(len(walmart_names)):
        walmart_names[i] = walmart_names[i].text
    for i in range(len(walmart_prices)):
        walmart_prices[i] = walmart_prices[i].text

    i = 0
    j = 0
    while i < len(walmart_item_desc):
        temp_list = list()
        
        #adds item link to item description
        try:
            walmart_item_desc[i] = walmart_item_desc[i].text + 'link: https://www.walmart.com/' + walmart_item_desc[i].find('a', attrs={'class' : 'absolute w-100 h-100 z-1 hide-sibling-opacity'}).get('href')
        except:
            walmart_item_desc[i] = walmart_item_desc[i].text

        #gets name of item
        temp_list.append(walmart_names[i])

        #gets price of item and isolates the numbers in order to convert it to float
        if '$' in walmart_item_desc[i]:
            if 'current price' in walmart_prices[j]:
                price_index = walmart_prices[j].find('current price')
                walmart_prices[j] = walmart_prices[j][price_index+15:]
                bad_str = 'ow'
                if bad_str in walmart_prices[j]:
                    walmart_prices[j] = walmart_prices[j].replace('ow $', '')
                
                if '$' in walmart_prices[j]:
                    index = walmart_prices[j].find('$')
                    walmart_prices[j] = walmart_prices[j][:index]
                if '+' in walmart_prices[j]:
                    walmart_prices[j] = walmart_prices[j].replace('+', '')
                if ',' in walmart_prices[j]:
                    walmart_prices[j] = walmart_prices[j].replace(',', '')
                try:
                    temp_list.append(float(walmart_prices[j]))
                except:
                    index = walmart_prices[j].find('.') + 3
                    walmart_prices[j] = walmart_prices[j][:index]
                    temp_list.append(float(walmart_prices[j]))
                j += 1
            
            elif 'From$' in walmart_prices[j] and 'Was $' in walmart_prices[j]:
                index = walmart_prices[j].find('$') + 1
                walmart_prices[j] = walmart_prices[j][index:]
                index = walmart_prices[j].find('$')
                walmart_prices[j] = walmart_prices[j][:index]
                walmart_prices[j] = walmart_prices[j][:len(walmart_prices[j])-2] + '.' + walmart_prices[j][len(walmart_prices[j])-2:]
                if ',' in walmart_prices[j]:
                    walmart_prices[j] = walmart_prices[j].replace(',', '')
                temp_list.append(float(walmart_prices[j]))
                j+=1

            elif 'From$' in walmart_prices[j]:
                if ' months' in walmart_prices[j]:
                    index_num_months = walmart_prices[j].find(' months') - 2
                    num_months = walmart_prices[j][index_num_months:index_num_months+2]
                    num_months = num_months.strip()
                    num_months = int(num_months)

                    #price comes right after 'From$'
                    price_index = 5
                    index = walmart_prices[j].find('/month') - 2
                    walmart_prices[j] = walmart_prices[j][5:index] + '.' + walmart_prices[j][index:index+8]
                    price = float(walmart_prices[j][:index-2])
                    if ',' in walmart_prices[j]:
                        walmart_prices[j] = walmart_prices[j].replace(',', '')
                    total_price = num_months * price
                    temp_list.append([walmart_prices[j], total_price])
                    j+=1
                else:
                    price_index = 5
                    walmart_prices[j] = walmart_prices[j][5:]
                    walmart_prices[j] = walmart_prices[j][:len(walmart_prices[j])-2] + '.' + walmart_prices[j][len(walmart_prices[j])-2:]
                    if ',' in walmart_prices[j]:
                        walmart_prices[j] = walmart_prices[j].replace(',', '')
                    temp_list.append(float(walmart_prices[j]))
                    j+=1
            elif 'Was $' in walmart_prices[j]:
                walmart_prices[j] = walmart_prices[j][1:]
                index = walmart_prices[j].find('$')
                walmart_prices[j] = walmart_prices[j][:index - 2] + '.' + walmart_prices[j][index-2:index]
                if ',' in walmart_prices[j]:
                    walmart_prices[j] = walmart_prices[j].replace(',', '')
                temp_list.append(float(walmart_prices[j]))
                j+=1
            elif '$' in walmart_prices[j]:
                index = walmart_prices[j].find('$')+1
                walmart_prices[j] = walmart_prices[j][index:len(walmart_prices[j])-2] + '.' + walmart_prices[j][len(walmart_prices[j])-2:]
                if ',' in walmart_prices[j]:
                    walmart_prices[j] = walmart_prices[j].replace(',', '')
                temp_list.append(float(walmart_prices[j]))
                j+=1
        else:
            temp_list.append(0)

        #gets the average review and isolates it to convert it to a float
        if 'out of 5 Stars' in walmart_item_desc[i]:
            review_index = walmart_item_desc[i].find(' out of 5 Stars')
            review_str = walmart_item_desc[i][review_index-3:review_index]
            if '.' not in review_str:
                review_str = review_str[2]
            temp_list.append(float(review_str))
        else:
            temp_list.append(0)

        #gets number of reviews and isolates it to convert it to an int
        if ' reviews' in walmart_item_desc[i]:
            num_of_reviews = walmart_item_desc[i].find(' reviews')
            temp_string = walmart_item_desc[i][review_index+17:num_of_reviews]
            temp_list.append(int(temp_string))
        else:
            temp_list.append(0)
        
        #gets the item link
        if 'link: https://www.walmart.com/' in walmart_item_desc[i]:
            link_index = walmart_item_desc[i].find('link: https://www.walmart.com/') + 6
            modified_str4 = walmart_item_desc[i][link_index:]
            temp_list.append(modified_str4)
        else:
            temp_list.append('No link available')

        #gets the validity score
        temp_list.append(temp_list[2] * temp_list[3])

        walmart_items.append(temp_list)
        i += 1


    return walmart_items

 
