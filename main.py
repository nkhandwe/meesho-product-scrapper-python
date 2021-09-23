from productclass import Product, Htmlextract ,CsvOperations,SqlOperations
from utils import field_names
import sqlite3

url ="/tshirts-men/pl/t3brl"
category = "Men"
sub_category="Top Wear"
child_category = "Tshirts"
csv_file_name = "files/products.csv"
no_of_pages_to_extract = 1 # default should be 1


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

    # create database
    # sql.create_table()




# getting links from given url
for i in range(no_of_pages_to_extract):
    # hitting request
    product = Product(url)
    req = product.get_request(i+1)
    html_extract = Htmlextract(req)
    links = html_extract.get_on_page_product_links()
    print(links)

    # uncomment this new line when start with a new file
    # csv.write_file()

    # adding links to database
    for i in links:
        sql.insert_data({
            'link':i,
            'product_id':i.split('/')[-1],
            'scrapped':False,
            'category':category,
            'sub_category':sub_category,
            'child_category':child_category
        })


# start with adding all details of one product from database
not_scrapped_data = sql.get_unscrapped_data()

for i in not_scrapped_data:

    # comming data (id,link)

    url = i[1]
    product = Product(url)
    req = product.get_request()
    html_extract = Htmlextract(req)

    # json extracted
    html_extract.get_json()

    # details of one product
    details = html_extract.get_data_of_single_product()

    #  downloading image and getting path
    images =(html_extract.get_image_url(details['images']))
    details['images'] =images
    print(details)

    sql.update_data_by_id(i[0],details)



cursor.close()