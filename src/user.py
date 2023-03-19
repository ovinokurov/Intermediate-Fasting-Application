from user_model import UserModel

class User:
    def __init__(self, name, fasting_hours=16):
        self.name = name
        self.model = UserModel(fasting_hours)

    def add_meal(self, meal_time, weight=None):
        self.model.add_meal(meal_time, weight)

    def update_meal(self, meal_index, new_time):
        self.model.update_meal(meal_index, new_time)

    def update_weight(self, current_weight):
        self.model.update_weight(current_weight)

    def change_fasting_hours(self, new_hours):
        self.model.change_fasting_hours(new_hours)

    def get_next_meal(self):
        return self.model.get_next_meal()

    def get_time_left_before_next_meal(self):
        return self.model.get_time_left_before_next_meal()

    def to_dict(self):
        return {
            "name": self.name,
            "fasting_hours": self.model.fasting_hours,
            "meals": self.model.meals,
            "weight_data": self.model.weight_data,
        }

    def generate_report(self):
        report = "\nFasting Report:\n"
        report += "------------------------------------------------------------------\n"
        report += "Date       | Meal Time           | Fasting Hours | Weight | Goal\n"
        report += "------------------------------------------------------------------\n"
        all_meal_dates = sorted([meal["time"] for meal in self.model.meals])
        all_weight_dates = {entry["date"]: (entry["weight"], entry["goal"]) for entry in self.model.weight_data}

        for meal_date in all_meal_dates:
            weight, goal = all_weight_dates.get(meal_date.split(" ")[0], ("N/A", "N/A"))
            report += f"{meal_date.split(' ')[0]} | {meal_date} | {self.model.fasting_hours}            | {weight}  | {goal}\n"

        report += "------------------------------------------------------------------\n"

        return report

    @classmethod
    def from_dict(cls, data):
        user = cls(data["name"], data["fasting_hours"])
        user.model.meals = data["meals"]
        user.model.weight_data = data["weight_data"]
        return user
