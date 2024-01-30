from flask import Flask, render_template, redirect, url_for, session, flash, get_flashed_messages, request
from __main__ import app
from db_connector import Database
import re
import hashlib
db = Database()

# Home page route
@app.route('/')
def index():
    return render_template('index.html')


# Register account route
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Get user input from form
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        username_pattern = "^[A-Za-z0-9_]+$"
        existing_username = db.queryDB('SELECT * FROM users WHERE username = ?', [username])
        existing_email = db.queryDB('SELECT * FROM users WHERE email = ?', [hashlib.md5(str(email).encode()).hexdigest()])

        # Validate user input
        if not re.match(username_pattern, username):
            flash("Username must be only alphanumeric characters and '_'")
        elif not len(username) > 5 or not len(username) < 12:
            flash("Username must be between 5 and 12 characters")
        elif not len(email) > 8 or not len(email) < 36:
            flash("Email must be between 8 and 36 characters")
        elif not "@" and "." not in email:
            flash("You must provide a valid email")
        elif not len(password) > 6 and len(password) < 36:
            flash("Password must be between 6 and 36 characters")
        elif not password == confirm_password:
            flash("Passwords must match")
        elif existing_username:
            flash("Username already in use")
        elif existing_email:
            flash("Email already in use")
        else:
            # Hash sensitive user data
            hashed_password = hashlib.md5(str(password).encode()).hexdigest()
            hashed_email = hashlib.md5(str(email).encode()).hexdigest()
            # Insert user information into users table
            db.updateDB('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', [username, hashed_email, hashed_password])
            # Redirect user to the login page
            return redirect(url_for('login'))

    # Return the register page
    return render_template('register.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Get the form data
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.md5(str(password).encode()).hexdigest()

        # Query for user account information
        user_account = db.queryDB('SELECT * FROM users WHERE username = ?', [username])
        stored_password = user_account[0][-1]

        # Validate user input
        if not user_account:
            flash("Account does not exist")
        if not stored_password == hashed_password:
            flash("Incorrect password")
        else:
            # Add user to the session dictionary
            session["user"] = username
            return redirect(url_for('index'))
    
    # If the user is already logged in
    if 'user' in session:
        return redirect(url_for('index'))
        
    return render_template('login.html')
        

# Logout route
@app.route('/logout')
def logout():
    # Iterate through each key in the session and pop it
    for key in list(session.keys()):
        session.pop(key)

    return redirect(url_for('index'))