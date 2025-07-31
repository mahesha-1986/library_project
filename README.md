# Library Management System - BBHC
A comprehensive library management system for Dr. B. B. Hegde First Grade College, Kundapura.

## Student Data Management

### Converting Excel to JSON
Two essential scripts are used to manage student data. These must be run externally before setting up the system:

1. **Excel to JSON Converter**:
```python
import pandas as pd
import json

# Read Excel file
file_path = "students.xlsx"
sheets = pd.read_excel(file_path, sheet_name=["First Year", "Second Year"])

def process_sheet(df):
    result = {}
    required_columns = ["rollNo", "studentName", "section", "year"]
    for col in required_columns:
        if col not in df.columns:
            df[col] = ""

    for _, row in df.iterrows():
        roll_no = str(row.get("rollNo", "")).strip()
        if roll_no:
            result[roll_no] = {
                "studentName": str(row.get("studentName", "")).strip(),
                "section": str(row.get("section", "")).strip(),
                "year": str(row.get("year", "")).strip()
            }
    return result

# Process sheets and save to JSON
first_year_json = process_sheet(sheets["First Year"])
second_year_json = process_sheet(sheets["Second Year"])

with open("first_year.json", "w") as f1:
    json.dump(first_year_json, f1, indent=4)
with open("second_year.json", "w") as f2:
    json.dump(second_year_json, f2, indent=4)
```

2. **Section Updater** (For yearly updates):
```python
import json
import re

with open("students.json", "r") as file:
    data = json.load(file)

# Update sections (I -> II, II -> III)
for roll_no, details in data.items():
    section = details.get("section", "")
    if re.match(r"^I\b", section):
        details["section"] = re.sub(r"^I\b", "II", section)
    elif re.match(r"^II\b", section):
        details["section"] = re.sub(r"^II\b", "III", section)

with open("students.json", "w") as file:
    json.dump(data, file, indent=4)
```

### How to Use Student Data Scripts:
1. Create Excel file `students.xlsx` with sheets "First Year" and "Second Year"
2. Run Excel to JSON converter script
3. Move generated JSON files to `students_data_JSON` folder
4. Use Section Updater script yearly when students move to next class
5. Always verify data after conversion/updates

## Setup Instructions

### 1. Clone & Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd Book_Issue_Return_System

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. MongoDB Setup
1. Install MongoDB on your system
2. Start MongoDB service
3. The system will automatically connect to: `mongodb://localhost:27017/`
4. Database name: `library_db`

### 3. Initial Data Import
1. Place your Excel file named `bookreport_copy_with_barcodes.xlsx` in the root directory
2. In [`app.py`](app.py), uncomment this line for first-time setup:
```python
import services.import_books_from_excel
```
3. Run the application once to import books
4. After successful import, comment out the line again

### 4. Run Application
```bash
flask run
```
Access the application at: http://127.0.0.1:5000

## Project Structure

```
Book_Issue_Return_System/
├── app.py                      # Main Flask application
├── bookreport_copy_with_barcodes.xlsx  # Book data source
├── department_codes.txt        # Department codes mapping
├── requirements.txt            # Python dependencies
├── student_info.json          # Sample student information
├── DB/                        # Database connection
│   ├── __init__.py
│   └── connection.py          # MongoDB connection setup
├── services/                  # Helper services
│   ├── __init__.py
│   ├── file_service.py       # File handling utilities
│   └── import_books_from_excel.py  # Excel to DB import
├── static/                    # Static assets
│   ├── clearall.png
│   ├── college_logo.png
│   ├── dustbin.png
│   ├── logo.png
│   └── OIP.png
├── templates/                 # HTML templates
│   ├── all_books.html        # All books listing
│   ├── book_system.html      # Main dashboard
│   ├── index.html            # Home page
│   ├── statistics.html       # Book statistics
│   └── view_books.html       # Book details view
└── students_data_JSON/       # Student data storage
    └── *.json                # Student JSON files
```

## Routes & Features

### 1. Main Routes
- `/` - Home page with book transaction history
- `/issue-book` - Issue books to students
- `/all-books` - View all books in library
- `/search_statistics` - View department-wise statistics

### 2. Book Management
- `/add-book` - Add new books
- `/view-books` - Search books by barcode
- `/Save` - Save book issue transactions
- `/returned_books` - Process book returns

### 3. API Routes
- `/recommendation` - Auto-suggestions for search
- `/lookup_barcode` - Barcode verification

## Required Excel Format
The `bookreport_copy_with_barcodes.xlsx` should have these columns:
- `barcode_value`
- `accession number`
- `title`
- `department`
- `author`
- `department_codes`

## Dependencies
```
flask
pymongo
pandas
python-dotenv
openpyxl
```

## Important Notes

### 1. Student Data Management
- **Excel Format Requirements**:
  - Create `students.xlsx` with two sheets: "First Year" and "Second Year"
  - Required columns: rollNo, studentName, section, year
  - All column names are case-sensitive
  - Keep data clean and consistent

- **JSON File Management**:
  - Run conversion scripts externally
  - Always backup before updates
  - Store JSON files in `students_data_JSON` folder
  - Verify data after conversion

### 2. System Setup
- Backup MongoDB data before major operations
- Comment out the import line after initial setup:
```python
# import services.import_books_from_excel  # Comment after initial import
```
- System uses session storage for transactions
- Department codes are managed in `department_codes.txt`

## MongoDB Collections
- `books` - Book inventory
  - Stores all book information
  - Tracks department mapping
  - Maintains availability status

- `issued_books` - Transaction records
  - Records all issue/return transactions
  - Links students with books
  - Maintains transaction dates

For more details, check the individual route handlers in [`app.py`](app.py).