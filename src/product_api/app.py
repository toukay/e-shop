from flask import Flask
from routes import api_bp

import database

app = Flask(__name__)
app.register_blueprint(api_bp)

with app.app_context():
    database.create_all()

if __name__ == "__main__":
    app.run(debug=True)
