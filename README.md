# Web Scraping of Apple Store Products
This project is about scraping data about apple store products from the Apple Store HTML webpage. Data points that are scrapped include product description, ratings, price, quantity, shipping date.

The scrapped data is then exported to a excel csv file for analysis.

Tools used: <br>
- Visual Studio

Libraries used: <br>
- Beautiful Soup - For reading the html content from the site and convert the data into a structured tree format. 

Extensions installed: <br>
- Live Server' - For viewing the actual webpage after loading the html file "apple_store.html" in Visual Studio.

## Creating a virtual environment 
A virtual environment (venv) is created for working within that space for the project. Libraries/dependencies are all installed specifically for the project only. 

```python
# Create virtual environment
python3 -m venv ws_env

# Activating the virtual environemnt
source ws_env/bin/activate
```

## Importing HTML data from local directory

```python
# URL source path
html_path = "/Users/ASUS/Library/CloudStorage/OneDrive-Personal/Desktop/Personal project/Python Web Scraping/Apple store web scraping/apple_store.html"

with open(html_path, 'r') as html_file:
    html_content = html_file.read()
```

## Structuring HTML data into tree format of tags
The HTML tags in the page are organized by hierarchical order and allows for easier searching of data by the tag labels using functions such as find() or find_all().

```python
soup = BeautifulSoup(html_content, 'html.parser')

header = soup.find('h1').text.strip()
```

## Extracting URLs 
URL links in the page are extracted by identifying all <a> tags using 'find_all()' . A for loop is then used to iterate through the tags and print out the 'href' attribute of each <a> tag that defines what the URL is pointing to.

```python
menus = soup.find_all('a', href=True)   # filters only the <a> tags with href attributes
for menu in menus:
    print(menu['href'])
```

## Extracting individual product details
Details of each product such as product name, price, available quantity and shipping duration are extracted here. 

The main <div> tags are identified first together with the "class" attribute type to narrow down the type of <div> tags we are looking for.

```python
products_divs = soup.find_all('div',  class_="product")
```

## Create new csv file and write the product details in
Identifying the different <p> tags in each <div> container of each product. The <p> tags contain the descriptive info of each product. 

Either list indexing [] or by attribute is used to identify the <p> tags in each container.

```python
with open('apple_products.csv', 'w') as file_csv:     # 'w' is to write/replace existing data
    writer = csv.writer(file_csv)    # create a new file if none exists and write rows in csv format
    
    # Defining/Creating the headers
    writer.writerow(['product_name', 'price', 'qty_left', 'ratings', 'est'])

    # Getting the data
    # iterate through each <div> container and access the <h3> tag inside the container to get all the PRODUCT NAMES
    for product in products_divs:
        product_name = product.find('h3').text   # using .find() since there is only one <h3> tag per <div> container
        price = product.find('p').text.replace('Price: ', '')    # use .find() since it's the first <p> tag so dont need [] to access it in each container
        qty_left = product.find_all('p')[1].text.replace('Quantity Available: ', '')   # finds all the <p> tags per container as a list and [1] to return the quantity tag info
        ratings = product.find('p', class_="rating").text     # .find() is used since the <p> tag has a 'class' attribute to differentiate it from the other <p> tags
        est = product.find_all('p')[-1].text.replace('Estimated Shipping: ', '')  # finds all <p> tags per container as a list and [-1] to return the shipping tag info

        # Pushing in the data as rows 
        ## must be inside the for loop to get info from ALL containers and pass the new column headers in as actual variable names without string quotes
        writer.writerow([product_name, price, qty_left, ratings, est])

print("Congratulations data scrapped and save successsfully")
```




## Conclusion
Once the data has been scrapped and exported out as a CSV file, the data can then be used for analysis. AS scrapped data may not always be in the desired state to be ready for analysis, data processing steps such as transformation and cleaning  still need to be performed according to the needs of the analysis.

