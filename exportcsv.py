from productclass import CsvOperations

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

csv = CsvOperations(file_name=file_name,data=Product name