import datetime
from dateutil.parser import parse as parse_date

class UserModel:
    def __init__(self, fasting_hours, meals=None, weight_data=None):
        self.fasting_hours = fasting_hours
        self.meals = meals if meals else []
        self.weight_data = weight_data if weight_data else []

    def add_meal(self, meal_time, weight=None):
        meal = {"time": meal_time}
        self.meals.append(meal)

        if weight is not None:
            goal_weight = weight * 0.9
            self.weight_data.append({"date": meal_time.split(" ")[0], "weight": weight, "goal": goal_weight})

    def update_meal(self, meal_index, new_time):
        if 0 <= meal_index < len(self.meals):
            self.meals[meal_index]["time"] = new_time
        else:
            raise ValueError("Invalid meal index")

    def update_weight(self, current_weight):
        goal_weight = current_weight * 0.9
        self.weight_data.append({"date": datetime.datetime.now().strftime("%m/%d/%Y"), "weight": current_weight, "goal": goal_weight})

    def change_fasting_hours(self, new_hours):
        self.fasting_hours = new_hours

    def get_next_meal(self):
        now = datetime.datetime.now()
        last_meal = max(self.meals, key=lambda x: parse_date(x['time'])) if self.meals else None
        if last_meal:
            last_meal_time = parse_date(last_meal['time'])
            next_meal_time = last_meal_time + datetime.timedelta(hours=self.fasting_hours)
            return next_meal_time
        return None

    def get_time_left_before_next_meal(self):
        next_meal = self.get_next_meal()
        if next_meal:
            now = datetime.datetime.now()
            time_left = next_meal - now
            return time_left
        return None
