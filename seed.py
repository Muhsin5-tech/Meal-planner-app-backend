from app import app, db
from models import User, Meal, DayPlan, DayPlanMeal
from datetime import date

with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(username="Muhsin")
    user2 = User(username="Ali")
    db.session.add_all([user1, user2])
    db.session.commit()

    meal1 = Meal(name="Pasta", ingredients="Noodles, Tomato Sauce", instructions="Boil noodles, add sauce.", image_url="https://example.com/pasta.jpg")
    meal2 = Meal(name="Salad", ingredients="Lettuce, Tomato, Cucumber", instructions="Mix ingredients.", image_url="https://example.com/salad.jpg")
    meal3 = Meal(name="Pizza", ingredients="Dough, Tomato, Cheese", instructions="Bake at 350°F for 15 minutes.", image_url="https://example.com/pizza.jpg")
    db.session.add_all([meal1, meal2, meal3])
    db.session.commit()

    dayplan1 = DayPlan(day_of_week="Monday", date=date.today(), user_id=user1.id)
    dayplan2 = DayPlan(day_of_week="Tuesday", date=date.today(), user_id=user2.id)
    db.session.add_all([dayplan1, dayplan2])
    db.session.commit()

    dayplan_meal1 = DayPlanMeal(day_plan_id=dayplan1.id, meal_id=meal1.id, meal_time="12:00")
    dayplan_meal2 = DayPlanMeal(day_plan_id=dayplan2.id, meal_id=meal2.id, meal_time="18:00")
    db.session.add_all([dayplan_meal1, dayplan_meal2])
    db.session.commit()

    print("Sample users, meals, day plans, and assigned meals added successfully!")
