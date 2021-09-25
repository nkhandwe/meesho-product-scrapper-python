import requests 
from utils import headers ,field_names
from bs4 import BeautifulSoup
from csv import DictReader , DictWriter
from collections import OrderedDict
import json

class Product(object):

    def __init__(self,url,*args,**kwargs):
        self.base = "https://meesho.com"
        self.url = self.base+url
    
    def get_request(self,*args,**kwargs):
        print(self.url)
        if args:
            return  requests.get(f"{self.url}?page={args[0]}",headers=headers)
        return  requests.get(self.url,headers=headers)

class Htmlextract(object):

    def __init__(self,page=None,*args,**kwargs):
        self.content = page.content
        self.soup = BeautifulSoup(self.content, 'html.parser')
        self.json_file = 'files/main.json'
        self.images_save = 'files/products/'
        self.pathname = 'products/'


    def get_on_page_product_links(self):
        # product cards
        links = self.soup.find_all('div', {"class":"sc-dlfnuX ProductList__GridCol-sc-8lnc8o-0 bAyXPl ldNFyP"})
        links_array = [pr.find('a')['href'] for pr in links]
        return links_array
    
    def get_json(self):
        with open(self.json_file,'w') as f:
            # print(self.soup.find('script',{"id":"__NEXT_DATA__","type":"application/json"}))
            f.write(self.soup.find('script',{"id":"__NEXT_DATA__","type":"application/json"}).text)
        return self.soup.find('script',{"id":"__NEXT_DATA__","type":"application/json"}).text
    
    def get_data_of_single_product(self):
        with open(self.json_file,'r') as f:
            data = json.load(f)
            data=data['props']['pageProps']['initialState']['product']
            similar =data['similar']['products']
            details =data['details']['data']
            return{
                'name':details['name'].replace("'",""),
                'description':details['description'].replace("'",""),
                'price':details['mrp_details']['mrp'],
                'images':details['images'],
                'sizes':json.dumps(details['variations']),
                'has_similar':len(similar),
                'similar':json.dumps([i['product_id'] for i in similar]),
                'scrapped':True
            }

        return False
    
    def get_image_url(self,*args,**kwargs):
        from datetime import datetime
        import urllib.request
        image_urls=[]
        for i in args[0]:
            image_name =str(datetime.timestamp(datetime.now()))+i.split('/')[-1]
            image_urls.append(self.pathname+image_name)
            urllib.request.urlretrieve(i, str(self.images_save+image_name))
        return json.dumps(image_urls)

class CsvOperations(object):

    def __init__(self,file_name,data=None,headers=None,field_names=None,*args,**kwargs):
        self.file_name = file_name
        self.data = data
        self.headers = headers
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
        print(args)
        try:
            with open(self.file_name,'w') as f:
                f = DictWriter(f,delimiter=',',fieldnames=self.field_names)
                if self.headers:
                    f.writeheader()
                for i in args[0]:
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

class SqlOperations(object):

    def __init__(self,cursor,table,connection,*args,**kwargs):
        self.cursor = cursor
        self.connection = connection
        self.table = table

    def create_table(self,*args,**kwargs):
        if args[0]=='product':
            sqlite_create_table_query = f'''CREATE TABLE { self.table  } (
                                id INTEGER  PRIMARY KEY AUTOINCREMENT,
                                product_id TEXT UNIQUE,
                                name TEXT ,
                                price INTEGER ,
                                link TEXT ,
                                images TEXT ,
                                category TEXT ,
                                sub_category TEXT ,
                                child_category TEXT ,
                                description TEXT ,
                                sizes TEXT ,
                                colours TEXT ,
                                has_similar TEXT,
                                similar TEXT,
                                scrapped TEXT
                                );'''
        if args[0]=='cat':
            # for cat table
            sqlite_create_table_query = f'''CREATE TABLE { self.table  } (
                                id INTEGER  PRIMARY KEY AUTOINCREMENT,
                                link TEXT ,
                                category TEXT ,
                                sub_category TEXT ,
                                child_category TEXT ,
                                scrapped TEXT
                                );'''
        
        try :
            self.cursor.execute(sqlite_create_table_query)
            return True

        except Exception as e:
            print(e)
            return False
    
    def get_data(self,*args,**kwargs):
        try:
            sqlite_select_query = f"""SELECT * from {self.table}"""
            self.cursor.execute(sqlite_select_query)
            records = self.cursor.fetchall()
            return records
        except Exception as e:
            print(e)
            return False

    def insert_data(self,*args, **kwargs):
        # needed data as dictionary to insert eg:  {'name':'you name'}
        if not self.table:
            return "No table given"
        try:
            columns = ()
            values =()
            for i in args[0]:
                columns = columns + (i,)
                values = values + (args[0][i],)

            sqlite_insert_query = f"""INSERT INTO {self.table}
                            {columns } 
                            VALUES 
                            {values}"""
            self.cursor.execute(sqlite_insert_query)
            self.connection.commit()
            return  True
        except Exception as e:
            print(e)
            return False
    
    def get_data_by_id(self,*args,**kwargs):
        # only pass id as argument
        try:
            sqlite_select_query = f"""SELECT * FROM {self.table} where id = {args[0]}"""
            self.cursor.execute(sqlite_select_query)
            return  self.cursor.fetchall()
        except Exception as e:
            print(e)
            return False

    def update_data_by_id(self,*args,**kwargs):
        #  pass id and dictionary as argument for data updation eg: (1,{'name':'your name'})

        try:
            updates = ""
            for i in args[1]:
                updates+= f" {i} = '{args[1][i]}' ,"

            sql_update_query = f"""Update {self.table} set {updates[:-1]} where id = {args[0]}"""
            self.cursor.execute(sql_update_query)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_unscrapped_data(self,*args,**kwargs):
        try:
            sqlite_select_query = f"""SELECT {args[0] if args else '*'} from {self.table} where scrapped = 0 """
            self.cursor.execute(sqlite_select_query)
            records = self.cursor.fetchall()
            return records
        except Exception as e:
            print(e)
            return False

    def get_data_with_image(self,*args,**kwargs):
        try:
            sqlite_select_query = f"""SELECT {args[0] if args else '*'} from {self.table} where images IS NOT NULL """
            self.cursor.execute(sqlite_select_query)
            records = self.cursor.fetchall()
            return records
        except Exception as e:
            print(e)
            return False
