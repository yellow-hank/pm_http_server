from flask import Flask
from campus_display.route import campus_display

def create_app():
    # Create Flask app
    app = Flask(__name__)
    # Configuration for flask_pymongo
    app.config['MONGO_DBNAME'] = 'pmBase'
    app.config['MONGO_URI'] = 'mongodb://mongo:27017/pmBase'
    # Bind the blueprint
    app.register_blueprint(campus_display)
    return app
