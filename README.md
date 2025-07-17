# Library Management System
A Flask-based library management system for my college.

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
├── DB/
│   ├── __init__.py
│   └── connection.py          # MongoDB connection
├── services/
│   ├── __init__.py
│   ├── file_service.py       # Department code handling
│   └── import_books_from_excel.py
├── static/                   # Images and assets
├── templates/               # HTML templates
├── app.py                  # Main application
├── department_codes.txt    # Department code mappings
├── student_info.json      # Student database
└── requirements.txt       # Dependencies
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
1. Always backup your MongoDB data before major operations
2. Comment out the import line after initial setup:
```python
# import services.import_books_from_excel  # Comment after initial import
```
3. The system uses session storage for transactions
4. Department codes are managed in `department_codes.txt`
5. Student data is stored in `student_info.json`

## MongoDB Collections
- `books` - Book inventory
- `issued_books` - Transaction records

For more details, check the individual route handlers in [`app.py`](app.py).