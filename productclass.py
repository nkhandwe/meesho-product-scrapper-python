import requests 
from utils import headers
from bs4 import BeautifulSoup

class Product(object):

    def __init__(self,url,page=None):
        self.base = "https://meesho.com"
        self.page = page
        if page: self.url= f'{self.base+url}?page={page}'
        self.url = self.base+url
    
    def get_request(self):
        if self.page:
            return  requests.get(self.url,headers=headers)
        return  requests.get(self.url,headers=headers)

class Htmlextract(object):

    def __init__(self,page):
        self.content = page.content
        self.soup = BeautifulSoup(self.content, 'html.parser')

    def get_on_page_product_links(self):
        # product cards

        links = self.soup.find_all('div', {"class":"sc-dlfnuX ProductList__GridCol-sc-8lnc8o-0 bAyXPl ldNFyP"})

        # with open('index.html','w') as f:
        #     f.write(str(self.soup))
        
        links_array = [pr.find('a')['href'] for pr in links]

        return links_array
    



    

