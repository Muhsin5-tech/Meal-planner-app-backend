from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, User, Meal, DayPlan, DayPlanMeal
from config import Config
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)

# Allow CORS for all domains, adjust as needed for production security
CORS(app, origins=[os.getenv("FRONTEND_URL")])

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "<h1>Welcome to my Meal Planner App Backend</h1>"

@app.route('/meals', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    return jsonify([meal.to_dict() for meal in meals])

@app.route('/meals/<int:id>', methods=['GET'])
def get_meal(id):
    meal = Meal.query.get_or_404(id)
    return jsonify(meal.to_dict())

@app.route('/meals', methods=['POST'])
def create_meal():
    data = request.get_json()
    if not data.get('name') or not isinstance(data['name'], str):
        return jsonify({"error": "Valid Name is required."}), 400
    if not data.get('ingredients') or not isinstance(data['ingredients'], str):
        return jsonify({"error": "Ingredients are required."}), 400
    if not data.get('instructions') or not isinstance(data['instructions'], str):
        return jsonify({"error": "Instructions are required."}), 400
    if not data.get('image_url') or not isinstance(data['image_url'], str):
        return jsonify({"error": "Valid Image URL is required."}), 400

    new_meal = Meal(
        name=data['name'],
        ingredients=data['ingredients'],
        instructions=data['instructions'],
        image_url=data['image_url']
    )
    db.session.add(new_meal)
    db.session.commit()

    return jsonify({
        "message": "Meal added successfully",
        'meal': new_meal.to_dict()
    }), 201

@app.route('/meals/<int:id>', methods=['PUT'])
def update_meal(id):
    meal = Meal.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data:
        if not isinstance(data['name'], str):
            return jsonify({"error": "Valid Name is required."}), 400
        meal.name = data['name']

    if 'ingredients' in data:
        if not isinstance(data['ingredients'], str):
            return jsonify({"error": "Valid Ingredients are required."}), 400
        meal.ingredients = data['ingredients']

    if 'instructions' in data:
        if not isinstance(data['instructions'], str):
            return jsonify({"error": "Valid Instructions are required."}), 400
        meal.instructions = data['instructions']

    if 'image_url' in data:
        if not isinstance(data['image_url'], str):
            return jsonify({"error": "Valid Image URL is required."}), 400
        meal.image_url = data['image_url']

    db.session.commit()

    return jsonify({
        "message": "Meal updated successfully",
        'meal': meal.to_dict()
    })

@app.route('/meals/<int:id>', methods=['DELETE'])
def delete_meal(id):
    meal = Meal.query.get_or_404(id)
    db.session.delete(meal)
    db.session.commit()
    return jsonify({"message": "Meal deleted successfully!"}), 204

@app.route('/dayplans', methods=['GET'])
def get_dayplans():
    dayplans = DayPlan.query.all()
    return jsonify([dayplan.to_dict() for dayplan in dayplans])

@app.route('/dayplans/<int:id>', methods=['GET'])
def get_dayplan(id):
    dayplan = DayPlan.query.get_or_404(id)
    return jsonify(dayplan.to_dict())

@app.route('/dayplans', methods=['POST'])
def create_dayplan():
    data = request.get_json()
    if not data.get('day_of_week') or not data.get('user_id'):
        return jsonify({"error": "Day of week and User ID are required."}), 400

    new_dayplan = DayPlan(day_of_week=data['day_of_week'], user_id=data['user_id'])
    db.session.add(new_dayplan)
    db.session.commit()

    return jsonify({
        "message": "Day plan added successfully!",
        'dayplan': new_dayplan.to_dict()
    }), 201

@app.route('/dayplans/<int:id>', methods=['PUT'])
def update_dayplan(id):
    dayplan = DayPlan.query.get_or_404(id)
    data = request.get_json()
    dayplan.day_of_week = data['day_of_week']
    dayplan.user_id = data['user_id']
    db.session.commit()

    return jsonify({
        "message": "Day plan updated successfully!",
        'dayplan': dayplan.to_dict()
    })

@app.route('/dayplans/<int:id>', methods=['DELETE'])
def delete_dayplan(id):
    dayplan = DayPlan.query.get_or_404(id)
    db.session.delete(dayplan)
    db.session.commit()
    return jsonify({"message": "Day plan deleted successfully!"}), 204

@app.route('/dayplans/<int:id>/assign_meals', methods=['POST'])
def assign_meals_to_dayplan(id):
    dayplan = DayPlan.query.get_or_404(id)
    data = request.get_json()

    meal_ids = data.get('meal_ids')
    meal_times = data.get('meal_times')

    if not meal_ids or len(meal_ids) != len(meal_times):
        return jsonify({"error": "Meal IDs and meal times must match."}), 400

    for meal_time in meal_times:
        try:
            datetime.strptime(meal_time, '%H:%M')
        except ValueError:
            return jsonify({"error": f"Invalid time format for meal: {meal_time}. Use HH:MM format."}), 400

    for meal_id, meal_time in zip(meal_ids, meal_times):
        meal = Meal.query.get_or_404(meal_id)
        dayplan_meal = DayPlanMeal(day_plan_id=dayplan.id, meal_id=meal.id, meal_time=meal_time)
        db.session.add(dayplan_meal)

    db.session.commit()
    return jsonify({"message": "Meals assigned to day plan successfully!"}), 201

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == '__main__':
    app.run()
