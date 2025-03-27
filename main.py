from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from flask_session import Session
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['TEMPLATES_AUTO_RELOAD'] = False  # Disable auto-reload for better performance
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem for session storage
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Set session lifetime

# Initialize Flask-Session
Session(app)

# Sample data for demonstration
SAMPLE_TRIPS = [
    {
        'id': 1,
        'driver_name': 'John Doe',
        'from_location': 'Beirut',
        'to_location': 'Tripoli',
        'date': '2024-03-26',
        'departure_time': '08:00 AM',
        'price_per_seat': 5000,
        'available_seats': 3,
        'status': 'active'
    },
    {
        'id': 2,
        'driver_name': 'Jane Smith',
        'from_location': 'Tripoli',
        'to_location': 'AUB',
        'departure_time': '7:30 AM',
        'price_per_seat': 75000,
        'available_seats': 2,
        'days': ['Tue', 'Thu']
    }
]

SAMPLE_USER = {
    'name': 'John Doe',
    'email': 'john.doe@example.com',
    'phone': '+961 70 123 456',
    'university': 'LAU',
    'bio': 'Regular commuter between Jounieh and LAU Byblos. Love meeting new people!',
    'car_model': 'Honda Civic',
    'car_year': 2020,
    'car_color': 'Silver',
    'license_plate': 'ABC 123',
    'joined_date': 'March 2024',
    'trips_completed': 45,
    'rating': 4.8,
    'reviews': 32
}

SAMPLE_CONVERSATIONS = [
    {
        'id': 1,
        'name': 'Sarah Wilson',
        'last_message': 'See you tomorrow at 8!',
        'last_time': '2:30 PM',
        'unread': True,
        'active': True,
        'status': 'Online'
    },
    {
        'id': 2,
        'name': 'Mike Johnson',
        'last_message': 'Thanks for the ride!',
        'last_time': 'Yesterday',
        'unread': False,
        'active': False,
        'status': 'Last seen 2h ago'
    }
]

SAMPLE_MESSAGES = [
    {
        'content': 'Hi, is the ride still available for tomorrow?',
        'time': '2:15 PM',
        'sent_by_me': False
    },
    {
        'content': 'Yes, it is! I have 2 seats available.',
        'time': '2:20 PM',
        'sent_by_me': True
    },
    {
        'content': 'Great! Can I book one seat?',
        'time': '2:25 PM',
        'sent_by_me': False
    },
    {
        'content': 'See you tomorrow at 8!',
        'time': '2:30 PM',
        'sent_by_me': True
    }
]

SAMPLE_BOOKINGS = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/choose-role')
def choose_role():
    return render_template('choose_role.html')

@app.route('/register/<role>', methods=['GET', 'POST'])
def register(role):
    if role not in ['driver', 'passenger']:
        return redirect(url_for('choose_role'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        # In a real app, you would validate and store in a database
        # For now, we'll just store in session
        session['user_id'] = 1  # Using a fixed ID for demo
        session['user_role'] = role
        session['user_name'] = name
        session['user_email'] = email
        
        flash(f'Welcome to WheelShare! You are now registered as a {role}.', 'success')
        return redirect(url_for('home'))
        
    return render_template('register.html', role=role)

@app.route('/login/<role>', methods=['GET', 'POST'])
def login(role):
    if role not in ['driver', 'passenger']:
        return redirect(url_for('choose_role'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # In a real app, you would validate against a database
        # For now, we'll just set the session
        session['user_id'] = 1
        session['user_role'] = role
        session['user_name'] = 'John Doe'
        session['user_email'] = email
        
        flash(f'Welcome back! You are now logged in as a {role}.', 'success')
        return redirect(url_for('home'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/trips', methods=['GET', 'POST'])
def trips():
    if not session.get('user_id'):
        flash('Please log in to view available trips.', 'error')
        return redirect(url_for('login', role='passenger'))
        
    if session.get('user_role') != 'passenger':
        flash('Only passengers can view available trips.', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Handle search/filter form submission
        university = request.form.get('university')
        departure = request.form.get('departure')
        day = request.form.get('day')
        
        # Filter trips based on criteria
        filtered_trips = SAMPLE_TRIPS
        if university:
            filtered_trips = [trip for trip in filtered_trips if trip['to_location'] == university]
        if departure:
            filtered_trips = [trip for trip in filtered_trips if trip['from_location'] == departure]
        if day:
            filtered_trips = [trip for trip in filtered_trips if day in trip.get('days', [])]
            
        return render_template('trips.html', trips=filtered_trips)
        
    return render_template('trips.html', trips=SAMPLE_TRIPS)

@app.route('/trips/new', methods=['GET', 'POST'])
def new_trip():
    if not session.get('user_id'):
        flash('Please log in to create a trip.', 'error')
        return redirect(url_for('login', role='driver'))
        
    if session.get('user_role') != 'driver':
        flash('Only drivers can create trips.', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Get form data
        from_location = request.form.get('from_location')
        to_location = request.form.get('to_location')
        departure_date = request.form.get('departure_date')
        departure_time = request.form.get('departure_time')
        available_seats = int(request.form.get('available_seats'))
        price_per_seat = int(request.form.get('price_per_seat'))
        notes = request.form.get('notes')
        
        # Create new trip
        new_trip = {
            'id': len(SAMPLE_TRIPS) + 1,
            'driver_name': session.get('user_name', 'Unknown Driver'),
            'from_location': from_location,
            'to_location': to_location,
            'date': departure_date,
            'departure_time': departure_time,
            'price_per_seat': price_per_seat,
            'available_seats': available_seats,
            'status': 'active',
            'notes': notes,
            'driver_id': session.get('user_id')
        }
        
        # Add to sample trips
        SAMPLE_TRIPS.append(new_trip)
        
        flash('Trip created successfully!', 'success')
        return redirect(url_for('my_rides'))
        
    return render_template('create_trip.html')

@app.route('/my-rides')
def my_rides():
    if not session.get('user_id'):
        flash('Please log in to view your rides.', 'error')
        return redirect(url_for('login', role='driver'))
        
    if session.get('user_role') != 'driver':
        flash('Only drivers can access this page.', 'error')
        return redirect(url_for('home'))
    
    # Get all trips created by the current driver
    driver_trips = [trip for trip in SAMPLE_TRIPS if trip.get('driver_id') == session.get('user_id')]
    return render_template('my_rides.html', trips=driver_trips)

@app.route('/trip/<int:trip_id>', methods=['GET', 'POST'])
def trip_details(trip_id):
    trip = next((t for t in SAMPLE_TRIPS if t['id'] == trip_id), None)
    if not trip:
        flash('Trip not found.', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        if not session.get('user_id'):
            flash('Please log in to book a trip.', 'error')
            return redirect(url_for('login'))

        seats = int(request.form.get('seats', 1))
        if seats > trip['available_seats']:
            flash('Not enough seats available.', 'error')
            return redirect(url_for('trip_details', trip_id=trip_id))

        # Create a booking
        booking = {
            'id': len(SAMPLE_BOOKINGS) + 1,
            'trip_id': trip_id,
            'user_id': session.get('user_id'),
            'seats': seats,
            'status': 'confirmed',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        SAMPLE_BOOKINGS.append(booking)

        # Update trip seats
        trip['available_seats'] -= seats

        flash('Booking successful! Your trip has been booked.', 'success')
        return redirect(url_for('my_bookings'))

    return render_template('trip_details.html', trip=trip)

@app.route('/bookings')
def my_bookings():
    if not session.get('user_id'):
        flash('Please log in to view your bookings.', 'error')
        return redirect(url_for('login'))

    # Get all bookings for the current user
    user_bookings = [b for b in SAMPLE_BOOKINGS if b['user_id'] == session.get('user_id')]
    
    # Get trip details for each booking
    bookings_with_trips = []
    for booking in user_bookings:
        trip = next((t for t in SAMPLE_TRIPS if t['id'] == booking['trip_id']), None)
        if trip:
            booking_info = {
                'id': booking['id'],
                'trip_id': trip['id'],
                'driver_name': trip['driver_name'],
                'from_location': trip['from_location'],
                'to_location': trip['to_location'],
                'date': trip['date'],
                'departure_time': trip['departure_time'],
                'seats': booking['seats'],
                'price': trip['price_per_seat'] * booking['seats'],
                'status': booking['status'],
                'created_at': booking['created_at']
            }
            bookings_with_trips.append(booking_info)

    return render_template('my_bookings.html', bookings=bookings_with_trips)

@app.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    # Here you would typically:
    # 1. Validate the booking exists and belongs to the user
    # 2. Update booking status in database
    # 3. Update trip availability
    flash('Booking cancelled successfully.', 'success')
    return redirect(url_for('my_bookings'))

@app.route('/chat', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        # Handle message sending
        message = request.form.get('message')
        flash('Message sent successfully.', 'success')
        return redirect(url_for('messages'))
    return render_template('messages.html', 
                         conversations=SAMPLE_CONVERSATIONS,
                         active_conversation=SAMPLE_CONVERSATIONS[0] if SAMPLE_CONVERSATIONS else None,
                         messages=SAMPLE_MESSAGES)

@app.route('/chat/<int:conversation_id>', methods=['GET', 'POST'])
def chat(conversation_id):
    conversation = next((conv for conv in SAMPLE_CONVERSATIONS if conv['id'] == conversation_id), None)
    if not conversation:
        return 'Conversation not found', 404
        
    if request.method == 'POST':
        # Handle message sending
        message = request.form.get('message')
        flash('Message sent successfully.', 'success')
        return redirect(url_for('chat', conversation_id=conversation_id))
        
    return render_template('messages.html',
                         conversations=SAMPLE_CONVERSATIONS,
                         active_conversation=conversation,
                         messages=SAMPLE_MESSAGES)

@app.route('/notifications')
def notifications():
    return render_template('notifications.html', notifications=[])

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Handle profile update
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))
    return render_template('profile.html', user=SAMPLE_USER)

@app.route('/payment-info', methods=['GET', 'POST'])
def payment_info():
    if request.method == 'POST':
        # Handle payment method addition/update
        flash('Payment information updated successfully.', 'success')
        return redirect(url_for('payment_info'))
    return render_template('payment_info.html')

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        # Handle profile edit
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))
    return render_template('edit_profile.html')

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        # Handle password change
        flash('Password changed successfully.', 'success')
        return redirect(url_for('profile'))
    return render_template('change_password.html')

@app.route('/api/system-info')
def system_info():
    return jsonify({
        "status": "running",
        "version": "1.0.0",
        "database": "SQLite",
        "uptime": "0 minutes"
    })

@app.route('/api/trips')
def api_trips():
    return jsonify(SAMPLE_TRIPS)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    print("🚀 Starting the application...")
    print(f"Visit http://localhost:{port} to see the web interface")
    app.run(host='0.0.0.0', port=port, debug=debug) 