import requests 
from utils import headers ,field_names
from bs4 import BeautifulSoup
from csv import DictReader , DictWriter
from collections import OrderedDict
import json

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

    def __init__(self,page=None,*args,**kwargs):
        self.content = page.content
        self.soup = BeautifulSoup(self.content, 'html.parser')
        self.json_file = 'files/main.json'
        self.images_save = 'images/'


    def get_on_page_product_links(self):
        # product cards
        links = self.soup.find_all('div', {"class":"sc-dlfnuX ProductList__GridCol-sc-8lnc8o-0 bAyXPl ldNFyP"})
        links_array = [pr.find('a')['href'] for pr in links]
        return links_array
    
    def get_json(self):
        # with open(self.json_file,'w') as f:
        #     f.write(self.soup.find('script',{"id":"__NEXT_DATA__","type":"application/json"}).text)
        return self.soup.find('script',{"id":"__NEXT_DATA__","type":"application/json"}).text
    
    def get_data_of_single_product(self):
        with open(self.json_file,'r') as f:
            data = json.load(f)
            data=data['props']['pageProps']['initialState']['product']
            similar =data['similar']['products']
            details =data['details']['data']
            return{
                'name':details['name'],
                'description':details['description'],
                'price':details['mrp_details']['mrp'],
                'images':details['images'],
                'sizes':details['variations'],
                'has_similar':len(similar),
                'similar':[i['product_id'] for i in similar],
                'scrapped':True
            }

        return False
    
    def get_image_url(self,*args,**kwargs):
        from datetime import datetime
        import urllib.request
        image_urls=[]
        for i in args[0]:
            image_name =str(datetime.timestamp(datetime.now()))+i.split('/')[-1]
            image_urls.append(image_name)
            urllib.request.urlretrieve(i, str(self.images_save+image_name))
        return image_urls



    


class CsvOperations(object):

    def __init__(self,file_name,data=None,headers=None,field_names=None,*args,**kwargs):
        self.file_name = file_name
        self.data = data
        self.headers = headers
        print(args)
        self.field_names = field_names

    def read_file(self,*args,**kwargs):
        with open(self.file_name,'r') as f:
                read = DictReader(f,delimiter=',')
                return [re for re in read]
    
    def get_not_scrapped(self,*args,**kwargs):
        with open(self.file_name,'r') as f:
                read = DictReader(f,delimiter=',')
                return [re for re in read if re['scrapped']=='False']

    def write_file(self,*args,**kwargs):
        try:
            with open(self.file_name,'w') as f:
                f = DictWriter(f,delimiter=',',fieldnames=self.field_names)
                if self.headers:
                    f.writeheader()
                for i in args:
                    f.writerow(i)
            return True

        except Exception as e:
            return e

    def append_file(self,*args,**kwargs):
        try:
            with open(self.file_name,'a') as f:
                f = DictWriter(f,delimiter=',',fieldnames=self.field_names)
                for i in args:
                    f.writerow(i)
            return True

        except Exception as e:
            return e
    
    def update_file_by_id(self,*args,**kwargs):
        # print(dict(args[1]))
        if len(self.read_file())==0:
            raise "No data for updation"
        with open(self.file_name,'r') as f:
            read = DictReader(f,delimiter=',')
            ls=[re for re in read]

            with open(self.file_name,'w') as f:
                update = DictWriter(f,delimiter=',',fieldnames=self.field_names)
                if self.headers:
                    update.writeheader()
                for i in ls:
                    if args[0] == i['product_id']:
                        dc = args[1].copy()

                        for key in dc:
                            i[key] = dc[key]
                        update.writerow(i)

                    else:
                        update.writerow(i)
            return True


    # search performed by id
    def check_availablity_of_data(self,*args,**kwargs):
        for i in self.read_file():
            if args[0] == i['product_id']:
                return True
        return False





    








    

