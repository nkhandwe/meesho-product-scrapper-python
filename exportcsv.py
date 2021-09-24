from productclass import CsvOperations, SqlOperations

file_name="products.csv"
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

if cursor:
    sql = SqlOperations(cursor,connection=sqliteConnection,table=table_name)

csv = CsvOperations(file_name=file_name,headers=field_names,field_names=field_names)