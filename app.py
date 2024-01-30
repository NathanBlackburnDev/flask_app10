from flask import Flask
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aii09i09w3if09vwawdoidu230q'
# Set the session lifetime to 1 hour
app.permanent_session_lifetime = timedelta(minutes=60)

import routes

if __name__ == "__main__":
    app.run(debug=True)