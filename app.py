from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
from dotenv import load_dotenv  # If you're using .env

load_dotenv()

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def send_email_oauth(sender_email, recipient_email, subject, body):
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise ValueError("Google credentials not found in environment variables.")
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    message = MIMEMultipart()
    message['To'] = recipient_email
    message['From'] = sender_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    raw_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        service.users().messages().send(userId='me', body=raw_message).execute()
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

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

@app.route('/fmg')
def fmg():
    return render_template('fmg.html')

@app.route('/addContact', methods=['GET', 'POST'])
def addContact():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        message = request.form['message']

        conn = sqlite3.connect('contact.db')
        c = conn.cursor()
        c.execute('INSERT INTO contacts (name, mobile, email, message) VALUES (?, ?, ?, ?)',
                  (name, mobile, email, message))
        conn.commit()
        conn.close()

        sender_email = os.environ.get("GOOGLE_CLIENT_ID")
        if not sender_email:
            raise ValueError("Sender email not found in environment variable SENDER_EMAIL")

        recipient_email = "anilbommineni123@gmail.com"
        subject = f"New Contact Form Submission from {name}"
        body = f"Name: {name}\nMobile: {mobile}\nEmail: {email}\nMessage: {message}"

        try:
            send_email_oauth(sender_email, recipient_email, subject, body)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")
            return render_template('error.html', error_message="Error sending email. Please try again later.")

        return render_template('thankyou.html')

    return render_template('contact.html')

init_db()

if __name__ == '__main__':
    app.run(debug=True)