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
        ("Urban Company", "+91 98765 43210", "urbancompany.com", "Thane West, Mumbai", 4.8),
        ("NoBroker Home Services", "+91 98123 45678", "nobroker.in", "Powai, Mumbai", 4.7),
        ("HomeTriangle", "+91 97111 22334", "hometriangle.com", "Andheri East, Mumbai", 4.6),
        ("Housejoy", "+91 98234 55667", "housejoy.in", "Navi Mumbai", 4.5),
        ("Sulekha", "+91 98345 66778", "sulekha.com", "Dadar, Mumbai", 4.6)
    ],

    'electrician': [
        ("Urban Company", "+91 98888 77766", "urbancompany.com", "Thane West, Mumbai", 4.8),
        ("NoBroker Home Services", "+91 98000 11223", "nobroker.in", "Powai, Mumbai", 4.7),
        ("HomeTriangle", "+91 98111 44556", "hometriangle.com", "Andheri East, Mumbai", 4.6),
        ("Housejoy", "+91 98222 33445", "housejoy.in", "Navi Mumbai", 4.5),
        ("Sulekha", "+91 98333 22334", "sulekha.com", "Dadar, Mumbai", 4.6)
    ],

    'home_cleaning': [
        ("Urban Company", "+91 99887 76655", "urbancompany.com", "Thane West, Mumbai", 4.9),
        ("NoBroker Home Services", "+91 98777 66554", "nobroker.in", "Powai, Mumbai", 4.8),
        ("HomeTriangle", "+91 98444 12345", "hometriangle.com", "Andheri East, Mumbai", 4.7),
        ("Housejoy", "+91 98555 23456", "housejoy.in", "Navi Mumbai", 4.6),
        ("HiCare", "+91 98666 34567", "hicare.in", "Mulund, Mumbai", 4.8)
    ],

    'ac_repair': [
        ("Blue Star Service", "+91 98989 89898", "bluestarindia.com", "Thane West, Mumbai", 4.8),
        ("Voltas Service", "+91 97777 88899", "voltas.com", "Powai, Mumbai", 4.7),
        ("Daikin Service", "+91 97888 22334", "daikinindia.com", "Andheri East, Mumbai", 4.8),
        ("LG Service Centre", "+91 97999 33445", "lg.com/in", "Navi Mumbai", 4.7),
        ("Urban Company", "+91 98123 98765", "urbancompany.com", "Dadar, Mumbai", 4.8)
    ],

    'ac_installation': [
        ("Blue Star Service", "+91 98222 33344", "bluestarindia.com", "Thane West, Mumbai", 4.8),
        ("Voltas Service", "+91 97333 44455", "voltas.com", "Powai, Mumbai", 4.7),
        ("Daikin Service", "+91 97444 55566", "daikinindia.com", "Andheri East, Mumbai", 4.8),
        ("Carrier Service", "+91 97555 66677", "carrier.com", "Navi Mumbai", 4.7),
        ("Urban Company", "+91 97666 77788", "urbancompany.com", "Mulund, Mumbai", 4.8)
    ],

    'laptop_repair': [
        ("HP Service Centre", "+91 98444 55566", "hp.com", "Thane West, Mumbai", 4.8),
        ("Dell Service Centre", "+91 97555 66677", "dell.com", "Powai, Mumbai", 4.8),
        ("Lenovo Service Centre", "+91 98666 77788", "lenovo.com", "Andheri East, Mumbai", 4.7),
        ("ASUS Service Centre", "+91 98777 88899", "asus.com", "Navi Mumbai", 4.7),
        ("Acer Service Centre", "+91 98888 99900", "acer.com", "Dadar, Mumbai", 4.6)
    ],

    'mobile_repair': [
        ("Cashify", "+91 98666 77788", "cashify.in", "Thane West, Mumbai", 4.8),
        ("Samsung Service Centre", "+91 97777 66655", "samsung.com/in", "Powai, Mumbai", 4.8),
        ("Apple Authorized Service Centre", "+91 97888 55544", "apple.com/in", "BKC, Mumbai", 4.9),
        ("Xiaomi Service Centre", "+91 97999 44433", "mi.com/in", "Navi Mumbai", 4.7),
        ("OnePlus Service Centre", "+91 98000 33322", "oneplus.in", "Andheri East, Mumbai", 4.7)
    ],

    'computer_repair': [
        ("HP Service Centre", "+91 98111 22211", "hp.com", "Thane West, Mumbai", 4.8),
        ("Dell Service Centre", "+91 98222 11122", "dell.com", "Powai, Mumbai", 4.8),
        ("Lenovo Service Centre", "+91 98333 22233", "lenovo.com", "Andheri East, Mumbai", 4.7),
        ("ASUS Service Centre", "+91 98444 33344", "asus.com", "Navi Mumbai", 4.7),
        ("Acer Service Centre", "+91 98555 44455", "acer.com", "Dadar, Mumbai", 4.6)
    ],

    'car_service': [
        ("GoMechanic", "+91 98111 99900", "gomechanic.in", "Thane West, Mumbai", 4.8),
        ("Bosch Car Service", "+91 97222 88811", "boschcarservice.com", "Andheri East, Mumbai", 4.8),
        ("Mahindra First Choice", "+91 97333 77722", "mahindrafirstchoice.com", "Navi Mumbai", 4.7),
        ("myTVS", "+91 97444 66633", "mytvs.in", "Powai, Mumbai", 4.7),
        ("Maruti Suzuki Service", "+91 97555 55544", "marutisuzuki.com", "Mulund, Mumbai", 4.9)
    ],

    'car_wash': [
        ("3M Car Care", "+91 98333 77722", "3mcarcare.com", "Thane West, Mumbai", 4.9),
        ("GoMechanic", "+91 97444 66633", "gomechanic.in", "Andheri East, Mumbai", 4.8),
        ("CarzSpa", "+91 97555 12345", "carzspa.com", "Powai, Mumbai", 4.8),
        ("myTVS", "+91 97666 23456", "mytvs.in", "Navi Mumbai", 4.7),
        ("Mahindra First Choice", "+91 97777 34567", "mahindrafirstchoice.com", "Mulund, Mumbai", 4.7)
    ],

    'painting': [
        ("Asian Paints Safe Painting Service", "+91 98111 11111", "asianpaints.com", "Mumbai", 4.9),
        ("Berger Express Painting", "+91 98222 22222", "bergerpaints.com", "Thane", 4.8),
        ("Nerolac Painting Service", "+91 98333 33333", "nerolac.com", "Andheri", 4.7),
        ("Urban Company", "+91 98444 44444", "urbancompany.com", "Powai", 4.8),
        ("HomeTriangle", "+91 98555 55555", "hometriangle.com", "Navi Mumbai", 4.6)
    ],

    'carpentry': [
        ("Urban Company", "+91 98666 11111", "urbancompany.com", "Mumbai", 4.8),
        ("NoBroker Home Services", "+91 98777 22222", "nobroker.in", "Thane", 4.7),
        ("HomeTriangle", "+91 98888 33333", "hometriangle.com", "Andheri", 4.6),
        ("Housejoy", "+91 98999 44444", "housejoy.in", "Navi Mumbai", 4.5),
        ("Sulekha", "+91 98000 55555", "sulekha.com", "Powai", 4.6)
    ],

    'pest_control': [
        ("Rentokil PCI", "+91 98123 12345", "rentokil-pestcontrolindia.com", "Mumbai", 4.9),
        ("HiCare", "+91 98234 23456", "hicare.in", "Thane", 4.8),
        ("Pest Control India", "+91 98345 34567", "pciindia.com", "Andheri", 4.8),
        ("Godrej Pest Control", "+91 98456 45678", "godrej.com", "Powai", 4.7),
        ("Urban Company", "+91 98567 56789", "urbancompany.com", "Navi Mumbai", 4.7)
    ],

    'salon': [
        ("Naturals Salon", "+91 98678 67890", "naturals.in", "Thane", 4.8),
        ("Lakme Salon", "+91 98789 78901", "lakmesalon.in", "Andheri", 4.8),
        ("Jawed Habib", "+91 98890 89012", "jawedhabib.co.in", "Powai", 4.7),
        ("Enrich Salon", "+91 98901 90123", "enrich.co.in", "Navi Mumbai", 4.8),
        ("TONI&GUY", "+91 98012 01234", "toniandguyindia.com", "Bandra", 4.9)
    ],

    'beauty_service': [
        ("Lakme Salon", "+91 98123 45670", "lakmesalon.in", "Thane", 4.8),
        ("Naturals Salon", "+91 98234 56781", "naturals.in", "Andheri", 4.8),
        ("VLCC", "+91 98345 67892", "vlcc.com", "Powai", 4.7),
        ("Urban Company", "+91 98456 78903", "urbancompany.com", "Navi Mumbai", 4.8),
        ("Enrich Salon", "+91 98567 89014", "enrich.co.in", "Bandra", 4.8)
    ],

    'appliance_repair': [
        ("Urban Company", "+91 98678 90125", "urbancompany.com", "Mumbai", 4.8),
        ("OneAssist", "+91 98789 01236", "oneassist.in", "Thane", 4.7),
        ("Onsitego", "+91 98890 12347", "onsitego.com", "Andheri", 4.8),
        ("LG Service Centre", "+91 98901 23458", "lg.com/in", "Powai", 4.8),
        ("Samsung Service Centre", "+91 98012 34569", "samsung.com/in", "Navi Mumbai", 4.8)
    ],

    'water_purifier_service': [
        ("Kent Service", "+91 98111 11112", "kent.co.in", "Thane", 4.8),
        ("Aquaguard Service", "+91 98222 22223", "eurekaforbes.com", "Mumbai", 4.9),
        ("Livpure Service", "+91 98333 33334", "livpure.com", "Powai", 4.7),
        ("AO Smith Service", "+91 98444 44445", "aosmithindia.com", "Andheri", 4.7),
        ("Urban Company", "+91 98555 55556", "urbancompany.com", "Navi Mumbai", 4.7)
    ],

    'packers_and_movers': [
        ("Agarwal Packers and Movers", "+91 98666 66667", "agarwalpackers.com", "Mumbai", 4.9),
        ("Porter", "+91 98777 77778", "porter.in", "Thane", 4.8),
        ("Leo Packers and Movers", "+91 98888 88889", "leopackersindia.com", "Andheri", 4.7),
        ("Gati Packers and Movers", "+91 98999 99990", "gati.com", "Navi Mumbai", 4.7),
        ("NoBroker Packers and Movers", "+91 98000 00001", "nobroker.in", "Powai", 4.8)
    ],

    'gardening': [
        ("Ugaoo", "+91 98123 11122", "ugaoo.com", "Mumbai", 4.8),
        ("GreenMyLife", "+91 98234 22233", "greenmylife.in", "Thane", 4.7),
        ("Urban Company", "+91 98345 33344", "urbancompany.com", "Andheri", 4.7),
        ("HomeTriangle", "+91 98456 44455", "hometriangle.com", "Powai", 4.6),
        ("Ferns N Petals", "+91 98567 55566", "fnp.com", "Navi Mumbai", 4.6)
    ],

    'photography': [
        ("Canvera", "+91 98678 66677", "canvera.com", "Mumbai", 4.8),
        ("Weddingz", "+91 98789 77788", "weddingz.in", "Thane", 4.7),
        ("WedMeGood", "+91 98890 88899", "wedmegood.com", "Andheri", 4.8),
        ("ShaadiSaga", "+91 98901 99910", "shaadisaga.com", "Powai", 4.7),
        ("Better Photography", "+91 98012 00021", "betterphotography.in", "Bandra", 4.8)
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
