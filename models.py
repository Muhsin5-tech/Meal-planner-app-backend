from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)
    instructions = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'image_url': self.image_url
        }

class DayPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('dayplans', lazy=True))
    meals = db.relationship('DayPlanMeal', back_populates='dayplan')

    def to_dict(self):
        return {
            'id': self.id,
            'day_of_week': self.day_of_week,
            'date': self.date,
            'user_id': self.user_id
        }

class DayPlanMeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_plan_id = db.Column(db.Integer, db.ForeignKey('day_plan.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
    meal_time = db.Column(db.String(50), nullable=False)

    dayplan = db.relationship('DayPlan', back_populates='meals')
    meal = db.relationship('Meal')

    def to_dict(self):
        return {
            'id': self.id,
            'day_plan_id': self.day_plan_id,
            'meal_id': self.meal_id,
            'meal_time': self.meal_time
        }