from productclass import CsvOperations, SqlOperations
import sqlite3

file_name="products.csv"
cursor = None
table_name = 'products' #database
field_names=[
    'Product name',
    'Description',
    'Slug',
    'SKU',
    'Categories',
    'Auto Generate SKU',
    'Status',
    'Is featured?',
    'Brand',
    'Product collections',
    'Labels',
    'Tax',
    'Images',
    'Price',
    'Product attributes',
    'Import type',
    'Is variation default?',
    'Stock status',
    'With storehouse management',
    'Quantity',
    'Allow checkout when out of stock',
    'Sale price',
    'Start date sale price',
    'End date sale price',
    'Weight',
    'Length',
    'Wide',
    'Height',
]


# creating database connection
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
    exit()

if cursor:
    sql = SqlOperations(cursor,connection=sqliteConnection,table=table_name)
    csv = CsvOperations(file_name=file_name,headers=field_names,field_names=field_names)

# getting data from database
products = sql.get_data()
# print(data)

export_data = []

for product in products:
    #  i : (id , product_id, name, price, link, images, category, sub_category, child_category, description, sizes, colours, has_similar, similar, scrapped)

    export_data.append({
    'Product name':product[2],
    'Description':product[9],
    'Slug':product[1],
    'SKU':product[1],
    'Categories':product[6:9],
    'Status':'published',
    'Is featured?':'No',
    'Images':",".join(product[5]),
    'Price':product[3],
    'Product attributes':f"Size:{product[10][-1]},Colour:{product[11][-1]}",
    'Import type':'product',
    'Stock status':'in_stock',
    'Quantity':100,
    })
    exit()

print(export_data)

