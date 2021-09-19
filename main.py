# import producList
# import requests ,time
# import json 
# import pandas as pd
# from bs4 import BeautifulSoup

from productclass import Product, Htmlextract

cat_url ="https://meesho.com/satin-sarees/pl/5mlbu"

product = Product("/satin-sarees/pl/5mlbu",1)
req = product.get_request()
html_extract = Htmlextract(req)

print(req) 

print(html_extract.get_on_page_product_links())

