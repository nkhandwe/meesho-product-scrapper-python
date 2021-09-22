import requests 
from utils import headers ,field_names
from bs4 import BeautifulSoup
from csv import DictReader , DictWriter

class Product(object):

    def __init__(self,url,page=None,*args,**kwargs):
        self.base = "https://meesho.com"
        self.page = page
        if page: self.url= f'{self.base+url}?page={page}'
        self.url = self.base+url
    
    def get_request(self):
        if self.page:
            return  requests.get(self.url,headers=headers)
        return  requests.get(self.url,headers=headers)

class Htmlextract(object):

    def __init__(self,page,*args,**kwargs):
        self.content = page.content
        self.soup = BeautifulSoup(self.content, 'html.parser')

    def get_on_page_product_links(self):

        # product cards
        links = self.soup.find_all('div', {"class":"sc-dlfnuX ProductList__GridCol-sc-8lnc8o-0 bAyXPl ldNFyP"})

        # with open('index.html','w') as f:
        #     f.write(str(self.soup))

        links_array = [pr.find('a')['href'] for pr in links]
        return links_array
    


class CsvOperations(object):

    def __init__(self,file_name,data=None,headers=None,field_names=None,*args,**kwargs):
        self.file_name = file_name
        self.data = data
        self.headers = headers
        print(args)
        self.field_names = field_names


    def write_file(self,*args,**kwargs):
        try:
            with open(self.file_name,'w') as f:
                print(args)
                f = DictWriter(f,delimiter=',',fieldnames=self.field_names)
                if self.headers:
                    f.writeheader()
                for i in args:
                    f.writerow(i)
            return True

        except Exception as e:
            return e

    def append_file(self,*args,**kwargs):
        # print(self)
        try:
            with open(self.file_name,'a') as f:
                f = DictWriter(f,delimiter=',',fieldnames=self.field_names)

                for i in args:
                    f.writerow(i)
            return True

        except Exception as e:
            return e








    

