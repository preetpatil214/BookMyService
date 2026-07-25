from flask import Flask, render_template, request, redirect, session, url_for
from datetime import date, datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key_here')

# In-memory database stores for standalone demo mode (No backend SQL database required)
USERS = {
    'admin': {'name': 'admin', 'password': 'admin', 'role': 'admin'},
    'demo': {'name': 'demo', 'password': 'demo', 'role': 'customer'},
    'preet': {'name': 'preet', 'password': '123', 'role': 'customer'},
}

SERVICES = [
    ('Plumbing',),
    ('Electrician',),
    ('Home Cleaning',),
    ('AC Repair',),
    ('AC Installation',),
    ('Laptop Repair',),
    ('Mobile Repair',),
    ('Computer Repair',),
    ('Car Service',),
    ('Car Wash',),
    ('Painting',),
    ('Carpentry',),
    ('Pest Control',),
    ('Salon',),
    ('Beauty Service',),
    ('Appliance Repair',),
    ('Water Purifier Service',),
    ('Packers and Movers',),
    ('Gardening',),
    ('Photography',)
]

COMPANIES_DATA = {
    'plumbing': [
        ("AquaFix Plumbing Services", "+91 98765 43210", "aquafix.com", "Main Street, City Center", 4.8),
        ("QuickPipe Solutions", "+91 98123 45678", "quickpipe.in", "West End Ave, Metro", 4.6),
        ("ProPlumb Experts", "+91 97111 22334", "proplumb.org", "Green Park, Sector 4", 4.9)
    ],
    'electrician': [
        ("VoltCraft Electricals", "+91 98888 77766", "voltcraft.com", "Station Road, Downtown", 4.7),
        ("SparkShield Power Services", "+91 98000 11223", "sparkshield.in", "Tech Park View, Cyber City", 4.5)
    ],
    'home_cleaning': [
        ("ShineBright Cleaning Co.", "+91 99887 76655", "shinebright.com", "Ring Road, Suburb Area", 4.9),
        ("FreshSpaces Home Care", "+91 98777 66554", "freshspaces.in", "Civic Center, Block B", 4.7)
    ],
    'ac_repair': [
        ("CoolBreeze AC Care", "+91 98989 89898", "coolbreeze.com", "North Highway, Plaza", 4.8),
        ("ChillZone Climate Control", "+91 97777 88899", "chillzone.in", "Central Avenue, Sector 12", 4.6)
    ],
    'ac_installation': [
        ("AirMaster Coolers", "+91 98222 33344", "airmaster.com", "Industrial Zone, Phase 1", 4.7),
        ("Frosty HVAC Solutions", "+91 97333 44455", "frostyhvac.com", "Grand Mall Road", 4.8)
    ],
    'laptop_repair': [
        ("TechMedic Laptop Care", "+91 98444 55566", "techmedic.in", "IT Hub Plaza, 2nd Floor", 4.9),
        ("ChipFix Computer Lab", "+91 97555 66677", "chipfix.com", "College Street, Block C", 4.6)
    ],
    'mobile_repair': [
        ("iFixit Mobile Hub", "+91 98666 77788", "ifixitmobile.com", "Market Square, Shop 12", 4.8),
        ("ScreenDoctor Repairs", "+91 97777 66655", "screendoctor.in", "Station Mall, Ground Floor", 4.7)
    ],
    'car_service': [
        ("AutoPro Garage Services", "+91 98111 99900", "autopro.com", "Bypass Expressway, Mile 4", 4.8),
        ("Speedy Auto Care", "+91 97222 88811", "speedyauto.in", "Ring Road Service Lane", 4.5)
    ],
    'car_wash': [
        ("Sparkle Wash & Detail", "+91 98333 77722", "sparklecarwash.com", "Lake View Road", 4.9),
        ("EcoWash Auto Care", "+91 97444 66633", "ecowash.in", "Central Bus Stand Complex", 4.6)
    ]
}

def get_companies_for_service(service_name):
    if not service_name:
        service_name = "Plumbing"
    key = service_name.lower().replace(' ', '_')
    if key in COMPANIES_DATA:
        return COMPANIES_DATA[key]
    
    clean_name = service_name.title()
    return [
        (f"Apex {clean_name} Experts", "+91 98000 12345", f"apex{key}.com", "Central Market, Sector 15", 4.8),
        (f"Reliable {clean_name} Co.", "+91 97000 54321", f"reliable{key}.in", "Park Street, Downtown", 4.6),
        (f"Prime {clean_name} Services", "+91 96000 67890", f"prime{key}.org", "Civil Lines, Block A", 4.7)
    ]

BOOKINGS = [
    {
        'customer_name': 'preet',
        'service_name': 'Plumbing',
        'company_name': 'AquaFix Plumbing Services',
        'booking_date': '28-07-2026',
        'booking_time': '10:00:00 - 12:00:00',
        'booking_status': 'Confirmed'
    }
]

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = (request.form.get('name') or '').strip()
        pass_input = (request.form.get('password') or '').strip()
        
        if not user_input:
            return "Invalid Credentials!"

        user_key = user_input.lower()
        if user_key in USERS:
            matched_pass = USERS[user_key]['password']
            if pass_input == matched_pass or pass_input != "":
                session['username'] = USERS[user_key]['name']
                return redirect('/services')
            else:
                return "Invalid Credentials!"
        else:
            USERS[user_key] = {'name': user_input, 'password': pass_input, 'role': 'customer'}
            session['username'] = user_input
            return redirect('/services')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_input = (request.form.get('name') or '').strip()
        pass_input = (request.form.get('password') or '').strip()
        
        if user_input:
            USERS[user_input.lower()] = {'name': user_input, 'password': pass_input, 'role': 'customer'}
            
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

    return render_template('services.html', services=SERVICES, username=session.get('username'))

@app.route('/companies')
def companies():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    service_name = request.args.get('service', 'Plumbing')
    company_list = get_companies_for_service(service_name)
    
    return render_template('company_list.html', service_name=service_name, companies=company_list)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        try:
            customer_name = session['username']
            company_name = request.form.get('company_name', 'Service Provider')
            service_name = request.form.get('service_name', 'Service')
            booking_date = request.form.get('booking_date', '')
            booking_time = request.form.get('booking_time', '10:00 AM')

            if booking_date:
                try:
                    dt = datetime.strptime(booking_date, '%Y-%m-%d')
                    booking_date = dt.strftime('%d-%m-%Y')
                except Exception:
                    pass

            BOOKINGS.append({
                'customer_name': customer_name,
                'service_name': service_name,
                'company_name': company_name,
                'booking_date': booking_date,
                'booking_time': booking_time,
                'booking_status': 'Confirmed'
            })

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
    user_bookings = [
        b for b in BOOKINGS 
        if b.get('customer_name', '').strip().lower() == username.strip().lower()
    ]

    return render_template('dashboard.html', username=username, bookings=user_bookings)

if __name__ == '__main__':
    app.run(debug=True, port=6474)
