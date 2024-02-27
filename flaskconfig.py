from flask import Flask, request
from flask_mail import Mail, Message
from supabase import create_client
import hashlib
import os

app = Flask(__name__)

# Supabase Connection
NEXT_PUBLIC_SUPABASE_URL = 'https://zwmhjgftwvkcdirgvxwj.supabase.co'
NEXT_PUBLIC_SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp3bWhqZ2Z0d3ZrY2Rpcmd2eHdqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDkwNTQ2NTAsImV4cCI6MjAyNDYzMDY1MH0.Of7v3vo-zPdfTbN2o9vfk5_U3kEtMUTo1tS-JQDlOmI'
supabase = create_client(NEXT_PUBLIC_SUPABASE_URL,
                         NEXT_PUBLIC_SUPABASE_ANON_KEY)

# Gmail Connection
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'matthewfernandez0@gmail.com'
app.config['MAIL_PASSWORD'] = '$yZal$%3PT8U0e2fDLn2'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # Generate a secret key for Flask
mail = Mail(app)


def hash_password(password):
    # Encode the password string to bytes
    password_bytes = password.encode('utf-8')

    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the password bytes
    sha256_hash.update(password_bytes)

    # Get the hexadecimal representation of the hashed password
    hashed_password = sha256_hash.hexdigest()

    return hashed_password


def send_confirmation_email(email, password):
    token = os.urandom(16).hex()  # Generate a random token
    supabase.table('ld4nj.sub_user').insert(
        {'email': email, 'password': password, 'confirmation_token': token}).execute()  # Store token in Supabase

    msg = Message('Confirm Your Email',
                  sender='noreply@lawdigestNJ.com', recipients=[email])
    msg.body = f'Please click the following link to confirm your email: {app.url_for("confirm_email", token=token, _external=True)}'
    mail.send(msg)


@app.route("/register", methods=['POST'])
def register():
    email = request.form['Email']
    password = request.form['Password']

    # Check if email is already registered
    user_exists = supabase.table('ld4nj.sub_user').select(
        'email').eq('email', email).execute()

    if user_exists:
        return 'Email already registered'
    else:
        hash = hash_password(password)
        send_confirmation_email(email, hash)
        return 'Registration successful. Please check your email to confirm your account.'


@app.route('/confirm_email/<token>')
def confirm_email(token):
    # Verify the token and update user's account status as confirmed
    # This step is omitted for brevity
    return 'Email confirmed successfully'


if __name__ == '__main__':
    app.run(debug=True)