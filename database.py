import sqlite3

def init_db():
    conn = sqlite3.connect('book_register.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        genre TEXT,
        publisher TEXT,
        isbn TEXT  
)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        student_id TEXT UNIQUE
)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS rentals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        student_id INTEGER,
        rent_date TEXT,
        return_date TEXT,
        FOREIGN KEY(book_id) REFERENCES books(id),
        FOREIGN KEY(student_id) REFERENCES students(id)
)''')
    
    conn.commit()
    conn.close