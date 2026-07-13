#-------------------------------------DB connection----------------------------------------
import mysql.connector
from datetime import date, time
p=input("Enter your SQL password: ")
mydb=mysql.connector.connect(host="localhost",
                          user="root",
                          password=p,
                          database="sps")
cursor=mydb.cursor()
#======================================================================
print("=============BOOK MY SERVICE==============")
print("-------------Your service,Your Schedule!!!--------------")

def login():
    while True:
        print("\n===========LOGIN============")
        name=input("Enter Your Name:")
        password=input("Enter Password:")
        role = input("Enter Role : ").lower()
        cursor.execute("select * from user where name=%s and password=%s",(name,password))
        d=cursor.fetchone()
        if d:
            if d[2] == "admin":
                admin_menu()
                break
            elif d[2] == "customer":
                customer_menu(name)
                break
            else:
                print("Invalid Role")
        else:
            print("Invalid Credentials!! : Account Not Found")
            x=input("Would you like to sign up? (yes/no) : ").lower()
            if x=="yes":
                name=input("Enter Your Name:")
                password=input("Enter Password:")
                cursor.execute("insert into user (name,password,role) values (%s,%s,%s)",(name,password,"customer"))
                mydb.commit()
                print("Registration successful !!!")
                print("Please login with your new account.\n")


#==========================Customer Menu====================================
def customer_menu(name):
    while True:
        print("\n==========Services Currently Available==========")
        cursor.execute("select * from services order by service_no")
        service = cursor.fetchall()
        for i in service:
            print(f"{i[1]}----{i[0]}")
        print("21----View My Bookings")
        print("22----Logout")

        try:
            choice = int(input("\nEnter Choice / Service Number: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            plumbing(name)
        elif choice == 2:
            electrician(name)
        elif choice == 3:
            home_cleaning(name)
        elif choice == 4:
            ac_repair(name)
        elif choice == 5:
            ac_installation(name)
        elif choice == 6:
            laptop_repair(name)
        elif choice == 7:
            mobile_repair(name)
        elif choice == 8:
            computer_repair(name)
        elif choice == 9:
            car_service(name)
        elif choice == 10:
            car_wash(name)
        elif choice == 11:
            painting(name)
        elif choice == 12:
            carpentry(name)
        elif choice == 13:
            pest_control(name)
        elif choice == 14:
            salon(name)
        elif choice == 15:
            beauty_service(name)
        elif choice == 16:
            appliance_repair(name)
        elif choice == 17:
            water_purifier_service(name)
        elif choice == 18:
            packers_and_movers(name)
        elif choice == 19:
            gardening(name)
        elif choice == 20:
            photography(name)
        elif choice == 21:
            view_my_bookings(name)
        elif choice == 22:
            print("Logging out...")
            login()
            break
        else:
            print("Invalid Choice")   

#==========================Helper Function For Booking Flow=========================
def handle_company_selection(customer_name, service_name, companies):
    """Helper function to show numbered companies and proceed with booking"""
    if not companies:
        print("No companies currently offering this service.")
        return

    print("\nSelect a Company by Serial Number to Book an Appointment:")
    for index, i in enumerate(companies, start=1):
        print("="*80)
        print(f"{index}. {i[0].upper()}")
        print(f"Contact No. : {i[1]} | Website : {i[2]} | Address : {i[3]} | Rating : ⭐ {i[4]}")
        print("="*80)
    
    print(f"{len(companies) + 1}. Go Back")

    try:
        comp_choice = int(input("\nEnter choice: "))
        if comp_choice == len(companies) + 1:
            return
        elif 1 <= comp_choice <= len(companies):
            selected_company = companies[comp_choice - 1][0]
            create_booking(customer_name, service_name, selected_company)
        else:
            print("Invalid Option.")
    except ValueError:
        print("Invalid input. Returning to menu.")

#==============================Each Service Function===============================
def plumbing(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from plumbing")
    z = cursor.fetchall()
    handle_company_selection(customer_name, "Plumbing", z)

def electrician(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from electrician")
    q= cursor.fetchall()
    handle_company_selection(customer_name, "Electrician", q)

def home_cleaning(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from home_cleaning")
    s= cursor.fetchall()
    handle_company_selection(customer_name, "Home Cleaning", s)

def ac_repair(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from ac_repair")
    w= cursor.fetchall()
    handle_company_selection(customer_name, "AC Repair", w)

def ac_installation(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from ac_installation")
    e= cursor.fetchall()
    handle_company_selection(customer_name, "AC Installation", e)

def laptop_repair(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from laptop_repair")
    y= cursor.fetchall()
    handle_company_selection(customer_name, "Laptop Repair", y)

def mobile_repair(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from mobile_repair")
    m = cursor.fetchall()
    handle_company_selection(customer_name, "Mobile Repair", m)

def computer_repair(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from computer_repair")
    c = cursor.fetchall()
    handle_company_selection(customer_name, "Computer Repair", c)

def car_service(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from car_service")
    cs = cursor.fetchall()
    handle_company_selection(customer_name, "Car Service", cs)

def car_wash(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from car_wash")
    cw = cursor.fetchall()
    handle_company_selection(customer_name, "Car Wash", cw)

def painting(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from painting")
    p = cursor.fetchall()
    handle_company_selection(customer_name, "Painting", p)

def carpentry(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from carpentry")
    cp = cursor.fetchall()
    handle_company_selection(customer_name, "Carpentry", cp)

def pest_control(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from pest_control")
    pc = cursor.fetchall()
    handle_company_selection(customer_name, "Pest Control", pc)

def salon(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from salon")
    sl = cursor.fetchall()
    handle_company_selection(customer_name, "Salon", sl)

def beauty_service(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from beauty_service")
    bs = cursor.fetchall()
    handle_company_selection(customer_name, "Beauty Service", bs)

def appliance_repair(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from appliance_repair")
    ar = cursor.fetchall()
    handle_company_selection(customer_name, "Appliance Repair", ar)

def water_purifier_service(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from water_purifier_service")
    wp = cursor.fetchall()
    handle_company_selection(customer_name, "Water Purifier Service", wp)

def packers_and_movers(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from packers_and_movers")
    pm = cursor.fetchall()
    handle_company_selection(customer_name, "Packers and Movers", pm)

def gardening(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from gardening")
    g = cursor.fetchall()
    handle_company_selection(customer_name, "Gardening", g)

def photography(customer_name):
    print("========Available Companies Offering This Service========")
    cursor.execute("select * from photography")
    ph = cursor.fetchall()
    handle_company_selection(customer_name, "Photography", ph)

#==============================Customer Booking History============================
def view_my_bookings(customer_name):
    print(f"\n=========== BOOKING HISTORY FOR {customer_name.upper()} ===========")
    cursor.execute(
        "SELECT service_name, company_name, booking_date, booking_time, booking_status FROM bookings WHERE customer_name = %s", 
        (customer_name,)
    )
    my_bookings = cursor.fetchall()
    
    if not my_bookings:
        print("No bookings found.")
        return

    for b in my_bookings:
        print(f"Service: {b[0]} | Company: {b[1]} | Date: {b[2]} | Time: {b[3]} | Status: {b[4].upper()}")
    print("="*60)

#==============================Admin Menu====================================
def admin_menu():
    while True:
        print("\n=========== ADMIN MENU ===========")
        print("1. Add Company")
        print("2. View Users")
        print("3. View Bookings")
        print("4. Delete Company")
        print("5. Update Booking Status")
        print("6. Logout")
        
        try:
            choice = int(input("Enter Choice : "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            add_company()
        elif choice == 2:
            view_users()
        elif choice == 3:
            view_bookings()
        elif choice == 4:
            delete_company()
        elif choice == 5:
            update_booking_status()
        elif choice == 6:
            print("Logging out...")
            login()
            break
        else:
            print("Invalid Choice")

def add_company():
    service = input("Enter Service Table Name : ").lower()
    company_name = input("Enter Company Name : ")
    contact_no = input("Enter Contact Number : ")
    website = input("Enter Website : ")
    address = input("Enter Address : ")
    try:
        rating = float(input("Enter Rating : "))
    except ValueError:
        rating = 0.0

    query =( f"INSERT INTO {service} VALUES (%s,%s,%s,%s,%s)")
    cursor.execute(query, (company_name, contact_no, website, address, rating))
    mydb.commit()
    print("Company Added Successfully!")

def view_users():
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    print("\n=========== REGISTERED USERS ===========")
    for i in users:
        print(f"Name : {i[0]} | Role : {i[2]}")

def view_bookings():
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    print("\n=========== BOOKINGS ===========")
    for i in bookings:
        print(i)

def delete_company():
    service = input("Enter Service Table Name : ").lower()
    company = input("Enter Company Name to Delete : ")
    query = f"DELETE FROM {service} WHERE company_name=%s"
    cursor.execute(query, (company,))
    mydb.commit()
    print("Company Deleted Successfully!")

def create_booking(customer_name, service_name, company_name):
    booking_date = input("Enter Booking Date (YYYY-MM-DD): ")
    booking_time = input("Enter Booking Time (HH:MM:SS): ")

    cursor.execute(
        """
        INSERT INTO bookings
        (customer_name,service_name,company_name,
        booking_date,booking_time,booking_status)
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (customer_name, service_name, company_name, booking_date, booking_time, "pending")
    )
    mydb.commit()
    print("Booking Created Successfully.")

def update_booking_status():
    try:
        booking_id = int(input("Enter Booking ID : "))
        print("1.Pending")
        print("2.Confirmed")
        print("3.Completed")
        print("4.Cancelled")
        choice = int(input("Enter Status Choice : "))

        status_dict = {1:"pending", 2:"confirmed", 3:"completed", 4:"cancelled"}
        if choice in status_dict:
            status = status_dict[choice]
            cursor.execute("UPDATE bookings SET booking_status=%s WHERE booking_id=%s", (status, booking_id))
            mydb.commit()
            print("Booking Status Updated.")
        else:
            print("Invalid choice. Status not altered.")
    except ValueError:
        print("Invalid numerical input.")

#============================================================================
login()
