# Creating a virtual environment for the project so that everything installed stays within this project only
# python3 -m venv ws_env

# Activating the virtual environment
# source ws_env/bin/activate

from bs4 import BeautifulSoup
import csv

# URL source path
html_path = "/Users/ASUS/Library/CloudStorage/OneDrive-Personal/Desktop/Personal project/Python Web Scraping/Apple store web scraping/apple_store.html"

# 'with' takes care of closing the file after use
# 'r' is to open the file in read-mode only and store in 'html_content', no modification
with open(html_path, 'r') as html_file:
    html_content = html_file.read()

# print(html_content)
 
# reads the html content from the site and converts into a structured tree format
soup = BeautifulSoup(html_content, 'html.parser')

header = soup.find('h1').text.strip()
# print(header)

# use 'find_all' in this case since we are scraping all the headers together (the <a> tags with href attributes)
menus = soup.find_all('a')
# use for loop to iterate through each menu label and convert to text
for menu in menus:
    print(menu.text)

# use 'find_all' as this time is to get the URLs for the 4 menu labels
menus = soup.find_all('a', href=True)   # filters only the <a> tags with href attributes
for menu in menus:
    print(menu['href'])   # tags are dictonaries and ['href'] is to get the value of the href key-value pair

# find all the <div> tags and store under the variable 'products_divs'
products_divs = soup.find_all('div',  class_="product")

# Place the with() segment to open a csv file BEFORE the loop starts so that each product inside the loop is included in the output
# using 'with' to open a csv file ensures that if an error occurs, anything ran before the error can still be saved
with open('apple_products.csv', 'w') as file_csv:     # 'w' is to write/replace existing data
    writer = csv.writer(file_csv)    # create a new file if none exists and write rows in csv format
    
    # Defining/Creating the headers
    writer.writerow(['product_name', 'price', 'qty_left', 'ratings', 'est'])

    # Getting the data
    # iterate through each <div> container and access the <h3> tag inside the container to get all the PRODUCT NAMES
    for product in products_divs:
        product_name = product.find('h3').text  # using .find() since there is only one <h3> tag per <div> container
        price = product.find('p').text.replace('Price: ', '')   # use .find() since it's the first <p> tag so dont need [] to access it in each container
        qty_left = product.find_all('p')[1].text.replace('Quantity Available: ', '')  # finds all the <p> tags per container as a list but [1] will return only the quantity tag info
        ratings = product.find('p', class_="rating").text     # .find() is used since the <p> tag has a 'class' attribute to separate it from the other <p> tags
        est = product.find_all('p')[-1].text.replace('Estimated Shipping: ', '')  # finds all the <p> tags per container as a list but [-1] will return only the shipping tag info


        # Pushing in the data into the rows 
        ## must be inside the for loop to get info from ALL containers
        ## pass the column headers in as the actual variable names without string quotes
        writer.writerow([product_name, price, qty_left, ratings, est])
        
print("Congratulations data scrapped and save successsfully")

