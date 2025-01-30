from flask import Flask, render_template, request, redirect
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

# Function to send email to the admin
def send_email_to_admin(name, mobile, email, message):
    # Admin email configuration
    admin_email = "anilbommineni123@gmail.com"
    sender_email = "hemesh0721@gmail.com"
    sender_password = "Hemesh@2001"  # Use a secure method to handle the password

    # SMTP server details (Example for Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create the email message
    subject = "New Contact Us Form Submission"
    body = f"""
    New contact form submission:
    Name: {name}
    Mobile: {mobile}
    Email: {email}
    Message: {message}
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = admin_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Encrypt the connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, admin_email, msg.as_string())
        server.quit()
        print("Email sent successfully to admin!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Route for the homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/vegetables")
def vegetables():
    return render_template("vegetables.html")

@app.route("/fruits")
def fruits():
    return render_template("fruits.html")

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for the contact page
@app.route('/addContact', methods=['GET', 'POST'])
def addContact():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        message = request.form['message']
        
        # Save the details to the database
        conn = sqlite3.connect('contact.db')
        c = conn.cursor()
        c.execute('INSERT INTO contacts (name, mobile, email, message) VALUES (?, ?, ?, ?)',
                  (name, mobile, email, message))
        conn.commit()
        conn.close()
        
        # Send email to the admin
        send_email_to_admin(name, mobile, email, message)
        
        return render_template('thankyou.html')
    return render_template('contact.html')


init_db()
app.run(debug=True)
