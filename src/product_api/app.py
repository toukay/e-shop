from flask import Flask
from routes import api_bp
from flask_cors import CORS

import database

app = Flask(__name__)
CORS(app)
app.register_blueprint(api_bp)

with app.app_context():
    database.create_all()

if __name__ == "__main__":
    app.run(debug=True)
