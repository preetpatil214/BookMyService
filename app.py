from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="preet@1414",
        database="sps"
    )

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = (request.form.get('name') or '').strip()
        pass_input = (request.form.get('password') or '').strip()
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user WHERE TRIM(name) = %s AND TRIM(password) = %s", 
            (user_input, pass_input)
        )
        user_account = cursor.fetchone()
        cursor.close()
        db.close()
        
        if user_account:
            session['username'] = user_account['name'].strip()
            return redirect('/services')
        else:
            return "Invalid Credentials!"
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_input = (request.form.get('name') or '').strip()
        pass_input = (request.form.get('password') or '').strip()
        role_input = 'customer'
        
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO user (name, password, role) VALUES (%s, %s, %s)", 
            (user_input, pass_input, role_input)
        )
        db.commit()
        cursor.close()
        db.close()
        
        return redirect('/login')
        
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/services')
def services():
    if 'username' not in session:
        return redirect('/login')
        
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT service_name FROM services")
    all_services = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('services.html', services=all_services, username=session.get('username'))

@app.route('/companies')
def companies():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    service_name = request.args.get('service')
    table_name = service_name.lower().replace(' ', '_')
    
    db = get_db_connection()
    cursor = db.cursor()
    # Fetching company name, contact, website, address, and rating for the service table
    cursor.execute(f"SELECT company_name, contact_no, website, address, rating FROM `{table_name}`")
    company_list = cursor.fetchall()
    cursor.close()
    db.close()
    
    return render_template('company_list.html', service_name=service_name, companies=company_list)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        try:
            customer_name = session['username']
            company_name = request.form.get('company_name')
            service_name = request.form.get('service_name')
            booking_date = request.form.get('booking_date')
            booking_time = request.form.get('booking_time')

            db = get_db_connection()
            cursor = db.cursor()
            query = """
                INSERT INTO bookings (customer_name, service_name, company_name, booking_date, booking_time, booking_status)
                VALUES (%s, %s, %s, %s, %s, 'Confirmed')
            """
            cursor.execute(query, (customer_name, service_name, company_name, booking_date, booking_time))
            db.commit()
            cursor.close()
            db.close()

            return redirect('/dashboard')
        except Exception as e:
            print(f"Error while booking: {e}")
            return f"An error occurred: {e}"

    company_name = request.args.get('company_name', '')
    service_name = request.args.get('service', '')
    return render_template('book.html', company_name=company_name, service_name=service_name)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT 
            customer_name,
            service_name,
            company_name,
            booking_date,
            booking_time,
            booking_status
        FROM bookings
        WHERE TRIM(customer_name) = %s
    """
    cursor.execute(query, (username,))
    user_bookings = cursor.fetchall()
    
    for b in user_bookings:
        if isinstance(b.get('booking_date'), (date, datetime)):
            b['booking_date'] = b['booking_date'].strftime('%d-%m-%Y')

    cursor.close()
    db.close()

    return render_template('dashboard.html', username=username, bookings=user_bookings)

if __name__ == '__main__':
    app.run(debug=True, port=6474)