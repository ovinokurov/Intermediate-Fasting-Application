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
        report = f"Name: {self.name}\n"
        report += f"Fasting hours: {self.model.fasting_hours}\n"
        report += "Meal history:\n"
        for meal in self.model.meals:
            report += f"{meal['time']}\n"
        report += "Weight history:\n"
        for weight_entry in self.model.weight_data:
            report += f"{weight_entry['date']}: {weight_entry['weight']} lbs\n"
        return report

    @classmethod
    def from_dict(cls, data):
        user = cls(data["name"], data["fasting_hours"])
        user.model.meals = data["meals"]
        user.model.weight_data = data["weight_data"]
        return user
