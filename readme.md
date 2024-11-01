# Matchify: A Spotify Matchmaker

Welcome to **Matchify**, your ultimate Spotify matchmaker! Matchify helps you find and connect with people who share your music tastes.

## Features

- **Music Taste Matching**: Discover users with similar music preferences.
- **Playlist Sharing**: Share your favorite playlists with your matches.
- **Music Recommendations**: Get personalized music recommendations based on your matches' playlists.

## Getting Started

1. **Sign Up**: Create an account on Matchify.
2. **Connect Spotify**: Link your Spotify account to Matchify.
3. **Find Matches**: Start finding users with similar music tastes.
4. **Enjoy Music**: Share playlists and enjoy new music recommendations.

## Installation

To install Matchify, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/matchify.git
    ```
2. Navigate to the project directory:
    ```bash
    cd matchify
    ```
3. Install dependencies:
    ```bash
    npm install
    ```
4. Start the application:
    ```bash
    npm start
    ```

## Contributing

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact us at support@matchify.com.

Happy matching with Matchify!

## Built With

- **Flask**: A lightweight WSGI web application framework in Python.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.x.
- You have a basic understanding of Python and Flask.
- You have a Spotify account.

## Running Locally

To run Matchify locally with Flask, follow these steps:

1. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
2. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Set the Flask application environment variable:
    ```bash
    export FLASK_APP=app.py
    ```
5. Run the Flask application:
    ```bash
    flask run
    ```


## things to be fixed
- [ ] Add a `Dockerfile` for containerization. - we dont need na ? 
- [ ] fix authentication with required password type
- [ ] making queries and authentication server secure
- [ ] data privacy and security 
- [ ] dynamic dashboard
- [ ] fixing ui 
- [ ] data collection
- [ ] new matching algorithm
- [ ] stats and compatibity and stars and zodiac signs
- [ ] personality types and music taste
- [ ] graphs and charts and extreme patterns recognition
- [ ] music taste and mood and time of the day
- [ ] many more features