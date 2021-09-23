from productclass import Product, Htmlextract ,CsvOperations,SqlOperations
from utils import field_names
import sqlite3

# url ="/satin-sarees/pl/5mlbu"
# category = "Men"
# sub_category="Top Wear"
# child_category = "Tshirts"
# csv_file_name = "files/products.csv"
# no_of_pages_to_extract = 1 # default should be 1


cursor = None
table_name = 'products'

# creating connection with database
try:
    sqliteConnection = sqlite3.connect('files/products.db')
    cursor = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")

    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("SQLite Database Version is: ", record)

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

if cursor:
  sql = SqlOperations(cursor,connection=sqliteConnection,table=table_name)



# print(sql.create_table('products'))
print(sql.insert_data({
              'name':'name',
                'description':'description',
                'price':'mrp',
                'images':'images',
                'sizes':'variations',
                'has_similar':'similar',
                'scrapped':True
            }))

print(sql.get_data())

# csv = CsvOperations(file_name=csv_file_name,headers=field_names,field_names=field_names)

# for i in range(no_of_pages_to_extract):
#     # hitting request
#     product = Product(url,i+1)
#     req = product.get_request()
#     html_extract = Htmlextract(req)

#     links = html_extract.get_on_page_product_links()

    # uncomment this new line when start with a new file
    # csv.write_file()

    # adding links to csv files
    # for i in links:
    #     if csv.check_availablity_of_data('tct9v'):
    #       print("Duplicate")
    #       continue
    #     csv.append_file({
    #     'link':i,
    #     'product_id':i.split('/')[-1],
    #     'scrapped':False,
    #     'category':category,
    #     'sub_category':sub_category,
    #     'child_category':child_category
    #     })


# for i in csv.read_file():
#     print(i['product_id'])



# update by id
# if csv.check_availablity_of_data('tct9v'):
#     print(csv.update_file_by_id('tct9v',{
#         'name':'here',
#         'scrapped':True
#     }))

# print(csv.get_not_scrapped())


# url = '/aagam-voguish-sarees/p/v0pji'
# product = Product(url)
# req = product.get_request()
# html_extract = Htmlextract(req)
# json extracted
# print(req)
# print(html_extract.get_json())

# details of one product
# details = html_extract.get_data_of_single_product()
# html_extract.get_image_url(details['images'])

# links = html_extract.get_on_page_product_links()






cursor.close()