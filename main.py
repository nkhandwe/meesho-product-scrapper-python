# import producList
# import requests ,time
# import json 
# import pandas as pd
# from bs4 import BeautifulSoup

from productclass import Product, Htmlextract ,CsvOperations
from utils import field_names

url ="/satin-sarees/pl/5mlbu"
category = "Men"
subcategory="Shirt"
childcategory = "Cotton"
csv_file_name = "csv/products.csv"

# hitting request
# product = Product(url,1)
# req = product.get_request()
# html_extract = Htmlextract(req)

# links = html_extract.get_on_page_product_links()

csv = CsvOperations(file_name=csv_file_name,headers=field_names,field_names=field_names)

# csv.write_file()
# adding links to csv files
# for i in links:
#     csv.append_file({
#     'link':i,
#     'product_id':i.split('/')[-1],
#     'scrapped':False
#     })

for i in csv.read_file():
    print(i['product_id'])