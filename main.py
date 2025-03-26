from app.core.database import get_db
from sqlalchemy import text
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
import datetime
import os
from dotenv import load_dotenv
from flask_frozen import Freezer
import sys

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')  # Use environment variable for secret key

# Initialize Flask-Frozen
freezer = Freezer(app)

# Sample data for demonstration
SAMPLE_TRIPS = [
    {
        'id': 1,
        'driver_name': 'John Doe',
        'from_location': 'Jounieh',
        'to_location': 'LAU Byblos',
        'departure_time': '8:00 AM',
        'price_per_seat': 50000,
        'available_seats': 3,
        'days': ['Mon', 'Wed', 'Fri']
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

@app.route('/create-account')
def create_account():
    return render_template('create_account.html')

@app.route('/driver/register', methods=['GET', 'POST'])
def driver_register():
    if request.method == 'POST':
        # Here you would typically:
        # 1. Validate the form data
        # 2. Create a new user in the database
        # 3. Handle file uploads if any
        # 4. Set up user session
        # For now, we'll just redirect to the home page
        flash('You are now signed in as a driver! Welcome to WheelShare.', 'success')
        return redirect(url_for('home'))
    return render_template('driver_register.html')

@app.route('/passenger/register', methods=['GET', 'POST'])
def passenger_register():
    if request.method == 'POST':
        # Here you would typically:
        # 1. Validate the form data
        # 2. Create a new user in the database
        # 3. Handle file uploads if any
        # 4. Set up user session
        # For now, we'll just redirect to the home page
        flash('You are now signed in as a passenger! Welcome to WheelShare.', 'success')
        return redirect(url_for('home'))
    return render_template('passenger_register.html')

@app.route('/trips', methods=['GET', 'POST'])
def trips():
    if request.method == 'POST':
        # Handle search/filter form submission
        return render_template('trips.html', trips=SAMPLE_TRIPS)
    return render_template('trips.html', trips=SAMPLE_TRIPS)

@app.route('/trips/new', methods=['GET', 'POST'])
def new_trip():
    if request.method == 'POST':
        # Here you would typically:
        # 1. Validate the form data
        # 2. Create a new trip in the database
        # 3. Handle any file uploads
        # For now, we'll just redirect to the trips page
        flash('Trip created successfully!', 'success')
        return redirect(url_for('trips'))
    return render_template('create_trip.html')

@app.route('/trips/mine', methods=['GET', 'POST'])
def my_rides():
    if request.method == 'POST':
        # Handle ride cancellation
        trip_id = request.form.get('trip_id')
        trip = next((t for t in SAMPLE_TRIPS if t['id'] == int(trip_id)), None)
        if trip:
            trip['status'] = 'cancelled'
            flash('Ride cancelled successfully.', 'success')
        return redirect(url_for('my_rides'))
    return render_template('my_rides.html', trips=SAMPLE_TRIPS)

@app.route('/trip/<int:trip_id>', methods=['GET', 'POST'])
def trip_details(trip_id):
    trip = next((t for t in SAMPLE_TRIPS if t['id'] == trip_id), None)
    if not trip:
        return 'Trip not found', 404
        
    if request.method == 'POST':
        # Handle booking submission
        seats = int(request.form.get('seats', 1))
        days = request.form.getlist('days')
        
        # Create a new booking
        booking = {
            'id': len(SAMPLE_BOOKINGS) + 1,
            'trip_id': trip_id,
            'driver_name': trip['driver_name'],
            'from_location': trip['from_location'],
            'to_location': trip['to_location'],
            'date': trip['date'],
            'departure_time': trip['departure_time'],
            'price': trip['price_per_seat'] * seats + 1000,  # Add service fee
            'status': 'confirmed'
        }
        
        # Add booking to the list
        SAMPLE_BOOKINGS.append(booking)
        
        # Update trip availability
        trip['available_seats'] -= seats
        
        flash('Booking successful! Your trip has been booked.', 'success')
        return redirect(url_for('home'))
        
    return render_template('trip_details.html', trip=trip)

@app.route('/bookings')
def my_bookings():
    # Here you would typically:
    # 1. Get bookings from the database
    # 2. Filter by user
    # 3. Sort by date
    bookings = [
        {
            'id': 1,
            'from_location': 'Beirut',
            'to_location': 'AUB',
            'departure_time': '8:00 AM',
            'price': 25000,
            'status': 'confirmed'
        }
    ]
    return render_template('my_bookings.html', bookings=bookings)

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
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        # Build static site
        print("Building static site...")
        freezer.freeze()
        print("Static site built successfully!")
    else:
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('FLASK_ENV') == 'development'
        print("🚀 Starting the application...")
        print(f"Visit http://localhost:{port} to see the web interface")
        app.run(host='0.0.0.0', port=port, debug=debug) 