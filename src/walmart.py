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
    "accept-language": "en-US,en;q=0.9","accept-encoding": "gzip, deflate, br","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }
def walmart_tings(product_name):
    HEADERS = {
    # 'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
    #                 'AppleWebKit/537.36 (KHTML, like Gecko)'
    #                 'Chrome/44.0.2403.157 Safari/537.36'),
    # 'Accept-Language': 'en-US, en;q=0.5'
       
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    # 'accept-language': 'en-GB,en;q=0.9',
    "accept-language": "en-US,en;q=0.9","accept-encoding": "gzip, deflate, br","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }
    walmart_url = 'https://www.walmart.com/search?q='

    product_name = product_name.replace(' ', '+')

    walmart_url = walmart_url.replace('search?q=', 'search?q=' + product_name)

    r3 = requests.get(walmart_url, headers = HEADERS)

    walmart_soup = bs(r3.content, features="html.parser")

    walmart_item_desc = walmart_soup.find_all('div', attrs={'class' : 'mb0 ph0-xl pt0-xl bb b--near-white w-25 pb3-m ph1'})
    walmart_names = walmart_soup.find_all('span', attrs={'class' : 'normal dark-gray mb0 mt1 lh-title f6 f5-l lh-copy'})
    walmart_prices = walmart_soup.find_all('div', attrs={'data-automation-id' : 'product-price'})
    walmart_items = list()
    
    for i in range(len(walmart_names)):
        walmart_names[i] = walmart_names[i].text
    for i in range(len(walmart_prices)):
        walmart_prices[i] = walmart_prices[i].text
    # for i in range(len(walmart_item_desc)):
    i = 0
    j = 0
    while i < len(walmart_item_desc):
        temp_list = list()
        walmart_item_desc[i] = walmart_item_desc[i].text

        #name of item
        temp_list.append(walmart_names[i])

        #price of item
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

                    total_price = num_months * price
                    temp_list.append([walmart_prices[j], total_price])
                    j+=1
                else:
                    price_index = 5
                    walmart_prices[j] = walmart_prices[j][5:]
                    walmart_prices[j] = walmart_prices[j][:len(walmart_prices[j])-2] + '.' + walmart_prices[j][len(walmart_prices[j])-2:]

                    temp_list.append(float(walmart_prices[j]))
                    j+=1
            elif 'Was $' in walmart_prices[j]:
                walmart_prices[j] = walmart_prices[j][1:]
                index = walmart_prices[j].find('$')
                walmart_prices[j] = walmart_prices[j][:index - 2] + '.' + walmart_prices[j][index-2:index]
                temp_list.append(float(walmart_prices[j]))
                j+=1
            elif '$' in walmart_prices[j]:
                index = walmart_prices[j].find('$')+1
                walmart_prices[j] = walmart_prices[j][index:len(walmart_prices[j])-2] + '.' + walmart_prices[j][len(walmart_prices[j])-2:]
                temp_list.append(float(walmart_prices[j]))
                j+=1
        else:
            temp_list.append(0)

        #review
        if 'out of 5 Stars' in walmart_item_desc[i]:
            review_index = walmart_item_desc[i].find(' out of 5 Stars')
            review_str = walmart_item_desc[i][review_index-3:review_index]
            if '.' not in review_str:
                review_str = review_str[2]
            temp_list.append(float(review_str))
        else:
            temp_list.append(0)

        #number of reviews
        if ' reviews' in walmart_item_desc[i]:
            num_of_reviews = walmart_item_desc[i].find(' reviews')
            temp_string = walmart_item_desc[i][review_index+17:num_of_reviews]
            temp_list.append(int(temp_string))
        else:
            temp_list.append(0)

        #product score
        temp_list.append(temp_list[2] * temp_list[3])

        walmart_items.append(temp_list)
        i += 1



    # print(walmart_names)
    # print(walmart_prices)
    # walmart_further_links = list()
    # walmart_search_links = walmart_soup.find_all('a', attrs={'class' : 'absolute w-100 h-100 z-1 hide-sibling-opacity'})
    # walmart_item_desc = list()


    # for element in walmart_search_links:
    #     walmart_further_links.append('https://www.walmart.com/' + element.get('href'))

    # for it in range(len(walmart_further_links)):
    #     detailed_w = requests.get(walmart_further_links[it], headers=HEADERS)
    #     new_walmart_soup = bs(detailed_w.content, "html.parser")
    #     specific_item = list()

    #     try:
    #         specific_item.append(new_walmart_soup.find('h1', attrs= {'class' : 'lh-copy dark-gray mv1 f3 mh0-l mh3 f4 black b'}).text)
    #     except:
    #         specific_item.append('None')

    #     try:
    #         specific_item.append(new_walmart_soup.find('span', attrs= {'class' : 'inline-flex flex-column'}).text)
    #     except:
    #         specific_item.append('None')

    #     try:
    #         specific_item.append(new_walmart_soup.find('span', attrs= {'class' : 'f7 rating-number'}).text) 
    #     except:
    #         specific_item.append('None')
            
    #     walmart_item_desc.append(specific_item)
    # print(walmart_item_desc)
    # for i in range(len(walmart_items)):
    #     print(walmart_items[i][1])
    return walmart_items

#gets user input
# item = input("Enter the item you would like: ")
# print(item)
# print(walmart_tings(item))

# print(walmart_soup)
# print(len(walmart_search_links))
# print(walmart_further_links)
# print(len(walmart_further_links))
# webbrowser.open(walmart_url, new = 2)