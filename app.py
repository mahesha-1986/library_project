from flask import Flask, jsonify, render_template, request, redirect, url_for, session , flash
import json
import logging
import pandas as pd
from bson import ObjectId
from DB.connection import db
from datetime import datetime
# Uncomment this line if you want to import books from an Excel file, white initial setup of the application
#import services.import_books_from_excel 
from services import Read_DepartmentCodes


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)

app.secret_key = 'Student_Barcode_Data'

print("APP Started")
books_collection = db['books']
issued_books = db['issued_books']

# Load student data
with open('student_info.json', 'r', encoding='utf-8') as f:
    student_data = json.load(f)


@app.route('/')
def home():
    try:
        All_issued_books_history = issued_books.find()
        All_issued_books_history = list(All_issued_books_history)
         # Reverse the order to show the latest issued books first
        All_issued_books_history.reverse()
        for b in All_issued_books_history:
            b['_id'] = str(b['_id'])
            
        logger.info("All issued books history loaded successfully.")

    except Exception as e:
        logger.error("Error loading home page", 500)


    return render_template('book_system.html',Books_history= All_issued_books_history)


@app.route("/search_statistics", methods=["GET", "POST"])
def search_statistics():
    try:
        total_books = None
        issued_books_count = None
        available_books = None
        header = None

        if request.method == "POST":
            query = request.form.get("query", "").strip()
            search_type = request.form.get("search_type", "").strip().lower()

            if not query or not search_type:
                return render_template(
                    'statistics.html',
                    error="Please enter both query and search type."
                )
            
           


            # Prepare query value based on search type
            if search_type == "department code":
                query_value = query.upper()
                search_type = "department_code"
            elif search_type == "title":
                query_value = query.upper()
                search_type = "title"
            else:
                query_value = query.title()

            header = f"{search_type.title() if search_type != 'department_code' else 'Department Code'}: {query_value}"

            # Prepare MongoDB filter
            filter_query = {search_type: query_value}
            filter_query_issued = {"book." + search_type: query_value, "status": "issued"}

            # Count total books
            total_books = books_collection.count_documents(filter_query)

            # Count issued books
            issued_books_count = issued_books.count_documents(filter_query_issued)
            print("total", total_books, "issued", issued_books_count)
            available_books = total_books - issued_books_count

        # Always render the page
        return render_template(
            'statistics.html',
            total_books=total_books,
            issued_books=issued_books_count,
            available_books=available_books,
            header=header,
        )

    except Exception as e:
        logger.error(f"Error in search_statistics: {e}")
        return jsonify({"error": "Error processing search request"}), 500
    


@app.route("/recommendation")
def recommendation():
    search_type = request.args.get("type", "Title").lower()
    query = request.args.get("query", "")
    
    
    try:
        if search_type == "department code":
            search_type = "department_code"

        cursor = books_collection.find(
                {search_type: {"$regex": query, "$options": "i"}},
                {search_type: 1, "_id": 0}
        )
        
        result_list = [doc[search_type] for doc in cursor]
        result_list = list(set(result_list))  # Convert to set and back to list to remove duplicates

        
        suggestions = [s for s in result_list if query.lower() in s.lower()]
        return jsonify(suggestions)

    except Exception as e:
        logger.error(f"Error fetching data for recommendations: {e}")
        return jsonify({"error": "Error fetching data"}), 500
   



@app.route('/returned_books')
def return_book():
    id = request.args.get('id')
    if not id:
        return "Book ID is required", 400

    try:
        issued_books.update_one(
            {'_id': ObjectId(id)},
            {'$set': {'status': 'returned', 'returned_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}
        )
        logger.info(f"Book with ID {id} returned successfully.")
    except Exception as e:
        logger.error(f"Error returning book with ID {id}: {e}")
        return "Error returning book", 500

    return redirect(url_for('home'))

@app.route('/all-books')
def all_books():
    try:
        departments = Read_DepartmentCodes()
        books_cursor = books_collection.find()
        books = [{**book, '_id': str(book['_id'])} for book in books_cursor]

        for book in books:
            book_history = issued_books.find_one({'book.barcode': book['barcode'], 'status': 'issued'})
           
            if not book_history:
                book['status'] = 'available'
            else:
                book['status'] = 'not available'
                book['student'] = book_history.get('student')
                book['issued_at'] = book_history.get('issued_at')

    except Exception as e:
        logger.error("Error fetching books: %s", e)
        return "Error fetching books", 500
    return render_template("all_books.html", Books=books, departments=departments, Book_Count=len(books))



@app.route('/issue-book', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        key = request.form.get('rollno', '').strip().upper()
        if key in student_data:
            result = {'rollno': key, **student_data[key]}
        else:
            error = f"No data found for roll number: {key}"
    return render_template('index.html', result=result, error=error)

@app.route('/view-books')
def view_books():
    key = request.args.get('rollno')
    if key:
        session['student'] = {'rollno': key, **student_data[key]}

    barcode = request.args.get('barcode')
    barcode = barcode.upper() if barcode else None
    barcode_result = None
    barcode_searched = None
    already_issued = None

    try:
        if barcode:
            barcode_result = books_collection.find_one({'barcode': barcode})
            if barcode_result:
                # remove _id or convert it
                barcode_result['id'] = str(barcode_result.pop('_id'))
                session['book'] = barcode_result

                already_issued = issued_books.find_one({'book.barcode': barcode,'status': 'issued'})
                if already_issued:
                    # convert any ObjectId inside already_issued too
                    already_issued['_id'] = str(already_issued['_id'])

            else:
                barcode_searched = barcode

    except Exception as e:
        logger.error("Error in view_books route: %s", e)

    books = []
    try:
        books_cursor = books_collection.find()
        books = [{**book, '_id': str(book['_id'])} for book in books_cursor]
    except Exception as e:
        logger.error("Error fetching books: %s", e)

    return render_template(
        'view_books.html',
        
        barcode_result=barcode_result,
        barcode_searched=barcode_searched,
        already_issued=already_issued
    )

@app.route('/Save')
def Save_To_DB():
    student = session.get('student')
    barcode_result = session.get('book')
    if not student or not barcode_result:
        return "Missing student or book information", 400

    issued_doc = {
        'student': student,
        'book': barcode_result,
        'status': 'issued',
        'issued_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # readable current date & time
    }

    try:
        issued_books.insert_one(issued_doc)
        logger.info("Book issued successfully!")
    except Exception as e:
        logger.error("Error while issuing book: %s", e)
        return "Error issuing book", 500

    return redirect(url_for('home'))


@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    print("Add Book Page")
    if request.method == 'POST':
        print("Add Book Page111")
        name = str(request.form['book_name'])
        dept = str(request.form['department'])
        author = str(request.form['author'])
        accession_number = request.form['accession_number']
        try:
            
            departments = Read_DepartmentCodes()
            
            if dept in departments:
                dept_code = departments[dept]
            else:
                logger.error(f"Invalid department: {dept}")
                return "Invalid department", 400
            barcode = dept_code +  str(accession_number)

            book_data = {
                'title': name.upper(),
                'barcode': barcode.upper(),
                'author': author.title(),
                'accession_number': accession_number,
                'department': dept.title(),
                'department_code': dept_code.upper(),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # readable current date & time
            }
            books_collection.insert_one(book_data)
            logger.info("Book added successfully.")
            flash(f"Book '{name}' added successfully!", "success")
            return redirect(url_for('all_books'))
 
        except Exception as e:
            logger.error(f"Error adding book: {e}")
            return "Error adding book", 500





@app.route('/lookup_barcode', methods=['GET'])
def lookup_barcode():
    barcode = request.args.get('barcode')
    if not barcode:
        return jsonify({"error": "No barcode provided"}), 400
    book = books_collection.find_one({'barcode': barcode})
    if not book:
        return jsonify({"error": "Book not found"}), 404
    book.pop('_id', None)
    return jsonify(book)

# fetch('http://localhost:5000/delete-issued-book/64f9b1e4d1b9a7d8e9a3c123', {
#     method: 'DELETE'
# })
# .then(response => response.json())
# .then(data => console.log(data))
# .catch(error => console.error(error));



@app.route('/delete-issued-book/<string:book_id>', methods=['DELETE'])
def delete_issued_book(book_id):
    try:
        # Attempt to delete by ObjectId
        result = issued_books.delete_one({"_id": ObjectId(book_id)})

        if result.deleted_count == 0:
            return jsonify({"message": "No record found with that ID"}), 404

        return jsonify({"message": "Record deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# fetch('http://localhost:5000/clear-issued-books', {
#     method: 'DELETE'
# })
# .then(response => response.json())
# .then(data => console.log(data))
# .catch(error => console.error(error));


@app.route('/clear-issued-books', methods=['DELETE'])
def clear_issued_books():
    try:
        result = issued_books.delete_many({})  # Delete all documents
        return jsonify({
            "message": "All records deleted successfully",
            "deleted_count": result.deleted_count
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.debug = True
    app.run(debug= True)
