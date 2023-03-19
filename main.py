import os
import sys
import json
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from data_manager import DataManager
from user import User


def print_next_meal(user):
    next_meal = user.get_next_meal()
    if next_meal:
        time_left = user.get_time_left_before_next_meal()
        hours, minutes = divmod(time_left.seconds, 3600)
        minutes = minutes // 60
        print(f"\nNext meal: {next_meal.strftime('%m/%d/%Y %I:%M %p')}")
        print(f"Time left before next meal: {hours} hours {minutes} minutes")
    else:
        print("\nNo meals recorded yet.")

def main():
    data_manager = DataManager()
    data = data_manager.load_data()
    name = input("What is your name? ").strip()

    if name in data:
        user = User.from_dict(data[name])
    else:
        user = User(name)
        data[name] = user.to_dict()

    while True:
        print_next_meal(user)
        print("\nOptions:")
        print("1. Add meal")
        print("2. Update meal")
        print("3. Update weight")
        print("4. Change fasting hours")
        print("5. Generate report")
        print("6. Save and exit")

        choice = int(input("Choose an option (1-6): "))

        if choice == 1:
            meal_time = input("Enter the date and time of your meal (mm/dd/yyyy hh:mm am/pm): ")
            if not user.model.weight_data:
                weight = float(input("Please enter your current weight: "))
            else:
                weight = None
            user.add_meal(meal_time, weight=weight)
        elif choice == 2:
            print("Meal history:")
            for i, meal in enumerate(user.model.meals, 1):
                print(f"{i}. {meal['time']}")
            meal_index = int(input("Enter the meal number you want to update: ")) - 1
            new_time = input("Enter the new date and time for this meal (mm/dd/yyyy hh:mm am/pm): ")
            user.update_meal(meal_index, new_time)
        elif choice == 3:
            current_weight = float(input("Please enter your current weight: "))
            user.update_weight(current_weight)
        elif choice == 4:
            new_hours = int(input("Enter your desired fasting hours: "))
            user.change_fasting_hours(new_hours)
        elif choice == 5:
            report = user.generate_report()
            print(report)
        elif choice == 6:
            data[name] = user.to_dict()
            data_manager.save_data(data)
            print("Data saved. Exiting the application.")
            break
        else:
            print("Invalid option. Please choose a valid option (1-6).")

if __name__ == "__main__":
    main()
