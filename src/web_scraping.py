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
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'accept-language': 'en-GB,en;q=0.9',
}
class Item:
    def __init__(self, amazon_list, walmart_list, ebay_list):
        ''' 
        Sets up the properties of the Item object
        '''
        self.amazon_list =  amazon_list
        self.walmart_list = walmart_list
        self.ebay_list = ebay_list


    def sort_high_low(self, general_list, strr2, i):
        '''
        Sorts the lists based on if the user wants it sorted from low to high or high to low

        Parameters:
        general_list: The general list
        strr2: The string on if the user wants the list sorted from high to low or low to high
        i: The element of the list the user wants sorted

        Returns:
        The sorted list
        '''
        if strr2 == 'l to h':
            general_list = sorted(general_list,key=lambda l:l[i])
            return general_list
        elif strr2 == 'h to l':
            general_list = sorted(general_list,key=lambda l:l[i], reverse=True)
            return general_list
        else:
            return 'invalid option'

    def num_items_shown(self, strr3):
        '''
        Takes the sorted list and only displays the number of items the user wants to see

        Parameters:
        strr3: The number of items the user wants to see

        Returns:
        the 3 lists with the limited number of items
        '''
        try:
            strr3 = int(strr3)
            i = 0
            short_a_list = list()
            short_w_list = list()
            short_e_list = list()
            while i < strr3:
                try:
                    short_a_list.append(self.amazon_list[i])
                except:
                    pass
                try:
                    short_w_list.append(self.walmart_list[i])
                except:
                    pass
                try:
                    short_e_list.append(self.ebay_list[i])
                except:
                    pass
                i += 1
            return short_a_list, short_w_list, short_e_list
        except:
            return 'invalid string entered'

    def sort_item_list(self, strr, strr2, strr3):
        '''
        Utilizes the previous two functions to sort the 3 lists and display the sorted lists with the number of items the user wants to be displayed

        Parameters:
        strr: the category the user wants sorted
        strr2: Whether the user wants the list sorted from low to high or high to low
        strr3: The number of items the user wants to see

        Returns:
        The three sorted lists
        '''
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
        
        return self.num_items_shown(strr3)
    
    def best_item_helper(self, strr2, i):
        '''
        Helper function to determine the 'best product' based on the users filter preferences

        Parameters:
        strr2: Whether the user wants the list sorted from low to high or high to low
        i: the category the user wants sorted

        Returns:
        The information of the best product
        '''
        return_str = ''
        if strr2 == 'h to l':
            if self.amazon_list[0][i] > self.ebay_list[0][i]:
                if self.amazon_list[0][i] > self.walmart_list[0][i]:
                    return_str = 'Name: ' + str(self.amazon_list[0][0]) + '\nPrice: ' + str(self.amazon_list[0][1]) + '\nReviews: ' + str(self.amazon_list[0][2]) + '\nNumber of Reviews: ' + str(self.amazon_list[0][3]) + '\nValidity Score: ' + str(self.amazon_list[0][5]) + '\nLink: ' + str(self.amazon_list[0][4])
                    return return_str
            if self.ebay_list[0][i] > self.amazon_list[0][i]:
                if self.ebay_list[0][i] > self.walmart_list[0][i]:
                    return_str = 'Name: ' + str(self.ebay_list[0][0]) + '\nPrice: ' + str(self.ebay_list[0][1]) + '\nReviews: ' + str(self.ebay_list[0][2]) + '\nNumber of Reviews: ' + str(self.ebay_list[0][3]) + '\nValidity Score: ' + str(self.ebay_list[0][5]) + '\nLink: ' + str(self.ebay_list[0][4])
                    return return_str
            if self.walmart_list[0][i] > self.amazon_list[0][i]:
                if self.walmart_list[0][i] > self.ebay_list[0][i]:
                    return_str = 'Name: ' + str(self.walmart_list[0][0]) + '\nPrice: ' + str(self.walmart_list[0][1]) + '\nReviews: ' + str(self.walmart_list[0][2]) + '\nNumber of Reviews: ' + str(self.walmart_list[0][3]) + '\nValidity Score: ' + str(self.walmart_list[0][5]) + '\nLink: ' + str(self.walmart_list[0][4])
                    return return_str
        if strr2 == 'l to h':
            if self.amazon_list[0][i] < self.ebay_list[0][i]:
                if self.amazon_list[0][i] < self.walmart_list[0][i]:
                    return_str = 'Name: ' + str(self.amazon_list[0][0]) + '\nPrice: ' + str(self.amazon_list[0][1]) + '\nReviews: ' + str(self.amazon_list[0][2]) + '\nNumber of Reviews: ' + str(self.amazon_list[0][3]) + '\nValidity Score: ' + str(self.amazon_list[0][5]) + '\nLink: ' + str(self.amazon_list[0][4])
            if self.ebay_list[0][i] < self.amazon_list[0][i]:
                if self.ebay_list[0][i] < self.walmart_list[0][i]:
                    return_str = 'Name: ' + str(self.ebay_list[0][0]) + '\nPrice: ' + str(self.ebay_list[0][1]) + '\nReviews: ' + str(self.ebay_list[0][2]) + '\nNumber of Reviews: ' + str(self.ebay_list[0][3]) + '\nValidity Score: ' + str(self.ebay_list[0][5]) + '\nLink: ' + str(self.ebay_list[0][4])
                    return return_str
            if self.walmart_list[0][i] < self.amazon_list[0][i]:
                if self.walmart_list[0][i] < self.ebay_list[0][i]:
                    return_str = 'Name: ' + str(self.walmart_list[0][0]) + '\nPrice: ' + str(self.walmart_list[0][1]) + '\nReviews: ' + str(self.walmart_list[0][2]) + '\nNumber of Reviews: ' + str(self.walmart_list[0][3]) + '\nValidity Score: ' + str(self.walmart_list[0][5]) + '\nLink: ' + str(self.walmart_list[0][4])
                    return return_str
    def best_item(self, strr, strr2, strr3):
        '''
        Determines the 'best product' based on the users filter preferences

        Parameters:
        strr: the category the user wants sorted
        strr2: Whether the user wants the list to be sorted from low to high or high to low
        strr3: The number of items the user wants to see

        Returns:
        The best item if the user answered the questions correctly
        '''
        try:
            strr3 = int(strr3)
            if strr == 'price':
                return self.best_item_helper(strr2, 1)
            if strr == 'reviews':
                return self.best_item_helper(strr2, 2)
            if strr == 'num of reviews':
                return self.best_item_helper(strr2, 3)
            if strr == 'validity score':
                return self.best_item_helper(strr2, 5)
        except:
            return 'invalid string entered'
        

        

#gets user input
item = input("Enter the item you would like: ")
print(item)
item = item.replace(' ', '+')

strr = input("\nHow would you like the list sorted \nPlease type in one of the following: price, reviews, num of reviews, validity score: ")

strr2 = input("\nWould you like the list sorted from low to high or high to low? \nType in either l to h or h to l: ")

strr3 = input("\nHow many items from each list would you like to see? Enter a number: ")

amazon_list = amazon.amazon_tings(item)

walmart_list = walmart.walmart_tings(item)

ebay_list = ebay.ebay_tings(item)

item_list = Item(amazon_list, walmart_list, ebay_list)

amazon_list, walmart_list, ebay_list = item_list.sort_item_list(strr, strr2, strr3)

best_item_list = item_list.best_item(strr, strr2, strr3)

print('Amazon List: ')
print(amazon_list)
print('Walmart List: ')
print(walmart_list)
print('Ebay List: ')
print(ebay_list)

print('The best item based on your filter preference is: ')
print(best_item_list)



