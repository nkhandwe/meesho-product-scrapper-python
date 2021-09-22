# import producList
# import requests ,time
# import json 
# import pandas as pd
# from bs4 import BeautifulSoup

from productclass import Product, Htmlextract ,CsvOperations
from utils import field_names

cat_url ="https://meesho.com/satin-sarees/pl/5mlbu"

# product = Product("/satin-sarees/pl/5mlbu",1)
# req = product.get_request()
# html_extract = Htmlextract(req)

# print(req) 

# print(html_extract.get_on_page_product_links())


csv = CsvOperations(file_name="csv/products.csv",headers=field_names,field_names=field_names)


print(csv.append_file({
    'name':'lol',
    'price':21,
    'link':'lllll',
    'product_id':'j98kj2',
    'category':'Men',
    'sub_category':'Shirt',
    'child_category':'Fabrics',
    'description':"shiet ",
    'sizes':'M,L,S',
    'has_similar':False,
    'scrapped':False
}))



