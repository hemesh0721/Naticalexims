from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create the database if it doesn't exist and ensure the table is set up
def init_db():
    conn = sqlite3.connect('contact.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/vegetables')
def vegetables():
    return render_template('vegetables.html')

@app.route('/fruits')
def fruits():
    return render_template('fruits.html')



@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for the contact page
@app.route('/addContact', methods=['GET', 'POST'])
def addContact():
    if request.method == 'POST':
        name = request.form['name']
        mobile=request.form['mobile']
        email = request.form['email']
        
        message = request.form['message']
        
        # Save the details to the database
        conn = sqlite3.connect('contact.db')
        c = conn.cursor()
        c.execute('INSERT INTO contacts (name, mobile, email, message) VALUES (?, ?, ?, ?)',
                  (name, mobile, email, message))
        conn.commit()
        conn.close()
        
        return render_template('thankyou.html')
    return render_template('contact.html')


init_db()
app.run(debug=True)