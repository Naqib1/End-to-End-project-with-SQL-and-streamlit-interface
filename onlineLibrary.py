import streamlit as st
import sqlite3
from datetime import date

# Connect to the database
db = sqlite3.connect('Online_Library.db')
crsr = db.cursor()

# Set up the layout
st.set_page_config(page_title="My Online Library", layout="wide")

# Colors and design
primary_color = "#4CAF50"  # Green
secondary_color = "#2E7D32"  # Dark Green
background_color = "#000000"  # Black
text_color = "#FFFFFF"  # White

# CSS for design and font improvements
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Noto+Sans+Arabic&display=swap');

    .stApp {{
        background-color: {background_color};
        font-family: 'Noto Sans Arabic', sans-serif;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {text_color};  # All headings in black
        font-family: 'Amiri', serif;
    }}
    .stButton button {{
        background-color: {primary_color};
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        margin: 5px;
        font-family: 'Noto Sans Arabic', sans-serif;
        width: 170px;  # Fixed width for buttons
        height: 50px;  # Fixed height for buttons
    }}
    .stTextInput input {{
        font-family: 'Noto Sans Arabic', sans-serif;
        color: {text_color};  # Text color
    }}
    .stMarkdown {{
        font-family: 'Noto Sans Arabic', sans-serif;
        font-size: 18px;
        color: {text_color};  # Text color
    }}
    .stSelectbox select {{
        font-family: 'Noto Sans Arabic', sans-serif;
        color: {text_color};  # Text color
    }}
    .stTextArea textarea {{
        font-family: 'Noto Sans Arabic', sans-serif;
        color: {text_color};  # Text color
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Button to return to the home page
def back_to_home():
    if st.button("Back to Home"):
        st.session_state.current_page = "Home"

# Home page
def home_page():
    st.title("Welcome to My Online Library!")
    st.write("Here you can explore featured books and search for the books you want.")

    # Navigation buttons
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        if st.button("Categories"):
            st.session_state.current_page = "Categories"
    
    with col2:
        if st.button("Search for a Book"):
            st.session_state.current_page = "Search for a Book"
    
    with col3:
        if st.button("Authors"):
            st.session_state.current_page = "Authors"
    
    with col4:
        if st.button("Books"):
            st.session_state.current_page = "Books"
    
    with col5:
        if st.button("Wishlist"):
            st.session_state.current_page = "Wishlist"
    
    with col6:
        if st.button("Reviews"):
            st.session_state.current_page = "Reviews"
    
    with col7:
        if st.button("Borrow & Buy"):
            st.session_state.current_page = "Borrow & Buy"

# Categories page
def categories_page():
    back_to_home()  # Button to return to the home page
    st.title("Book Categories")

    # Fetch categories from the database
    crsr.execute("SELECT * FROM Categories")
    categories = crsr.fetchall()

    # Display each category with its books
    for category in categories:
        # Use st.expander to display the category
        with st.expander(f"{category[1]}"):
            # Fetch books in this category
            crsr.execute("""
                SELECT Books.book_name, Books.publication_date, Books.Availability_Status 
                FROM Books 
                WHERE book_id IN (SELECT book_id FROM Categories WHERE category_id = ?)
            """, (category[0],))
            books = crsr.fetchall()
            
            if books:
                st.write(f"Number of books in this category: {len(books)}")
                for book in books:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"{book[0]} - {book[1]} ({book[2]})")
                    with col2:
                        if st.button(f"Add to Wishlist", key=f"add_{book[0]}"):
                            if "wishlist" not in st.session_state:
                                st.session_state.wishlist = []
                            if book not in st.session_state.wishlist:
                                st.session_state.wishlist.append(book)
                                st.success(f"{book[0]} has been added to your wishlist!")
                            else:
                                st.warning("This book is already in your wishlist.")
            else:
                st.write("No books in this category.")

# Search page
def search_page():
    back_to_home()  # Button to return to the home page
    st.title("Search for a Book")

    # Search box
    search_query = st.text_input("Search for a book (by name):")

    if search_query:
        # Search for books matching the book name
        crsr.execute("SELECT * FROM Books WHERE book_name LIKE ?", (f"%{search_query}%",))
        results = crsr.fetchall()
        
        if results:
            st.subheader("Search Results:")
            for book in results:
                st.write(f"{book[1]} - {book[2]} ({book[3]})")
        else:
            st.write("No results found.")

# Authors page
def authors_page():
    back_to_home()  # Button to return to the home page
    st.title("Authors")

    # Fetch the list of authors from the database
    crsr.execute("SELECT * FROM Authors")
    authors = crsr.fetchall()

    # Select an author
    selected_author = st.selectbox("Select an author:", [author[1] for author in authors])

    if selected_author:
        st.subheader(f"Books by {selected_author}")

        # Fetch books by the selected author
        crsr.execute("SELECT * FROM Books WHERE book_id IN (SELECT book_id FROM Authors WHERE author_name = ?)", (selected_author,))
        author_books = crsr.fetchall()
        
        if author_books:
            for book in author_books:
                st.write(f"{book[1]} ({book[2]})")
        else:
            st.write("No books by this author.")

# Books page
def books_page():
    back_to_home()  # Button to return to the home page
    st.title("Books")

    # Fetch all books from the database
    crsr.execute("SELECT * FROM Books")
    books = crsr.fetchall()

    # Display books
    for book in books:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{book[1]} - {book[2]} ({book[3]})")
        with col2:
            if st.button(f"Add to Wishlist", key=f"add_{book[0]}"):
                if "wishlist" not in st.session_state:
                    st.session_state.wishlist = []
                if book not in st.session_state.wishlist:
                    st.session_state.wishlist.append(book)
                    st.success(f"{book[1]} has been added to your wishlist!")
                else:
                    st.warning("This book is already in your wishlist.")

# Wishlist page
def wishlist_page():
    back_to_home()  # Button to return to the home page
    st.title("Wishlist")

    # Display the wishlist
    if "wishlist" in st.session_state and st.session_state.wishlist:
        st.subheader("📚 Books in your wishlist:")
        for i, book in enumerate(st.session_state.wishlist):
            if len(book) >= 3:  # Ensure the book has at least a name and publication date
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"📖 {book[0]} - 🗓 {book[1]} ({book[2]})")  # Book name + publication date
                with col2:
                    if st.button(f"🗑 Remove", key=f"remove_{i}"):
                        st.session_state.wishlist.pop(i)
                        st.success(f"✅ {book[1]} has been removed from your wishlist!")
                        st.rerun()  # Refresh the page after removal
            else:
                st.warning(f"⚠ Error: Incomplete data for this book: {book}")  # Alert for incomplete data
    else:
        st.write("📭 Your wishlist is empty.")

# Reviews page
def reviews_page():
    back_to_home()  # Button to return to the home page
    st.title("Reviews")

    # Select a book
    crsr.execute("SELECT book_name FROM Books")
    book_titles = [book[0] for book in crsr.fetchall()]
    selected_book = st.selectbox("Select a book:", book_titles)

    if selected_book:
        st.subheader(f"Reviews for {selected_book}")

        # Display existing reviews
        crsr.execute("""
            SELECT Reviews.rating, Reviews.comment, Reviews.reviewDate, Reviews.user_id 
            FROM Reviews 
            WHERE Reviews.book_id IN (SELECT book_id FROM Books WHERE book_name = ?)
        """, (selected_book,))
        reviews = crsr.fetchall()
        
        if reviews:
            for review in reviews:
                st.write(f"Rating: {review[0]}")
                st.write(f"Comment: {review[1]}")
                st.write(f"Date: {review[2]}")
                st.write(f"User ID: {review[3]}")
                st.write("---")
        else:
            st.write("No reviews for this book yet.")

        # Add a new review
        st.subheader("Add your review:")
        new_review_user = st.text_input("Your name:")
        new_review_text = st.text_area("Your review:")
        if st.button("Add Review"):
            if new_review_user and new_review_text:
                # Get the book_id for the selected book
                crsr.execute("SELECT book_id FROM Books WHERE book_name = ?", (selected_book,))
                book_id = crsr.fetchone()[0]
                
                # Insert the new review
                crsr.execute("""
                    INSERT INTO Reviews (rating, comment, reviewDate, user_id, book_id) 
                    VALUES (?, ?, ?, ?, ?)
                """, (5, new_review_text, "2024-01-01", 1, book_id))
                db.commit()
                st.success("Your review has been added successfully!")
            else:
                st.warning("Please fill in all fields.")

# Borrow & Buy page
def borrow_buy_page():
    back_to_home()  # Button to return to the home page
    st.title("Borrow & Buy")

    # Fetch all books from the database
    crsr.execute("SELECT * FROM Books")
    books = crsr.fetchall()

    # Select a book
    book_titles = [book[1] for book in books]
    selected_book = st.selectbox("Select a book:", book_titles)

    if selected_book:
        st.subheader(f"Book Details: {selected_book}")

        # Fetch details of the selected book
        crsr.execute("SELECT * FROM Books WHERE book_name = ?", (selected_book,))
        book_details = crsr.fetchone()

        if book_details:
            st.write(f"Book Name: {book_details[1]}")
            st.write(f"Publication Date: {book_details[2]}")
            st.write(f"Availability Status: {book_details[3]}")

            # Select operation (Buy or Borrow)
            operation = st.radio("Select operation:", ["Buy", "Borrow"])

            if operation == "Buy":
                if st.button("Buy Book"):
                    # Record the purchase in the Operations table
                    crsr.execute("""
                        INSERT INTO Operations (operation_name, startDate, endDate)
                        VALUES (?, ?, ?)
                    """, ("Buying", "2024-01-01", ""))
                    operation_id = crsr.lastrowid  # Get the inserted operation_id

                    # Link the operation to the book in the Book_Mangement table
                    crsr.execute("""
                        INSERT INTO Book_Mangement (operation_id, book_id)
                        VALUES (?, ?)
                    """, (operation_id, book_details[0]))
                    db.commit()
                    st.success(f"{selected_book} has been purchased successfully!")

            elif operation == "Borrow":
                # Select borrowing dates
                start_date = st.date_input("Borrow Start Date:")
                end_date = st.date_input("Borrow End Date:")

                if st.button("Borrow Book"):
                    # Record the borrowing in the Operations table
                    crsr.execute("""
                        INSERT INTO Operations (operation_name, startDate, endDate)
                        VALUES (?, ?, ?)
                    """, ("Borrowing", start_date, end_date))
                    operation_id = crsr.lastrowid  # Get the inserted operation_id

                    # Link the operation to the book in the Book_Mangement table
                    crsr.execute("""
                        INSERT INTO Book_Mangement (operation_id, book_id)
                        VALUES (?, ?)
                    """, (operation_id, book_details[0]))
                    db.commit()
                    st.success(f"{selected_book} has been borrowed successfully!")

# Operations page
def operations_page():
    back_to_home()  # Button to return to the home page
    st.title("Operations")

    # Fetch all operations from the database
    crsr.execute("""
        SELECT Operations.operation_id, Operations.operation_name, Operations.startDate, Operations.endDate, Books.book_name 
        FROM Operations 
        JOIN Book_Mangement ON Operations.operation_id = Book_Mangement.operation_id 
        JOIN Books ON Book_Mangement.book_id = Books.book_id
    """)
    operations = crsr.fetchall()

    if operations:
        st.subheader("List of Operations:")
        for operation in operations:
            st.write(f"Operation ID: {operation[0]}")
            st.write(f"Operation Type: {operation[1]}")
            st.write(f"Book Name: {operation[4]}")
            st.write(f"Start Date: {operation[2]}")
            st.write(f"End Date: {operation[3]}")
            st.write("---")
    else:
        st.write("No operations recorded yet.")

# Manage page state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Display the selected page
if st.session_state.current_page == "Home":
    home_page()
elif st.session_state.current_page == "Categories":
    categories_page()
elif st.session_state.current_page == "Search for a Book":
    search_page()
elif st.session_state.current_page == "Authors":
    authors_page()
elif st.session_state.current_page == "Books":
    books_page()
elif st.session_state.current_page == "Wishlist":
    wishlist_page()
elif st.session_state.current_page == "Reviews":
    reviews_page()
elif st.session_state.current_page == "Borrow & Buy":
    borrow_buy_page()
elif st.session_state.current_page == "Operations":
    operations_page()

# Close the database connection when the app is terminated
db.close()