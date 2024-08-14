from bs4 import BeautifulSoup as bs
import requests
import webbrowser
import pandas as pd
import ebay
import walmart
import amazon
#########################################################################################################
### how to change url for each website to search for different things ###

# https://www.amazon.com/s?k=(put name here)

# https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=(put name here)&_sacat=0

# https://www.walmart.com/search?q=(put name here)

#########################################################################################################

#user agent to be able to scape amazon
HEADERS = {
    # 'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
    #                 'AppleWebKit/537.36 (KHTML, like Gecko)'
    #                 'Chrome/44.0.2403.157 Safari/537.36'),
    # 'Accept-Language': 'en-US, en;q=0.5'
       
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'accept-language': 'en-GB,en;q=0.9',
}
class item:
    def __init__(self, amazon_list, walmart_list, ebay_list):
        self.amazon_list =  amazon_list
        self.walmart_list = walmart_list
        self.ebay_list = ebay_list


    def sort_high_low(self, general_list, strr2, i):
        if strr2 == 'l to h':
            general_list = sorted(general_list,key=lambda l:l[i])
            return general_list
        elif strr2 == 'h to l':
            general_list = sorted(general_list,key=lambda l:l[i], reverse=True)
            return general_list
        else:
            return 'invalid option'

    def sort_item_list(self, strr, strr2):
        if strr == 'price':
            self.amazon_list = self.sort_high_low(self.amazon_list, strr2, 1)
            self.walmart_list = self.sort_high_low(self.walmart_list, strr2, 1)
            self.ebay_list = self.sort_high_low(self.ebay_list, strr2, 1)
        if strr == 'reviews':
            self.amazon_list = self.sort_high_low(self.amazon_list, strr2, 2)
            self.walmart_list = self.sort_high_low(self.walmart_list, strr2, 2)
            self.ebay_list = self.sort_high_low(self.ebay_list, strr2, 2)
        if strr == 'num of reviews':
            self.amazon_list = self.sort_high_low(self.amazon_list, strr2, 3)
            self.walmart_list = self.sort_high_low(self.walmart_list, strr2, 3)
            self.ebay_list = self.sort_high_low(self.ebay_list, strr2, 3)
        if strr == 'validity score':
            self.amazon_list = self.sort_high_low(self.amazon_list, strr2, 4)
            self.walmart_list = self.sort_high_low(self.walmart_list, strr2, 4)
            self.ebay_list = self.sort_high_low(self.ebay_list, strr2, 4)
        
        return self.amazon_list, self.walmart_list, self.ebay_list

#gets user input
item = input("Enter the item you would like: ")
print(item)
item = item.replace(' ', '+')

strr = input("\nHow would you like the list sorted \nPlease type in one of the following: price, reviews, num of reviews, validity score: ")

strr2 = input("\nWould you like the list sorted from low to high or high to low? \nType in either l to h or h to l: ")

amazon_list = amazon.amazon_tings(item)

walmart_list = walmart.walmart_tings(item)

ebay_list = ebay.ebay_tings(item)

amazon_list, walmart_list, ebay_list = item.sort_item_list(amazon_list, walmart_list, ebay_list, strr, strr2)

print(amazon_list)




