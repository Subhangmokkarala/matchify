from flask import Flask, redirect, url_for, session, render_template, request
import spotidatacollect  # Custom module for Spotify API data collection
import spotistats        # Custom module for matching and stats
import mysql.connector   # For MySQL interaction
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure logging
logging.basicConfig(level=logging.INFO)

# MySQL connection
db = mysql.connector.connect(
    host="192.168.29.82",
    user="root",
    password="mokkarala2004",
    database="spotify_matchmaker"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        gender = request.form['gender']  # 'male' or 'female'
        session['username'] = username
        session['gender'] = gender
        logging.info(f"User registered: {username}, Gender: {gender}")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login')
def login():
    # Redirect to Spotify login
    return spotidatacollect.spotify_login()

@app.route('/callback')
def callback():
    # Handle Spotify OAuth callback
    spotify_user_data = spotidatacollect.get_spotify_data(request.args)
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
    username = session.get('username')
    gender = session.get('gender')
    return render_template('profile.html', user_data=user_data, username=username, gender=gender)

@app.route('/match')
def match():
    if 'spotify_data' not in session:
        return redirect(url_for('login'))

    username = session.get('username')
    gender = session.get('gender')

    if gender == 'male':
        match_gender = 'female'
    else:
        match_gender = 'male'

    match_data = spotistats.match_user(gender, db)
    return render_template('match.html', match_data=match_data)

def save_user_to_db(user_data):
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

if __name__ == '__main__':
    app.run(debug=True)
