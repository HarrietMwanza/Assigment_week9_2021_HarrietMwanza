# Start

# I downloaded library requests
# It allows me to access data from the web page
# I downloaded the library BeautifulSoup for pulling data out of HTML and XML files
# I also used the system(sys) module which provides access to variables used
# The library time returns the processor clock time used and it returns localtime based on the argument timer.

# initialize BeautialSoup object with url information Find them html tag to
# Amazon website
# with all the data that we want to scrape

# initialize lists to organize scraped data into categories which is author name and book price

# Allocate the scraped data to the appropriate categories which we created list to hold our results

# Set up pattern recognitions to only grab the information that we need which we used the if and else

# Use these pattern recognitions to clean the data that we scraped to grab what we need and replace the values in our
# categories with these cleaned values.

# return cleaned data back

# End



# we Import required libraries and modules needed for the program
import requests
import bs4
import sys
import time

"""
The get_valid_page() function helps us get the page number for the webpage we want to access 
"""


def get_valid_page(n):
    pages = 2
    if n == 0 or n > pages:
        print("We are Sorry, this web page only has 2 pages. You cannot go further than page 2")
        sys.exit()


page = 1
get_valid_page(page)

# The url variable holds the URL we want to access
url = f"https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/ref=zg_bs_pg_1?_encoding=UTF8&pg={page}"

# we let our user know that we collecting their data
print("Fetching data from webpage\n")
time.sleep(2)

""" We wrap our program in a try except to handle possible errors.
"""
try:

    """
we add the headers because some servers only allow specific user-agent hence making the server 
specifically block requests.Passing header into the .get() will help solve this problem.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 '
                      'Safari/537.36',
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate"
    }
    #  we use request.get() to get web page url.
    response = requests.get(url, headers=headers, params={"wait": 2})

    # Make a soup object from the BeautifulSoup library
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    """
    Book component is where all books information can be found.
    select() method in beautiful soup to select the HTML tag and class 
    """
    book_component = soup.select(".zg-item-immersion")

    # EDGE CASE
    """
    There are problems with requesting from URL, beautiful soup might return an empty list object.
    We want to inform the person running our program to know they should try again if there is a problem
    """
    if not len(book_component):
        print("Oops! The webpage has refused to serve the data. Please can you run the program again")

    # Make an empty list to add all the popular books we have selected
    popular_books = []
    # loop through my book component
    for book in book_component:
        # if the book is a 5 star rated, get the book. Note: this is my logic for getting the popular books.
        # Be free to explore your own logic if you disagree with this
        if "a-star-5" in str(book):
            for book_names in book.select(".p13n-sc-truncate"):
                popular_books.append(book_names.getText().strip())

    """
    Let us get the book prices.
    """
    # Make an empty list to hold the values / prices we get
    popular_books_prices = []
    for book in book_component:
        # We want to make sure we are looking through the book component and getting the prices of popular books
        if "a-star-5" in str(book):
            for prices in book.find(name="span", class_="p13n-sc-price"):
                popular_books_prices.append(float(prices.replace("$", "")))

    """
     we  sort the prices and get the top 10 prices of the books
    """
    # make an empty lst to hold the sorted prices we get
    sorted_top_ten_prices = []
    # Now loop through the initial prices list and get the top 10
    for price in popular_books_prices:
        sorted_top_ten_prices.append(price)
    # The steps below helps get the top 10 prices of books from lowest to highest
    # Note: if you have a max_range, do change the value of max_range. E.g, if you want to get top 20, max_range = 20
    max_range = 10
    sorted_top_ten_prices.sort()
    sorted_top_ten_prices = sorted_top_ten_prices[-max_range:]

    """
    Now that we have the top 10 prices/most expensive books. 
    We need to get the names of the books from the webpage
    """
    # Make an empty list to hold the value
    ten_most_expensive = []

    unsorted_prices = []
    # Loop through the book component
    for book in book_component:
        # if we find a 5 star book
        if "a-star-5" in str(book):
            # loop through the sorted top ten price list as well
            for val in sorted_top_ten_prices:
                # if the val from the price list is in the string book component
                if f"${val}" in str(book):
                    # append all the books in the ten most expensive books list
                    ten_most_expensive.append((book.find(name="div", class_="p13n-sc-truncate").text.strip()))
                    """
                    Again this part below is not important, you can decide to just return the books as they are instead 
                    of putting them in a list of dictionary like I did below
                    """
                    for prices in book.find(name="span", class_="p13n-sc-price"):
                        unsorted_prices.append(prices)

    # USING dictionary Comprehension
    """
    We add all the results to a dictionary
    """
    final_result = [{ten_most_expensive[i]: unsorted_prices[i] for i in range(len(ten_most_expensive))}]

    # This is what we are returning as final result
    print(final_result)

except requests.exceptions.RequestException as e:
    print("Something went wrong,try again. Please check the URL\n", e)

