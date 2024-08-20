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


    def sort_high_low(self, general_list, order, i):
        '''
        Sorts the lists based on if the user wants it sorted from low to high or high to low

        Parameters:
        general_list: The general list
        order: The string on if the user wants the list sorted from high to low or low to high
        i: The element of the list the user wants sorted

        Returns:
        The sorted list
        '''
        j=0
        while j < len(general_list):
            if len(general_list[j]) < 6:
                del general_list[j]
            else:
                j+=1
        if order == 'l to h':
            general_list = sorted(general_list,key=lambda l:l[i])
            return general_list
        elif order == 'h to l':
            general_list = sorted(general_list,key=lambda l:l[i], reverse=True)
            return general_list
        else:
            return 'invalid option'


    def sort_item_list(self, sort_by, order):
        '''
        Utilizes the previous two functions to sort the 3 lists and display the sorted lists with the number of items the user wants to be displayed

        Parameters:
        sort_by: the category the user wants sorted
        order: Whether the user wants the list sorted from low to high or high to low
        num_items: The number of items the user wants to see

        Returns:
        The three sorted lists
        '''
        if sort_by == 'price':
            self.amazon_list = self.sort_high_low(self.amazon_list, order, 1)
            self.walmart_list = self.sort_high_low(self.walmart_list, order, 1)
            self.ebay_list = self.sort_high_low(self.ebay_list, order, 1)
        if sort_by == 'reviews':
            self.amazon_list = self.sort_high_low(self.amazon_list, order, 2)
            self.walmart_list = self.sort_high_low(self.walmart_list, order, 2)
            self.ebay_list = self.sort_high_low(self.ebay_list, order, 2)
        if sort_by == 'num of reviews':
            self.amazon_list = self.sort_high_low(self.amazon_list, order, 3)
            self.walmart_list = self.sort_high_low(self.walmart_list, order, 3)
            self.ebay_list = self.sort_high_low(self.ebay_list, order, 3)
        if sort_by == 'validity score':
            self.amazon_list = self.sort_high_low(self.amazon_list, order, 5)
            self.walmart_list = self.sort_high_low(self.walmart_list, order, 5)
            self.ebay_list = self.sort_high_low(self.ebay_list, order, 5)
        
        return self.amazon_list, self.walmart_list, self.ebay_list
    
    def num_items_shown(self, sort_by, order, num_items):
        '''
        Takes the sorted list and only displays the number of items the user wants to see

        Parameters:
        sort_by: the category the user wants sorted
        order: Whether the user wants the list sorted from low to high or high to low
        num_items: The number of items the user wants to see

        Returns:
        the 3 lists with the limited number of items
        '''
        self.amazon_list, self.walmart_list, self.ebay_list = self.sort_item_list(sort_by, order)
        i = 0
        short_a_list = list()
        short_w_list = list()
        short_e_list = list()
        while i < num_items:
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


    def best_item_helper(self, sort_by, order, i):
        '''
        Helper function to determine the 'best product' based on the users filter preferences

        Parameters:
        sort_by: the category the user wants sorted
        num_items: The number of items the user wants to see
        i: the category the user wants sorted

        Returns:
        The information of the best product
        '''
        self.amazon_list, self.walmart_list, self.ebay_list = self.sort_item_list(sort_by, order)
        return_str = ''
        return_str_list = list()
        if order == 'h to l':
            if self.amazon_list[0][i] > self.ebay_list[0][i] and self.amazon_list[0][i] > self.walmart_list[0][i]:
                return_str = ['Name: ' + str(self.amazon_list[0][0]), 'Price: ' + str(self.amazon_list[0][1]), 'Reviews: ' + str(self.amazon_list[0][2]), 'Number of Reviews: ' + str(self.amazon_list[0][3]),'Validity Score: ' + str(self.amazon_list[0][5]),'Link: ' + str(self.amazon_list[0][4])]
                return_str_list = [return_str]
                return return_str_list
            elif self.ebay_list[0][i] > self.amazon_list[0][i] and self.ebay_list[0][i] > self.walmart_list[0][i]:
                return_str2 = ['Name: ' + str(self.ebay_list[0][0]), 'Price: ' + str(self.ebay_list[0][1]), 'Reviews: ' + str(self.ebay_list[0][2]), 'Number of Reviews: ' + str(self.ebay_list[0][3]), 'Validity Score: ' + str(self.ebay_list[0][5]), 'Link: ' + str(self.ebay_list[0][4])]
                return_str_list = [return_str2]
                return return_str_list
            elif self.walmart_list[0][i] > self.amazon_list[0][i] and self.walmart_list[0][i] > self.ebay_list[0][i]:
                return_str3 = ['Name: ' + str(self.walmart_list[0][0]), 'Price: ' + str(self.walmart_list[0][1]), 'Reviews: ' + str(self.walmart_list[0][2]), 'Number of Reviews: ' + str(self.walmart_list[0][3]), 'Validity Score: ' + str(self.walmart_list[0][5]), 'Link: ' + str(self.walmart_list[0][4])]
                return_str_list = [return_str3]
                return return_str_list
            elif self.amazon_list[0][i] == self.ebay_list[0][i] and (self.amazon_list[0][i] > self.walmart_list[0][i] or self.ebay_list[0][i] > self.walmart_list[0][i]):
                return_str = ['Name: ' + str(self.amazon_list[0][0]), 'Price: ' + str(self.amazon_list[0][1]), 'Reviews: ' + str(self.amazon_list[0][2]), 'Number of Reviews: ' + str(self.amazon_list[0][3]),'Validity Score: ' + str(self.amazon_list[0][5]),'Link: ' + str(self.amazon_list[0][4])]
                return_str2 = ['Name: ' + str(self.ebay_list[0][0]), 'Price: ' + str(self.ebay_list[0][1]), 'Reviews: ' + str(self.ebay_list[0][2]), 'Number of Reviews: ' + str(self.ebay_list[0][3]), 'Validity Score: ' + str(self.ebay_list[0][5]), 'Link: ' + str(self.ebay_list[0][4])]
                return_str_list = [return_str,return_str2]
                return return_str_list
            elif self.amazon_list[0][i] == self.walmart_list[0][i] and (self.amazon_list[0][i] > self.ebay_list[0][i] or self.walmart_list[0][i] > self.ebay_list[0][i]):
                return_str = ['Name: ' + str(self.amazon_list[0][0]), 'Price: ' + str(self.amazon_list[0][1]), 'Reviews: ' + str(self.amazon_list[0][2]), 'Number of Reviews: ' + str(self.amazon_list[0][3]),'Validity Score: ' + str(self.amazon_list[0][5]),'Link: ' + str(self.amazon_list[0][4])]
                return_str3 = ['Name: ' + str(self.walmart_list[0][0]), 'Price: ' + str(self.walmart_list[0][1]), 'Reviews: ' + str(self.walmart_list[0][2]), 'Number of Reviews: ' + str(self.walmart_list[0][3]), 'Validity Score: ' + str(self.walmart_list[0][5]), 'Link: ' + str(self.walmart_list[0][4])]
                return_str_list = [return_str,return_str3]
                return return_str_list
            elif self.walmart_list[0][i] == self.ebay_list[0][i] and (self.walmart_list[0][i] > self.amazon_list[0][i] or self.ebay_list[0][i] > self.amazon_list[0][i]):
                return_str2 = ['Name: ' + str(self.ebay_list[0][0]), 'Price: ' + str(self.ebay_list[0][1]), 'Reviews: ' + str(self.ebay_list[0][2]), 'Number of Reviews: ' + str(self.ebay_list[0][3]), 'Validity Score: ' + str(self.ebay_list[0][5]), 'Link: ' + str(self.ebay_list[0][4])]
                return_str3 = ['Name: ' + str(self.walmart_list[0][0]), 'Price: ' + str(self.walmart_list[0][1]), 'Reviews: ' + str(self.walmart_list[0][2]), 'Number of Reviews: ' + str(self.walmart_list[0][3]), 'Validity Score: ' + str(self.walmart_list[0][5]), 'Link: ' + str(self.walmart_list[0][4])]
                return_str_list = [return_str2,return_str3]
                return return_str_list
            elif self.amazon_list[0][i] == self.ebay_list[0][i] and self.amazon_list[0][i] == self.walmart_list[0][i]:
                return_str = ['Name: ' + str(self.amazon_list[0][0]), 'Price: ' + str(self.amazon_list[0][1]), 'Reviews: ' + str(self.amazon_list[0][2]), 'Number of Reviews: ' + str(self.amazon_list[0][3]),'Validity Score: ' + str(self.amazon_list[0][5]),'Link: ' + str(self.amazon_list[0][4])]
                return_str2 = ['Name: ' + str(self.ebay_list[0][0]), 'Price: ' + str(self.ebay_list[0][1]), 'Reviews: ' + str(self.ebay_list[0][2]), 'Number of Reviews: ' + str(self.ebay_list[0][3]), 'Validity Score: ' + str(self.ebay_list[0][5]), 'Link: ' + str(self.ebay_list[0][4])]
                return_str3 = ['Name: ' + str(self.walmart_list[0][0]), 'Price: ' + str(self.walmart_list[0][1]), 'Reviews: ' + str(self.walmart_list[0][2]), 'Number of Reviews: ' + str(self.walmart_list[0][3]), 'Validity Score: ' + str(self.walmart_list[0][5]), 'Link: ' + str(self.walmart_list[0][4])]
                return_str_list = [return_str,return_str2,return_str3]
                return return_str_list
            
        elif order == 'l to h':
            if self.amazon_list[0][i] < self.ebay_list[0][i] and self.amazon_list[0][i] < self.walmart_list[0][i]:
                return_str = ['Name: ' + str(self.amazon_list[0][0]), 'Price: ' + str(self.amazon_list[0][1]), 'Reviews: ' + str(self.amazon_list[0][2]), 'Number of Reviews: ' + str(self.amazon_list[0][3]),'Validity Score: ' + str(self.amazon_list[0][5]),'Link: ' + str(self.amazon_list[0][4])]
                return_str_list = [return_str]
                return return_str_list
            elif self.ebay_list[0][i] < self.amazon_list[0][i] and self.ebay_list[0][i] < self.walmart_list[0][i]:
                return_str2 = ['Name: ' + str(self.ebay_list[0][0]), 'Price: ' + str(self.ebay_list[0][1]), 'Reviews: ' + str(self.ebay_list[0][2]), 'Number of Reviews: ' + str(self.ebay_list[0][3]), 'Validity Score: ' + str(self.ebay_list[0][5]), 'Link: ' + str(self.ebay_list[0][4])]
                return_str_list = [return_str2]
                return return_str_list
            elif self.walmart_list[0][i] < self.amazon_list[0][i] and self.walmart_list[0][i] < self.ebay_list[0][i]:
                return_str3 = ['Name: ' + str(self.walmart_list[0][0]), 'Price: ' + str(self.walmart_list[0][1]), 'Reviews: ' + str(self.walmart_list[0][2]), 'Number of Reviews: ' + str(self.walmart_list[0][3]), 'Validity Score: ' + str(self.walmart_list[0][5]), 'Link: ' + str(self.walmart_list[0][4])]
                return_str_list = [return_str3]
                return return_str_list
            elif self.amazon_list[0][i] == self.ebay_list[0][i] and (self.amazon_list[0][i] < self.walmart_list[0][i] or self.ebay_list[0][i] < self.walmart_list[0][i]):
                return_str = ['Name: ' + str(self.amazon_list[0][0]), 'Price: ' + str(self.amazon_list[0][1]), 'Reviews: ' + str(self.amazon_list[0][2]), 'Number of Reviews: ' + str(self.amazon_list[0][3]),'Validity Score: ' + str(self.amazon_list[0][5]),'Link: ' + str(self.amazon_list[0][4])]
                return_str2 = ['Name: ' + str(self.ebay_list[0][0]), 'Price: ' + str(self.ebay_list[0][1]), 'Reviews: ' + str(self.ebay_list[0][2]), 'Number of Reviews: ' + str(self.ebay_list[0][3]), 'Validity Score: ' + str(self.ebay_list[0][5]), 'Link: ' + str(self.ebay_list[0][4])]
                return_str_list = [return_str , return_str2]
                return return_str_list
            elif self.amazon_list[0][i] == self.walmart_list[0][i] and (self.amazon_list[0][i] < self.ebay_list[0][i] or self.walmart_list[0][i] < self.ebay_list[0][i]):
                return_str = ['Name: ' + str(self.amazon_list[0][0]), 'Price: ' + str(self.amazon_list[0][1]), 'Reviews: ' + str(self.amazon_list[0][2]), 'Number of Reviews: ' + str(self.amazon_list[0][3]),'Validity Score: ' + str(self.amazon_list[0][5]),'Link: ' + str(self.amazon_list[0][4])]
                return_str3 = ['Name: ' + str(self.walmart_list[0][0]), 'Price: ' + str(self.walmart_list[0][1]), 'Reviews: ' + str(self.walmart_list[0][2]), 'Number of Reviews: ' + str(self.walmart_list[0][3]), 'Validity Score: ' + str(self.walmart_list[0][5]), 'Link: ' + str(self.walmart_list[0][4])]
                return_str_list = [return_str , return_str3]
                return return_str_list
            elif self.walmart_list[0][i] == self.ebay_list[0][i] and (self.walmart_list[0][i] < self.amazon_list[0][i] or self.ebay_list[0][i] < self.amazon_list[0][i]):
                return_str2 = ['Name: ' + str(self.ebay_list[0][0]), 'Price: ' + str(self.ebay_list[0][1]), 'Reviews: ' + str(self.ebay_list[0][2]), 'Number of Reviews: ' + str(self.ebay_list[0][3]), 'Validity Score: ' + str(self.ebay_list[0][5]), 'Link: ' + str(self.ebay_list[0][4])]
                return_str3 = ['Name: ' + str(self.walmart_list[0][0]), 'Price: ' + str(self.walmart_list[0][1]), 'Reviews: ' + str(self.walmart_list[0][2]), 'Number of Reviews: ' + str(self.walmart_list[0][3]), 'Validity Score: ' + str(self.walmart_list[0][5]), 'Link: ' + str(self.walmart_list[0][4])]
                return_str_list = [return_str2 , return_str3]
                return return_str_list
            elif self.amazon_list[0][i] == self.ebay_list[0][i] and self.amazon_list[0][i] == self.walmart_list[0][i]:
                return_str = ['Name: ' + str(self.amazon_list[0][0]), 'Price: ' + str(self.amazon_list[0][1]), 'Reviews: ' + str(self.amazon_list[0][2]), 'Number of Reviews: ' + str(self.amazon_list[0][3]),'Validity Score: ' + str(self.amazon_list[0][5]),'Link: ' + str(self.amazon_list[0][4])]
                return_str2 = ['Name: ' + str(self.ebay_list[0][0]), 'Price: ' + str(self.ebay_list[0][1]), 'Reviews: ' + str(self.ebay_list[0][2]), 'Number of Reviews: ' + str(self.ebay_list[0][3]), 'Validity Score: ' + str(self.ebay_list[0][5]), 'Link: ' + str(self.ebay_list[0][4])]
                return_str3 = ['Name: ' + str(self.walmart_list[0][0]), 'Price: ' + str(self.walmart_list[0][1]), 'Reviews: ' + str(self.walmart_list[0][2]), 'Number of Reviews: ' + str(self.walmart_list[0][3]), 'Validity Score: ' + str(self.walmart_list[0][5]), 'Link: ' + str(self.walmart_list[0][4])]
                return_str_list = [return_str,return_str2,return_str3]
                return return_str_list
    
    
    def best_item(self, sort_by, order):
        '''
        Determines the 'best product' based on the users filter preferences

        Parameters:
        sort_by: the category the user wants sorted
        order: Whether the user wants the list to be sorted from low to high or high to low

        Returns:
        The best item if the user answered the questions correctly
        '''
        try:
            if sort_by == 'price':
                return self.best_item_helper(sort_by, order, 1)
            if sort_by == 'reviews':
                return self.best_item_helper(sort_by, order, 2)
            if sort_by == 'num of reviews':
                return self.best_item_helper(sort_by, order, 3)
            if sort_by == 'validity score':
                return self.best_item_helper(sort_by, order, 5)
        except:
            return 'invalid string entered'
    


def product_data(item):
    amazon_list = amazon.amazon_tings(item)
    walmart_list = walmart.walmart_tings(item)
    ebay_list = ebay.ebay_tings(item)
    return amazon_list, walmart_list, ebay_list

        
def main():
    #gets user input
    item = input("Enter the item you would like: ").replace(' ', '+')
    sort_by = input("\nHow would you like the list sorted \nPlease type in one of the following: price, reviews, num of reviews, validity score: ")
    order = input("\nWould you like the list sorted from low to high or high to low? \nType in either l to h or h to l: ")
    num_items = int(input("\nHow many items from each list would you like to see? Enter a number: "))

    amazon_list, walmart_list, ebay_list = product_data(item)

    #for testing
    # amazon_list = [['The Legend of Zelda: Breath of the Wild - US Version  ESRB Rating: Rating Pending | Mar 3, 2017 | by Nintend', 49.0, 4.8, 52773, 'https://www.amazon.com//Legend-Zelda-Breath-Wild-Nintendo-Switch/dp/B01MS6MO77/ref=sr_1_3?dib=eyJ2IjoiMSJ9.Lc1Up3dodvUnEPr1XhN8ikshBTDud5L2PUk8w_3b5CLIMMN3znc2xzOSy8bUWVtlLE0vUx2T2FZGFl6NLHZt5LQZp6j1yg-Nue--K6haxB3Cprmqpu2uZfUHLVxnjjQIFypBvh047275seXCAPe8BIgtYArlpP9EYgn3DBS7jsZgkLxUbzcLtB5vkcd8HYBQ0mPQAS98K0rrSIWj-KdVO5KwDDriLWKkrY0cj24vL1c.ZikFkEoK-vCkAbgGAGLnfNcLpqPYVwO7pqLgCwIoV_o&dib_tag=se&keywords=the+legend+of+zelda&qid=1724098383&sr=8-3', 253310.4], ['PDP Gaming AIRLITE Wired Stereo Headset with Noise-Cancelling Mic for Nintendo Switch/Switch Lite/Switch OLED (Legend of Zelda Hyrule Blue)  Aug 18, 2023 | by PD', 14.99, 4.5, 28929, 'https://www.amazon.com//Gaming-AIRLITE-Stereo-Headset-Noise-Cancelling-Nintendo/dp/B0BXB7D6W4/ref=sr_1_62?dib=eyJ2IjoiMSJ9.uKyqc18-eBuZCqYRjlAQOldo_AptVMT7MfYrkCYsMy_LVV2hTyi6lv34vXLdmdXqQJWLenXnA9X25e7AYZ1TYnxXqVxZyt1Rf8vVq1yRVTxla4ZCm6fqe_vQNSwKY4MIMQaRiccBA2I8DITixTo-RTdMsImWUvU3rfVX4imurUeu2Vz_tyQIDFNhn6eTDOKvxlrBjPV86M8Y7FufUnK6p9uKnDkGBsxE_DPtL0gQp-g.cGtoZkG1BBFh6CIsok8E8qnFwb_LXIouPJibXQwBY6I&dib_tag=se&keywords=the+legend+of+zelda&qid=1724098387&sr=8-62', 130180.5], ["The Legend of Zelda: Link's Awakening - Nintendo Switch  ESRB Rating: Everyone | Sep 20, 2019 | by Nintend", 53.99, 4.8, 24247, 'https://www.amazon.com//Legend-Zelda-Links-Awakening-Nintendo-Switch/dp/B07SG15148/ref=sr_1_34?dib=eyJ2IjoiMSJ9.29mtBdUUXxedEjl8KFO83UwVkQd0ZeRR2pVFbonSW-sadJpG368FDhiRzFLlkUU_-FSYAU76tyGwyjfNGHPKFGAGTiojShz8giyWxjZNkba673Fk-fyy-42HEJuANPjlWkxMdorjHvtRD6v1rjo7LAJ1EjhOkw2rG4H3sxIgkzCMoKdmy1H26MUVIO4Ismw_rBzcAJ-TexbjpRDTl7gcvTVdyKHI9ouyCbO5mb8EoZ4.bJFaA72FDAVTbbSslCYfJ57uwbUD5EYhlfyOp6zDtTo&dib_tag=se&keywords=the+legend+of+zelda&qid=1724098384&sr=8-34', 116385.59999999999], ['Nintendo Switch Compact Playstand (The Legend of Zelda) by HORI - Officially Licensed by Nintendo  May 22, 2018 | by HOR', 12.99, 4.7, 24017, 'https://www.amazon.com//HORI-Compact-PlayStand-Officially-Licensed-Nintendo/dp/B01A9UATJC/ref=sr_1_118?dib=eyJ2IjoiMSJ9.GqsuMk34Dkl6FRBTixrQXPVvbYHxbj7VZmqU-Y72kqCF-kdr4hYoltTLx8aMJS9XY78Twx8O1IvhTamyInNhIUlTMBy4rbYqvBepojDts5EUmTEtDQEJ7kmzXZAHmMvVo6_JEb9mxDROBOvNF1ACc6uCApDnTMSgeMq8HUu1iH1p5BPux9OwHJ3fZqWIZz7klEQRBIehka9D9ianAT-HoXU5CDroasD2eVKZO1zfQHs.656MQvj8cmI6CbkxNAcVjqfpcMG0UrE4aoOWdcm1sXY&dib_tag=se&keywords=the+legend+of+zelda&qid=1724098393&sr=8-118', 112879.90000000001], ['The Legend of Zelda: Tears of the Kingdom - Nintendo Switch (US Version)  ESRB Rating: Rating Pending | May 12, 2023 | by Nintend', 56.95, 4.9, 21527, 'https://www.amazon.com//Legend-Zelda-Breath-Wild-Nintendo-Switch/dp/B097B2YWFX/ref=sr_1_2?dib=eyJ2IjoiMSJ9.Lc1Up3dodvUnEPr1XhN8ikshBTDud5L2PUk8w_3b5CLIMMN3znc2xzOSy8bUWVtlLE0vUx2T2FZGFl6NLHZt5LQZp6j1yg-Nue--K6haxB3Cprmqpu2uZfUHLVxnjjQIFypBvh047275seXCAPe8BIgtYArlpP9EYgn3DBS7jsZgkLxUbzcLtB5vkcd8HYBQ0mPQAS98K0rrSIWj-KdVO5KwDDriLWKkrY0cj24vL1c.ZikFkEoK-vCkAbgGAGLnfNcLpqPYVwO7pqLgCwIoV_o&dib_tag=se&keywords=the+legend+of+zelda&qid=1724098383&sr=8-2', 105482.3], ['The Legend of Zelda: Breath of the Wild (Nintendo Switch) (European Version)  ESRB Rating: Everyone | Mar 3, 2017 | by Nintend', 46.97, 4.8, 18118, 'https://www.amazon.com//Legend-Zelda-Breath-Wild-switch-Nintendo/dp/B01N1083WZ/ref=sr_1_51?dib=eyJ2IjoiMSJ9.uKyqc18-eBuZCqYRjlAQOldo_AptVMT7MfYrkCYsMy_LVV2hTyi6lv34vXLdmdXqQJWLenXnA9X25e7AYZ1TYnxXqVxZyt1Rf8vVq1yRVTxla4ZCm6fqe_vQNSwKY4MIMQaRiccBA2I8DITixTo-RTdMsImWUvU3rfVX4imurUeu2Vz_tyQIDFNhn6eTDOKvxlrBjPV86M8Y7FufUnK6p9uKnDkGBsxE_DPtL0gQp-g.cGtoZkG1BBFh6CIsok8E8qnFwb_LXIouPJibXQwBY6I&dib_tag=se&keywords=the+legend+of+zelda&qid=1724098387&sr=8-51', 86966.4], ['Hyrule Warriors: Age of Calamity - Nintendo Switch  ESRB Rating: Teen | Nov 20, 2020 | by Nintend', 53.59, 4.7, 17777, 'https://www.amazon.com//Hyrule-Warriors-Age-Calamity-Nintendo-Switch/dp/B08HP4K7KC/ref=sr_1_184?dib=eyJ2IjoiMSJ9.7LpLsyTMrx2d3_obj4FrKJ05qFf9ZGIUfXms-U9hM6miD0lzUgF5OkBOOf_lsAB2qirqh-RRnaTa8KKnxSq7YoO27pV_8zev00SY7wjIQr46BqrVJ5dYHcrEGAM2Zj0ups5rci6vbZsnutgtWxzgA2X_2vofKZ4YaWt-nzLun8NYpma0Qx-EmqUJUmAKpOredSrIBmMvD6bBUp25-nY5gYEcG3Wz1byOcFuz7_pyGnU.3zV-XyWYRDW2hpaSJ9WTmVEuFTDTh7UP_W0l0bxgPyM&dib_tag=se&keywords=the+legend+of+zelda&qid=1724098398&sr=8-184', 83551.90000000001], ['BumkinsSleeved Bib for Girl or Boy, Baby and Toddler for 6-24 Mos, Essential Must Have for Eating, Feeding, Baby Led Weaning Supplies, Long Sleeve Mess Saving Food Catcher, Nintendo Legend of Zelda ', 12.95, 4.7, 17615, 'https://www.amazon.com//Bumkins-Nintendo-Waterproof-Washable-Resistant/dp/B0759PS4NK/ref=sr_1_182?dib=eyJ2IjoiMSJ9.7LpLsyTMrx2d3_obj4FrKJ05qFf9ZGIUfXms-U9hM6miD0lzUgF5OkBOOf_lsAB2qirqh-RRnaTa8KKnxSq7YoO27pV_8zev00SY7wjIQr46BqrVJ5dYHcrEGAM2Zj0ups5rci6vbZsnutgtWxzgA2X_2vofKZ4YaWt-nzLun8NYpma0Qx-EmqUJUmAKpOredSrIBmMvD6bBUp25-nY5gYEcG3Wz1byOcFuz7_pyGnU.3zV-XyWYRDW2hpaSJ9WTmVEuFTDTh7UP_W0l0bxgPyM&dib_tag=se&keywords=the+legend+of+zelda&qid=1724098398&sr=8-182', 82790.5], ['The Legend of Zelda: Skyward Sword HD - Nintendo Switch  ESRB Rating: Everyone 10+ | Jul 16, 2021 | by Nintend', 0, 4.8, 12359, 'https://www.amazon.com//Legend-Zelda-Skyward-Sword-Nintendo-Switch/dp/B08WWFWRY6/ref=sr_1_84?dib=eyJ2IjoiMSJ9.Kwk-NRjR2wYBfN6hezt0wKMQGTgsBcNkHlV9sIVQPcNExYKO_p7biDgfMH_ZLDa6PJ6MyBsybhjSG-ifCVjFfuaUvAXZD0csFBsASFiJGEOccp6SPMwKFyoZkC8qqvFyQ88bX3WMglaAdRgpA1Z_1DhT3meLgCODok1HtTVjgpr-C2-E3rkU-NKSLevZCj-_0yUwgczH8JA3-Crvkazczwz18SqkvYUrIUThCpxZc3I.f-i23D4RiRc7QjLiTWah3o2CapJIAxGWtUCMsjAsZek&dib_tag=se&keywords=the+legend+of+zelda&qid=1724098389&sr=8-84', 59323.2], ['The Legend of Zelda: Skyward Sword HD - Nintendo Switch  ESRB Rating: Everyone 10+ | Jul 16, 2021 | by Nintend', 0, 4.8, 12359, 'https://www.amazon.com//Legend-Zelda-Skyward-Sword-Nintendo-Switch/dp/B08WWFWRY6/ref=sr_1_83?dib=eyJ2IjoiMSJ9.FckI-hVFhUwnA4BkLA4mYFILAuTcGOE7HQjFp8hPxb5oCdCqus8DDA_4nBczG3NbO4t9BiBj9yySKO5i012KPn5Sj_M4A5I7Gzzai0AauD_GRvDV6XPLDCfgYbH3vHSdM-9xOfdLWSauGAUa1Kv97ArXH7xaAeKOWQMDEJg_yjUn_vXWtJE7hBCIyEEpPsQ_upeF3ftUNbkyYl-cW0HWXgo84GfAFSfmXPNIq4ySyb8.uIjSAzP9tIV8hkJm0QivykqWC0bjxdc0mxaymdrwuYY&dib_tag=se&keywords=the+legend+of+zelda&qid=1724098390&sr=8-83', 59323.2], ['The Legend of Zelda: Breath of the Wild The Complete Official Guide: -Expanded Edition  by Piggyback  | Feb 13, 201', 22.26, 4.8, 11553, 'https://www.amazon.com//Legend-Zelda-Complete-Official-Expanded/dp/1911015486/ref=sr_1_9?dib=eyJ2IjoiMSJ9.Lc1Up3dodvUnEPr1XhN8ikshBTDud5L2PUk8w_3b5CLIMMN3znc2xzOSy8bUWVtlLE0vUx2T2FZGFl6NLHZt5LQZp6j1yg-Nue--K6haxB3Cprmqpu2uZfUHLVxnjjQIFypBvh047275seXCAPe8BIgtYArlpP9EYgn3DBS7jsZgkLxUbzcLtB5vkcd8HYBQ0mPQAS98K0rrSIWj-KdVO5KwDDriLWKkrY0cj24vL1c.ZikFkEoK-vCkAbgGAGLnfNcLpqPYVwO7pqLgCwIoV_o&dib_tag=se&keywords=the+legend+of+zelda&qid=1724098383&sr=8-9', 55454.4]]
    # walmart_list = [['The Legend of Zelda: Tears of the Kingdom - Nintendo Switch', 51.66, 4.8, 2582, 'https://www.walmart.com//ip/The-Legend-of-Zelda-Tears-of-the-Kingdom-Nintendo-Switch/1481578625?classType=VARIANT&athbdg=L1600&from=/search', 12393.6], ['The Legend of Zelda: Breath of the Wild - Nintendo Switch', 44.98, 4.7, 1755, 'https://www.walmart.com//ip/The-Legend-of-Zelda-Breath-of-the-Wild-Nintendo-Switch/55432568?classType=VARIANT&athbdg=L1600&from=/search', 8248.5], ["The Legend of Zelda: Link's Awakening, Nintendo Switch, [Physical], 110249", 53.99, 4.8, 603, 'https://www.walmart.com//ip/The-Legend-of-Zelda-Link-s-Awakening-Nintendo-Switch-Physical-110249/755653843?classType=VARIANT&athbdg=L1600&from=/search', 2894.4], ['The Legend of Zelda: Skyward Sword HD, Nintendo Switch [Physical], 045496597559', 0, 4.8, 369, 'https://www.walmart.com//ip/The-Legend-of-Zelda-Skyward-Sword-HD-Nintendo-Switch-Physical-045496597559/530817837?classType=REGULAR&athbdg=L1200&from=/search', 1771.2], ['The Legend of Zelda - Legendary Edition Box Set (Paperback)', 78.99, 4.3, 11, 'https://www.walmart.com//ip/The-Legend-of-Zelda-Legendary-Edition-Box-Set-Paperback-9781974718191/723440464?classType=REGULAR&athbdg=L1600&from=/search', 47.3], ['The Legend of Zelda: Twilight Princess Vol. 1', 12.44, 4.8, 8, 'https://www.walmart.com//ip/The-Legend-of-Zelda-Twilight-Princess-Vol-1-9781421593470/55311737?classType=VARIANT&from=/search', 38.4], ["The Legend of Zelda Link's Awakening Import Region Free, Nintendo Switch", 49.99, 4.0, 4, 'https://www.walmart.com//ip/The-Legend-of-Zelda-Link-s-Awakening-Import-Region-Free-Nintendo-Switch/434399817?classType=REGULAR&from=/search', 16.0], ['Bokoblin Amiibo The Legend Of Zelda BOTW Collection (Nintendo Switch/3DS/Wii U)', 18.87, 5.0, 1, 'https://www.walmart.com//ip/Bokoblin-Amiibo-The-Legend-Of-Zelda-BOTW-Collection-Nintendo-Switch-3DS-Wii-U/776052631?classType=REGULAR&from=/search', 5.0], ["N64 Game The Legend of Zelda: Majora's Mask for Nintendo 64 Cartridge / Box / Tray / PET (No Expansion pak and Manual) NTSC Version", 29.99, 0, 0, 'https://www.walmart.com//ip/N64-Game-The-Legend-of-Zelda-Majora-s-Mask-for-Nintendo-64-Cartridge-Box-Tray-PET-No-Expansion-pak-and-Manual-NTSC-Version/5702664633?classType=REGULAR&from=/search', 0]]
    # ebay_list = [['The Legend of Zelda: Breath of the Wild New Factory Sealed Wata Graded 9.8 A+', 182.5, 5.0, 1290, 'https://www.ebay.com/itm/156362095473?_nkw=the+legend+of+zelda&epid=8045279653&itmmeta=01J5P4C15N2G4GCBRX2EBNXK9Q&hash=item2467e83b71:g:GyEAAOSwqxdmwhE4&itmprp=enc%3AAQAJAAAA8HoV3kP08IDx%2BKZ9MfhVJKkViaJsscpGJtOw2a1hfEDACquhnLzqWIK33btJXuW8eKAEoPqCd2US8Rjc2baRxt9WcaORBUuqF9AOefPy5ptyh8ksYpGVn62eNsehFmzmtIP3EQ9nQzoU23TpmzjX2KvA8vGo8NwFW8Y575Mz3w4uE3Kk80PCledX6%2Fsf6NATKGm23%2FGqElKt4KtlUwzy7NvuFhRmLHvaNa8IbS0Zywlk5iCaWzORO1IjnMQU0GQjxFBuS1MTzCo4ZXHNC5NIRD6f9k%2Fzlcon9jUQSQ2aX2yYaUZ0z4aSDUDFZLB8JwoBOA%3D%3D%7Ctkp%3ABFBM9JKwxK1k', 6450.0], ['The Legend of Zelda: Breath of the Wild - Nintendo Switch Edition', 32.0, 5.0, 1290, 'https://www.ebay.com/itm/135200398389?_nkw=the+legend+of+zelda&epid=8045279653&itmmeta=01J5P4C15PBNKJZQV4GNGJ92R1&hash=item1f7a925c35:g:X0oAAOSwGqFmw1cD&itmprp=enc%3AAQAJAAAA0HoV3kP08IDx%2BKZ9MfhVJKnYmXiKUJKq%2BP%2FvAoPqf20Ni5PaRs9w%2BARCgCyM3FWrFyvE%2BhA2AglrwZhjgTLlizUZMI1inRJawUc0EvIg%2BQBRDR6vdVltMBI1WQrrZnVu4Htdp54nZ2e9Po%2B9eunsErg%2FzWNUFxaNfSICptds0HfVT%2FDi6cndOzWybqWAeWloLrdn3G203QEllDSYBxSVIniPwP2MnDj2WWrjZYrUI0svKYTjZrgv2TXFHgPXltSlU3IGeKWmMMBI%2Fg8M8SCCSsY%3D%7Ctkp%3ABk9SR_qSsMStZA', 6450.0], ['The Legend of Zelda: Breath of the Wild - Nintendo Switch', 31.95, 5.0, 1290, 'https://www.ebay.com/itm/266956837168?_nkw=the+legend+of+zelda&epid=8045279653&itmmeta=01J5P4E8ZC677Y6NFP0K7B3KK9&hash=item3e27de1130:g:rD0AAOSw9lVmw3qC&itmprp=enc%3AAQAJAAAA8HoV3kP08IDx%2BKZ9MfhVJKm6HtmB%2BO1Vo98KJG3XJCq%2BwC5XcLwEEyLym5UFc4--Zo7NW3JRKHGNRBDk0ERmdz2zV%2F1r%2BZkFtuk8Cdhe68ZZWQCkA6EcEaXHv9egNt4WrjQkC16KyKBlmY3TTS0arm8gQCSFifF4X88o92eLE%2Fbo3ncrKL1WUKLQIVY30vDsbj%2Bul%2BZmRU%2F7Zd4tgqaOgeihu5TQgsLIhiBMfRPbaX3eihz6HXormUioWhJgbzqfJFyrZyGgW7nVL2ZZy5X%2BAazmE7o3GSjgkyGCcO4aKQY%2B5JU6ok9ntXTTYmmcBdbLaQ%3D%3D%7Ctkp%3ABk9SR-KPucStZA', 6450.0], ['The Legend of Zelda: Breath of the Wild - Nintendo Switch', 29.99, 5.0, 1290, 'https://www.ebay.com/itm/395605824354?_nkw=the+legend+of+zelda&epid=8045279653&itmmeta=01J5P4E8ZDPTFQ4V41RQJ78JPH&hash=item5c1bf1d362:g:j3UAAOSwguVmw6U6&itmprp=enc%3AAQAJAAAA8HoV3kP08IDx%2BKZ9MfhVJKncHI2CuN%2Bj2WtgLXTmVaqO8rj1Jl60u7e5J5nhGz8XM0Jb8pS%2B6IevEh6EvDIJXjBKtMu3vRimgIrrBwki4nuhc%2BJuXRA72qsBKoZe%2BB--KZ%2FWwo85%2Bp9j87pjay4rCOuF8PuGFdgW5teqGMieIe0pmoq6iMC%2FWnYUhDxN%2FRR6SiZ%2BO%2BLX8nf1YQOwV90TynMTDUmpTiJh6g8If6qv8mgZpa5VaTiN7w5xwXTRv4iPrqWJW%2ByOsPkYobBPCbJm5lld3lLdDYSXCQdTqr0wx0P1ZAzUgutYHxYEoEvVZ%2Fh%2BWg%3D%3D%7Ctkp%3ABk9SR-aPucStZA', 6450.0], ['The Legend of Zelda: Breath of the Wild - Nintendo Switch', 31.95, 5.0, 1290, 'https://www.ebay.com/itm/266956838284?_nkw=the+legend+of+zelda&epid=8045279653&itmmeta=01J5P4E8ZEYSDZSHRBBDCN1QHS&hash=item3e27de158c:g:tKQAAOSwBRxmw32C&itmprp=enc%3AAQAJAAAA0HoV3kP08IDx%2BKZ9MfhVJKm0qH3B4xEb1vUmSABDMYtVmufSlfrhbc0XttBkbpODgD0UbOX%2FwETL1RFvgHN3H27o%2BjMOJUaBDe6%2FcceiBQm4giswF7GSotFUyYCb%2F0IsbfLHqBcT5S31IS03Wr2Uee0R4pOyQ7jfxcWLN74o3mVpjoYz%2BLkxAGozUUyuHjnZYaQ3fYIBwMVaFBvJcNgFD2dexFNNRh0L5qYvZ4gnq635lrrhW7gXvEnzkDJnOwHssJ4CbX7pvwx7KculHliqF5w%3D%7Ctkp%3ABk9SR-qPucStZA', 6450.0], ['The Legend of Zelda: Breath of the Wild - Nintendo Switch', 31.95, 5.0, 1290, 'https://www.ebay.com/itm/266956837168?_nkw=the+legend+of+zelda&epid=8045279653&itmmeta=01J5P4G1VVJYB5X00P2EN9RZDA&hash=item3e27de1130:g:rD0AAOSw9lVmw3qC&itmprp=enc%3AAQAJAAAA8HoV3kP08IDx%2BKZ9MfhVJKm6HtmB%2BO1Vo98KJG3XJCq%2BwC5XcLwEEyLym5UFc4--Zo7NW3JRKHGNRBDk0ERmdz2zV%2F1r%2BZkFtuk8Cdhe68ZZWQCkA6EcEaXHv9egNt4WrjQkC16KyKBlmY3TTS0arm98gERTTPiMRgARjllh5ExHx%2Bxxe2oIJTf%2B%2FWO45ngyDqkbzGNJWvtVJCfjcAXOhRb2QCpZCR38%2BuwwWzRoKlCMhYfsalLiC8wn9S6MfeOIjaGZY%2FXbs32BFgvACbSjJHtWxoOrG4eAF3eofEJiirUvbofU0PuR20Z3HmOVAtMTvg%3D%3D%7Ctkp%3ABk9SR4KewMStZA', 6450.0], ['The Legend of Zelda: Breath of the Wild - Nintendo Switch', 50.0, 5.0, 1290, 'https://www.ebay.com/itm/166922394212?_nkw=the+legend+of+zelda&epid=8045279653&itmmeta=01J5P4HT3F2FS9E4ZNSCGE0HPQ&hash=item26dd599a64:g:LPwAAOSw3aNmv45V&itmprp=enc%3AAQAJAAAA8HoV3kP08IDx%2BKZ9MfhVJKmCb5eWqcValHL0l7fVJr%2FZIVDIweJxzVAffktmbspXwmvAYtojHQU9cHszWvOtM6QJ1uv5fNxd19henbTVjAilmz8XPQQ9EhjjnhHB96BnIdOP4PwfX2pk26pT7PsCac2Sfm267AqMAa4fPY2b%2Bcj0Si9WqTKB0T1MiK5Fv8cupE7daH9PQUDlQ0V4KkY3LWWozdfVpjluQQrJpW44422dUFg52fiIh82uWjVO1Sbc6PhGxP2qncAEPix63Dw15K5rsThWr2iV0Hmk3NCc5%2Bub%2Bc6DgpEnpxkTl5LVTZpn3A%3D%3D%7Ctkp%3ABFBM5qHHxK1k', 6450.0], ['The Legend of Zelda: Breath of the Wild - Nintendo Switch', 30.0, 5.0, 1290, 'https://www.ebay.com/itm/266950219302?_nkw=the+legend+of+zelda&epid=8045279653&itmmeta=01J5P4HT3G1T8YM08XANF3AY85&hash=item3e27791626:g:oKAAAOSwsd9mslbn&itmprp=enc%3AAQAJAAAA8HoV3kP08IDx%2BKZ9MfhVJKk1H7qHAGthkz%2BFmK3M%2F846V5gsv3NlzFIxpZ9N15FaoJRHrilIN50nh0rXeiV2yxDmaW5Jhsaaw%2FicoQg0dJ12O5bty8VCHs9%2BsNBi4u633BmmqTwLzdd8zXpddYrS8nyOkVn1uNMHe6L2drztk377TzzgaTnKucO7YSzcRxXS1nMgjLsuChWvRXMk6zBfba4GZAcO%2FVRdDoHvcl%2BFwhdtutc5zjSBOgWRjd9PVVDjpXeunS%2F471szj4kzoLcryvmD8RBe6VXUOftoQc8vDYkNw2UtFc5dCd49kETl1P01mw%3D%3D%7Ctkp%3ABFBM6KHHxK1k', 6450.0], ['The Legend of Zelda: Breath of the Wild - Nintendo Switch', 31.95, 5.0, 1290, 'https://www.ebay.com/itm/266956838284?_nkw=the+legend+of+zelda&epid=8045279653&itmmeta=01J5P4KJ6N38QX3XYDYB4VRBWR&hash=item3e27de158c:g:tKQAAOSwBRxmw32C&itmprp=enc%3AAQAJAAAA8HoV3kP08IDx%2BKZ9MfhVJKlFiEf%2FN6sCwmypeqoK5e7pfkved%2BMnZKU9l8Ha2UwdAgpAj2%2Fj5WTZiNd9X3lkPYZRcHqooq6Vq3aZet%2F7rsCsWPkgF6mX5WU2%2B4nyk6mBd72Z8HfLH1BrsY6wcj%2FfoJjcd6RyBH8ZDhqbo0YBK%2FiucXzaAyl%2BUDhSExqJMe6dLeOEhsNIzAgpNoDVJryh%2B43IGgRc8kDrrmcP%2FTeufOIqwW4ggBDfsYLMMwY%2BehMAU%2BCKgZ61OmEP%2FAZR3a9e5HdunQh1KjQXFJyjqO4yTxYgi1RetNE2KJmaoERuM5yWWg%3D%3D%7Ctkp%3ABk9SR7ijzsStZA', 6450.0], ['The Legend of Zelda: Breath of the Wild - Nintendo Switch - Factory Sealed New', 29.99, 5.0, 1290, 'https://www.ebay.com/itm/276601057657?_nkw=the+legend+of+zelda&epid=8045279653&itmmeta=01J5P4RWJRAS2756AH1FPM8ATF&hash=item4066b53179:g:SdMAAOSw~GJml65Y&itmprp=enc%3AAQAJAAAA8HoV3kP08IDx%2BKZ9MfhVJKka%2F6bpiKi024%2BL6VN5rfDid8PsH5kCDHX5Q6rhVA98rtUuTho4%2B8CHDfZ%2BhkGVnc%2F24DX1Q%2F0wnt3zukm5%2FfglaFcSij0VLcblYAxvoIKetc8JlB7tkP%2Fd3pL4r2ZaU23NqZd9cMZeYlO0rkQrH7p965XMg4XyIrWN7VGBQh8JsxW4T4ZfMr5EugFAiCBWhQ7RwBCImvMXbGUVd0d77R9B9Q0l%2Fuue02FWvuOHWdbGow%2BYPxSAqXqzPsWc3SlIWeM7FaVgguJq36ntMXE54zDvrwDQcuYgcmij8dM5pGssDA%3D%3D%7Ctkp%3ABk9SR8bJ48StZA', 6450.0], ['The Legend of Zelda: Breath of the Wild - Nintendo Switch - Mint in Case', 30.0, 5.0, 1290, 'https://www.ebay.com/itm/135200144345?_nkw=the+legend+of+zelda&epid=8045279653&itmmeta=01J5P4TN51KHNZBMMPGCNV3E8X&hash=item1f7a8e7bd9:g:Mf0AAOSwP75mwytD&itmprp=enc%3AAQAJAAAA8HoV3kP08IDx%2BKZ9MfhVJKkoxHt%2FSmdDFN5c9R7505ejmOLP37IBeyGfblrjAh8ajf2mTIi1cYrIhOou4l5kWCZAtpK2B0xShBPKGex%2FajFJ1yjXeMPKs2os%2Bn32tKVUZ2bvFIoK6RAp%2BJ%2BY%2BCtbjLRbI9kXqKmJOOepDuDtvJGApXRA4K2hmPZ2IiiUnpcPIy67zbeWB2Qnw04M3havZ82c4ncQ0jdjVvktg6mmRhaAqsXr1ZfRGZ6j%2BewWcO%2FbHs9Es2NRocRVP8Ku6h4R7tB%2BObgGqxMZLxXgDNYiC0rarULNDV7p%2FKhRuIr7HoRxuA%3D%3D%7Ctkp%3ABk9SR9TS6sStZA', 6450.0]]
    
    item_list = Item(amazon_list, walmart_list, ebay_list)

    amazon_list, walmart_list, ebay_list = item_list.sort_item_list(sort_by, order)

    amazon_list, walmart_list, ebay_list = item_list.num_items_shown(sort_by, order, num_items)

    best_item_list = item_list.best_item(sort_by, order)

    print('Amazon List: ')
    print(amazon_list)
    print('\nWalmart List: ')
    print(walmart_list)
    print('\nEbay List: ')
    print(ebay_list)

    print('\nThe best item based on your filter preference is: ')
    if len(best_item_list) > 1:
        for i in range(len(best_item_list)):
            for j in range(len(best_item_list[i])):
                print(best_item_list[i][j])
            print('\n')
    else:
         for i in range(len(best_item_list)):
             print(best_item_list[i])

if __name__ == "__main__":
    main()



