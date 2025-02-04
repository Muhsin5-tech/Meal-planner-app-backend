from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, User, Meal, DayPlan, DayPlanMeal
from config import Config
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS with explicit origin
CORS(app, origins=[os.getenv("FRONTEND_URL")])

# Initialize database
db.init_app(app)
migrate = Migrate(app, db)

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return "<h1>Welcome to my Meal Planner App Backend</h1>"

@app.route('/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    return jsonify([meal.to_dict() for meal in meals])

# Add other routes as needed...

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == '__main__':
    app.run(debug=True)