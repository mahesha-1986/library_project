import pandas as pd
from pymongo import UpdateOne
from DB.connection import db  # Assuming this returns a valid MongoDB connection

# Load Excel file
excel_file = 'bookreport_copy_with_barcodes.xlsx'
df = pd.read_excel(excel_file)

# Drop rows with missing barcodes (optional but recommended)
df.dropna(subset=['barcode_value'], inplace=True)

# Reference to the collection
books_collection = db['books']

# Prepare bulk operations
operations = []
for record in df.to_dict(orient='records'):
    s= record.get('title').upper()
    if s:
        s = " ".join(s.split())

 
    operations.append(
        UpdateOne(
            {'barcode': record['barcode_value']},
            {'$set': {
                'accession_number': record.get('accession number'),
                'title': s,
                'department': record.get('department').title(),
                'author': str(record.get('author')).title(),
                'department_code': record.get('department_codes').upper(),
                'barcode': record.get('barcode_value').upper()
            }},
            upsert=True
        )
    )

# Perform bulk write if there’s anything to insert
if operations:
    result = books_collection.bulk_write(operations)
    print(f'Bulk write complete. Inserted: {result.upserted_count}, Modified: {result.modified_count}')
else:
    print('No valid data to insert.')
