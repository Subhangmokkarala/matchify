from flask import Flask, redirect, url_for, session, render_template, request, flash
import spotidatacollect  # Custom module for Spotify API data collection
import matchmake        # Custom module for matching and stats
import mysql.connector   # For MySQL interaction
import logging
import os
from dotenv import load_dotenv

#use pyfiglet and win10toast to make the app more fun
from pyfiglet import Figlet
from win10toast import ToastNotifier

# Create a custom figlet font
f = Figlet(font='slant')
print(f.renderText('Matchify'))

# Create a ToastNotifier object
toaster = ToastNotifier()
toaster.show_toast("Matchify", "Your perfect match is just a Beat away!", duration=10)


# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Set a default for development

# Configure logging
logging.basicConfig(level=logging.INFO)

# MySQL connection setup
try:
    db = mysql.connector.connect(
        host=os.getenv('HOST_SECRET'),
        user=os.getenv('USER_SECRET'),
        password=os.getenv('PASSWORD_SECRET'),
        database=os.getenv('DATABASE_SECRET')
    )
except mysql.connector.Error as err:
    logging.error(f"Error connecting to the database: {err}")
    raise

# Validate required environment variables
REQUIRED_ENV_VARS = ['CLIENT_ID', 'CLIENT_SECRET', 'REDIRECT_URI', 'FLASK_SECRET_KEY', 'HOST_SECRET', 'USER_SECRET', 'PASSWORD_SECRET', 'DATABASE_SECRET']
for var in REQUIRED_ENV_VARS:
    if not os.getenv(var):
        logging.error(f"Environment variable {var} is missing.")
        raise EnvironmentError(f"{var} is not set")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        gender = request.form['gender']  # 'male' or 'female'
        
        # Save user credentials to the database
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (username, password, gender) VALUES (%s, %s, %s)",
                           (username, password, gender))
            db.commit()
            session['username'] = username
            session['gender'] = gender
            logging.info(f"User registered: {username}, Gender: {gender}")
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            logging.error(f"Error saving user data: {err}")
            flash("Registration failed. Please try again.")
            return render_template('register.html')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials in the database
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = user[1]  # Assuming username is in the second column
            session['gender'] = user[3]     # Assuming gender is in the fourth column
            logging.info(f"User logged in: {username}")
            return redirect(url_for('login_with_spotify'))  # Redirect to Spotify login
        else:
            flash("Invalid username or password.")
            return render_template('login.html')

    return render_template('login.html')

@app.route('/login_with_spotify')
def login_with_spotify():
    # Redirect to Spotify login
    sp_oauth, auth_url = spotidatacollect.spotify_login()
    return redirect(auth_url)  # Ensure to redirect to the authorization URL

@app.route('/callback')
def callback():
    # Handle Spotify OAuth callback
    code = request.args.get('code')  # Get authorization code
    if not code:
        logging.error("No code provided in the callback")
        return redirect(url_for('login'))  # Redirect back to login if no code

    # Get Spotify user data
    try:
        spotify_user_data = spotidatacollect.get_spotify_data(code)
    except ValueError as e:
        logging.error(f"Error getting Spotify data: {e}")
        return redirect(url_for('login'))

    session['spotify_data'] = spotify_user_data
    session['spotify_user_id'] = spotify_user_data['id']

    # Save user data to MySQL
    save_user_to_db(spotify_user_data)
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    if 'spotify_data' not in session:
        return redirect(url_for('login'))

    user_data = session['spotify_data']
    username = session.get('username', 'Guest')
    gender = session.get('gender', 'Unknown')

    return render_template('profile.html', user_data=user_data, username=username, gender=gender)

@app.route('/match')
def match():
    if 'spotify_data' not in session:
        return redirect(url_for('login'))

    username = session.get('username')
    gender = session.get('gender')

    match_gender = 'female' if gender == 'male' else 'male'

    match_data = matchmake.match_user(gender, db)
    return render_template('match.html', match_data=match_data)

def save_user_to_db(user_data):
    try:
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO users (spotify_id, username, gender, top_artists, top_tracks)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            top_artists = %s, top_tracks = %s
        """, (user_data['id'], session['username'], session['gender'], 
              str(user_data['top_artists']), str(user_data['top_tracks']),
              str(user_data['top_artists']), str(user_data['top_tracks'])))
        db.commit()
        logging.info(f"User {session['username']} saved to database.")
    except mysql.connector.Error as err:
        logging.error(f"Error saving user data: {err}")
        db.rollback()

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', True))  # Set to True for development, False for production
