import os
import json
import datetime
from src.data_manager import DataManager
from src.user import User

def print_next_meal(user):
    next_meal = user.get_next_meal()
    time_left = user.get_time_left_before_next_meal()
    hours, minutes = divmod(time_left.seconds, 3600)
    minutes = minutes // 60
    if next_meal:
        if time_left.total_seconds() <= 0:
            print(f"\nFasting goal reached! You can start eating now.")
        else:
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
            user.add_meal()
        elif choice == 2:
            user.update_meal()
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
