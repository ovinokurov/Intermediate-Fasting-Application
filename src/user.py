import datetime

class User:
    def __init__(self, name, fasting_hours=16):
        self.name = name
        self.fasting_hours = fasting_hours
        self.meals = []
        self.weight_data = []

    @classmethod
    def from_dict(cls, user_data):
        user = cls(user_data["name"], user_data["fasting_hours"])
        user.meals = user_data["meals"]
        user.weight_data = user_data["weight_data"]
        return user

    def to_dict(self):
        return {
            "name": self.name,
            "fasting_hours": self.fasting_hours,
            "meals": self.meals,
            "weight_data": self.weight_data,
        }

    def add_meal(self):
        now = datetime.datetime.now()
        default_time = now.strftime("%m/%d/%Y %I:%M %p")
        print(f"Current date and time: {default_time}")
        
        current_time = datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')
        meal_time = input(f"Enter the date and time of your meal (mm/dd/yyyy hh:mm am/pm) [default: {current_time}]: ") or current_time
        
        if not meal_time:
            meal_time = default_time
        meal = {"time": meal_time}

        if self.weight_data:
            last_weight_entry = self.weight_data[-1]
            current_weight = last_weight_entry["weight"]
            goal_weight = last_weight_entry["goal"]
        else:
            current_weight = float(input("Please enter your current weight: "))
            goal_weight = current_weight * 0.9

        self.weight_data.append({"date": meal_time.split(" ")[0], "weight": current_weight, "goal": goal_weight})
        self.meals.append(meal)
        print(f"Meal added: {meal_time}")

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

    def generate_report(self):
        report = "\nFasting Report:\n"
        report += "------------------------------------------------------------------\n"
        report += "Date       | Meal Time           | Fasting Hours | Weight | Goal\n"
        report += "------------------------------------------------------------------\n"
        all_meal_dates = sorted([meal["time"] for meal in self.meals])
        all_weight_dates = {entry["date"]: (entry["weight"], entry["goal"]) for entry in self.weight_data}

        for meal_date in all_meal_dates:
            weight, goal = all_weight_dates.get(meal_date.split(" ")[0], ("N/A", "N/A"))
            report += f"{meal_date.split(' ')[0]} | {meal_date} | {self.fasting_hours}            | {weight}  | {goal}\n"

        report += "------------------------------------------------------------------\n"

        return report

    def get_next_meal(self):
            if not self.meals:
                return None

            last_meal_time = datetime.datetime.strptime(self.meals[-1]["time"], "%m/%d/%Y %I:%M %p")
            next_meal_time = last_meal_time + datetime.timedelta(hours=self.fasting_hours)
            return next_meal_time

    def get_time_left_before_next_meal(self):
        next_meal_time = self.get_next_meal()
        if next_meal_time:
            time_left = next_meal_time - datetime.datetime.now()
            return time_left
        else:
            return None