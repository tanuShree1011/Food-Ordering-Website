from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages and session

# Data for canteens
menus = {
    1: {
        "name": "Canteen 1 ",
        "items": [
            {"name": "Dosa", "price": 50, "image": "canteen1/dosa.jpg"},
            {"name": "Idli", "price": 40, "image": "canteen1/idli.jpg"},
            {"name": "Uttapam", "price": 60, "image": "canteen1/uttapam.jpg"},
            {"name": "Vada", "price": 30, "image": "canteen1/vada.jpg"},
            {"name": "Sambar Rice", "price": 70, "image": "canteen1/sambar_rice.jpg"},
            {"name": "Curd Rice", "price": 60, "image": "canteen1/curd_rice.jpg"},
            {"name": "Noodles", "price": 40, "image": "canteen1/noodles.jpg"},
            {"name": "Upma", "price": 35, "image": "canteen1/upma.jpg"},
            {"name": "Appam", "price": 40, "image": "canteen1/appam.jpg"},
           
           
        ]
    },
    2: {
        "name": "Canteen 2 ",
        "items": [
            {"name": "Vegetable Sandwich", "price": 80, "image": "canteen2/veg_sandwich.jpg"},   
            {"name": "Pizza", "price": 100, "image": "canteen2/pizza.jpg"},
            {"name": "Egg Roll", "price": 100, "image": "canteen2/egg_roll.jpg"},
            {"name": "Veg Burger", "price": 90, "image": "canteen2/veg_burger.jpg"},
            {"name": "Cheese Sandwich", "price": 100, "image": "canteen2/cheese_sandwich.jpg"},
            {"name": "Cheese Burger", "price": 120, "image": "canteen2/cheese_burger.jpg"},
            {"name": "Veg Wrap", "price": 110, "image": "canteen2/veg_wrap.jpg"},
            {"name": "Paneer Wrap", "price": 130, "image": "canteen2/paneer_wrap.jpg"},
            {"name": "French Fries", "price": 60, "image": "canteen2/french_fries.jpg"},
            
        ]
    },
    3: {
        "name": "Canteen 3 ",
        "items": [
            {"name": "Chicken Curry", "price": 150, "image": "canteen3/chicken_curry.jpg"},
            {"name": "Fried Rice", "price": 180, "image": "canteen3/fried_rice.jpg"},
            {"name": "Egg Curry", "price": 120, "image": "canteen3/egg_curry.jpg"},
            {"name": "Chicken Biryani", "price": 200, "image": "canteen3/chicken_biryani.jpg"},
            {"name": "Egg Noodles", "price": 100, "image": "canteen3/egg_noodles.jpg"},
            {"name": "Samosa", "price": 20, "image": "canteen3/samosa.jpg"},
            {"name": "Kachori", "price": 25, "image": "canteen3/kachori.jpg"},
            {"name": "Chicken 65", "price": 150, "image": "canteen3/chicken_65.jpg"},
            {"name": "Gobi Rice", "price": 150, "image": "canteen3/gobi_rice.jpg"},
           
        ]
    }
}

# Initialize the database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# Home route to display login page
@app.route('/')
def login_page():
    return render_template('login.html')

# Login route to process the form submission
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Check if email exists
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Check if password matches
            if check_password_hash(user[2], password):  # user[2] is the hashed password
                # Check if role matches
                if role == 'admin' and user[3] == 'admin':  # Check if the role is admin
                    session['email'] = email
                    session['role'] = role
                    #print("Admin login successful!")
                    return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
                elif role == 'user' and user[3] == 'user':  # Check if the role is user
                    session['email'] = email
                    session['role'] = role
                    #flash("User login successful!")
                    return redirect(url_for('dashboard'))  # Redirect to user dashboard
                else:
                    flash("Role mismatch! Please select the correct role.")
            else:
                flash("Incorrect password!")
        else:
            flash("Email not found!")

        return redirect(url_for('login'))

    return render_template('login.html')

# Dashboard route (only accessible after login)
@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        flash('You must be logged in to access the dashboard.')
        return redirect(url_for('login_page'))
    return render_template('dashboard.html', email=session['email'])

# Register route to handle new user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register'))

        # Check if email already exists
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email already exists! Please choose a different email.")
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (email, password, role) VALUES (?, ?, ?)', 
                       (email, hashed_password, role))
        conn.commit()
        conn.close()

        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/canteen/1', methods=['GET'])
def canteen1():
    return render_template('canteen1.html')

@app.route('/canteen/2')
def canteen2():
    # This will render the canteen2.html file for Cafe food
    return render_template('canteen2.html')

@app.route('/canteen/3')
def canteen3():
    # This will render the canteen3.html file for Non-Veg food
    return render_template('canteen3.html')

import random  # To generate the token number

@app.route('/checkout', methods=['POST'])
def checkout():
    # Get the total amount from the form
    total_amount = request.form.get('total_amount')
    
    # Initialize an empty list to store the cart items
    cart_items = []

    # Loop through each item in the form
    index = 0
    while f'item_name_{index}' in request.form:
        item_name = request.form.get(f'item_name_{index}')
        item_price = request.form.get(f'item_price_{index}')
        item_quantity = request.form.get(f'item_quantity_{index}')
        
        cart_items.append({
            'name': item_name,
            'price': float(item_price),
            'quantity': int(item_quantity)
        })
        index += 1

    # Generate a random token number on the server-side
    token_number = random.randint(1000, 9999)

    # Save the order to the database
    try:
        conn = sqlite3.connect('canteen.db')
        cursor = conn.cursor()

        # Ensure the orders table exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token_number INTEGER NOT NULL,
                cart_items TEXT NOT NULL,
                total_amount REAL NOT NULL
            )
        ''')

        # Convert the cart items to a string format for storage
        cart_items_str = str(cart_items)

        # Insert the order into the table with the generated token number
        cursor.execute('''
            INSERT INTO orders (token_number, cart_items, total_amount)
            VALUES (?, ?, ?)
        ''', (token_number, cart_items_str, total_amount))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving order to database: {e}")

    # Render the checkout page with the cart, total amount, and token number
    return render_template('checkout.html', cart=cart_items, total_amount=total_amount, token_number=token_number)

@app.route('/check', methods=['POST'])
def check():
    cart_items = request.form.get('cart_items')
    total_amount = request.form.get('total_amount')
    token_number = random.randint(1000, 9999)

    # Save order to the database
    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (token_number, cart_items, total_amount)
        VALUES (?, ?, ?)
    ''', (token_number, cart_items, total_amount))
    conn.commit()
    conn.close()

    return render_template('confirmation.html', token_number=token_number)

@app.route('/admin_dashboard')
def admin_dashboard():
    # Fetch orders from the database
    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()
    cursor.execute('SELECT token_number, cart_items, total_amount FROM orders')
    orders = cursor.fetchall()
    conn.close()

    # Pass orders to the admin dashboard
    return render_template('admin_dashboard.html', orders=orders)


@app.route('/logout')
def logout():
    session.pop('email', None)  # Remove email from the session
    flash('You have been logged out.')
    return redirect(url_for('login_page'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)





