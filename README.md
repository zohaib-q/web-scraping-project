This project asks the user to enter a product they are interested in and takes that information to webscrape amazon, walmart, and ebay for that item.
Once all the item information is collected from these websites, the following information is collected into a list:
[name, price, average review, number of review, link to item, validity score]
The validity score is just the average review multiplied by the number of reviews.
The list is then sorted by the category the user wants. The user can sort by price, average review, number of reviews or validity score as of now.
The user can choose whether they want to sort from low to high or high to low.
The user can also choose the amount of items per list they would want to see. 
Finally, the 'best' item across all 3 websites based on the sort chosen by the user is displayed with its information.

Current time complexity: O(n^2)
(takes a long time to run)

