import json
import os
from datetime import datetime, timedelta

# Define constants and global variables
USER_DATA_FILE = "data/user_data.json"
FASTING_HOURS_DEFAULT = 16
CUPS_OF_WATER_GOAL_DEFAULT = 11


def load_user_data(username):
    # Check if the user_data.json file exists
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w") as f:
            f.write("{}")
        user_data = {}
    else:
        # Load user data from JSON file
        with open(USER_DATA_FILE, "r") as f:
            user_data = json.load(f)
    return user_data.get(username, {
        "weight": None,
        "last_meal": None,
        "meal_times": [],
        "fasting_hours": FASTING_HOURS_DEFAULT,
        "cups_of_water_goal": 11  
    })


def save_user_data(username, data):
    # Load user data
    user_data = {}
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE) as f:
            user_data = json.load(f)

    # Update user data
    user_data[username] = data

    # Save user data
    with open(USER_DATA_FILE, "w") as f:
        json.dump(user_data, f, default=json_serializable)


def json_serializable(obj):
    """Converts datetime objects to ISO format for JSON serialization."""
    if isinstance(obj, datetime):
        if hasattr(obj, "isoformat"):
            return obj.isoformat()
        else:
            return obj.strftime("%Y-%m-%dT%H:%M:%S.%f")
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def calculate_next_meal_time(last_meal_time, fasting_hours):
    # Calculate the time of the next meal
    next_meal_time = last_meal_time + timedelta(hours=fasting_hours)
    return next_meal_time


def add_meal(username, data):
    # Ask user for meal type and time
    meal_type = input("Enter meal type (breakfast, lunch, dinner, cup of water, snack): ")
    meal_time_input = input("Enter the time of your meal (mm/dd/yyyy hh:mm am/pm) or press enter for current time: ")
    try:
        if meal_time_input == "":
            meal_time = datetime.now()
        else:
            meal_time = datetime.strptime(meal_time_input, "%m/%d/%Y %I:%M %p")
    except ValueError:
        print("Invalid time format. Setting meal time to current time.")
        meal_time = datetime.now()

    is_last_meal_input = input("Is this your last meal for today? (y/n): ")
    if is_last_meal_input.lower() == "y":
        data["last_meal"] = meal_time
        data["next_meal"] = calculate_next_meal_time(meal_time, data["fasting_hours"])
        
    data["meal_times"].append({"type": meal_type, "time": meal_time})
    save_user_data(username, data)
    print("Meal added successfully!")


def update_meal(username, data):
    # Display list of meals
    meals = data["meal_times"]
    print("Select a meal to update:")
    for i, meal in enumerate(meals):
        print(f"{i + 1}. {meal['type']} at {datetime.fromisoformat(meal['time']).strftime('%m/%d/%Y %I:%M %p')}")
    selection = int(input("Please select a meal (or enter 0 to cancel): ")) - 1
    if selection < -1 or selection >= len(meals):
        print("Invalid selection. Please try again.")
        return
    elif selection == -1:
        print("Update meal cancelled.")
        return
    # Ask user for meal type and time
    meal_type = input("Enter meal type (breakfast, lunch, dinner, snack): ")
    meal_time_input = input("Enter the time of your meal (mm/dd/yyyy hh:mm am/pm): ")
    meal_time = datetime.strptime(meal_time_input, "%m/%d/%Y %I:%M %p")
    data["meal_times"][selection] = {"type": meal_type, "time": meal_time.isoformat()}
    save_user_data(username, data)
    print("Meal updated successfully!")


def delete_meal(username, data):
    meals = data["meal_times"]
    if not meals:
        print("No meals found to delete.")
        return

    print("Select a meal to delete:")
    for i, meal in enumerate(meals):
        meal_time = datetime.fromisoformat(meal["time"])
        print(f"{i + 1}. {meal['type']} at {meal_time.strftime('%m/%d/%Y %I:%M %p')}")
    
    selection = int(input("Please select a meal (or enter 0 to cancel): ")) - 1
    if selection < -1 or selection >= len(meals):
        print("Invalid selection. Please try again.")
        return
    elif selection == -1:
        print("Delete meal cancelled.")
        return

    del data["meal_times"][selection]
    save_user_data(username, data)
    print("Meal deleted successfully!")


def generate_report(username):
    data = load_user_data(username)
    print("")
    print("======= Intermediate Fasting Report =======")
    print(f"User: {username}")
    print(f"Current weight: {data['weight']} lbs")

    # Prompt user for time period
    print("Report for what period?")
    print("1. Today")
    print("2. This week")
    print("3. This month")
    print("4. All time")
    period_choice = input("Enter your choice (1, 2, 3, or 4): ")
    period_choice = int(period_choice)

    # Calculate start and end dates for chosen period
    today = datetime.now().date()
    if period_choice == 1:
        #Today
        start_date = today
        end_date = today
    elif period_choice == 2:
        #This week
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    elif period_choice == 3:
        #This month
        start_date = today.replace(day=1)
        next_month = today.replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)
    else:
        #All time
        start_date = datetime.min.date()
        end_date = datetime.max.date()

    print("\n+------------+-----------+---------------+")
    print("|    Date    |   Time    |   Meal Type   |")
    print("+------------+-----------+---------------+")

    meals = data.get("meal_times", [])
    total_meals = 0
    last_meal_time = None

    for meal in meals:
        meal_type = meal.get("type", "N/A")
        meal_time = datetime.fromisoformat(meal.get("time", "N/A"))

        if start_date <= meal_time.date() <= end_date:
            if last_meal_time is not None and last_meal_time.date() != meal_time.date():
                print("+------------+-----------+---------------+")

            print(f"| {meal_time.strftime('%m/%d/%Y')} | {meal_time.strftime('%I:%M %p')}  | {meal_type:<12}  |")
            last_meal_time = meal_time
            total_meals += 1

    print("+------------+-----------+---------------+")
    print(f"\nTotal meals: {total_meals}")


def change_fasting_hours(username, data):
    # Ask user for their new fasting hours
    fasting_hours = int(input("Enter your new fasting hours: "))
    data["fasting_hours"] = fasting_hours
    if data["last_meal"] is not None:
        data["next_meal"] = calculate_next_meal_time(data["last_meal"], data["fasting_hours"])
    save_user_data(username, data)
    print("Fasting hours updated successfully!")


def update_weight(username, data):
    # Ask user for their new weight
    weight = float(input("Enter your weight in pounds: "))
    data["weight"] = weight
    save_user_data(username, data)
    print("Weight updated successfully!")


def display_next_meal_and_fasting_goal(data):
    fasting_hours = data["fasting_hours"]
    if data["last_meal"] is None:
        next_meal = datetime.now() + timedelta(hours=fasting_hours)
    else:
        next_meal = calculate_next_meal_time(data["last_meal"], fasting_hours)
    remaining_time = next_meal - datetime.now()
    if remaining_time.total_seconds() < 0:
        print("Fasting goal reached! You can eating now.")
    else:
        print(f"Next meal at: {next_meal.strftime('%I:%M %p')}")
        print(f"Remaining fasting time: {str(remaining_time).split('.')[0]}")


def calculate_next_meal_time(last_meal_time, fasting_hours):
    # Check if last_meal_time is a string, and convert to string if not
    if not isinstance(last_meal_time, str):
        last_meal_time = last_meal_time.isoformat()

    # Convert fasting_hours to an integer
    fasting_hours = int(fasting_hours)

    # Calculate the time of the next meal
    next_meal_time = datetime.fromisoformat(last_meal_time) + timedelta(hours=fasting_hours)
    return next_meal_time


def update_cups_of_water_goal(username, data):
    # Ask user for their new cups of water goal
    new_goal = int(input("Enter your new daily cups of water goal: "))
    data["cups_of_water_goal"] = new_goal
    save_user_data(username, data)
    print("Daily cups of water goal updated successfully!")


def count_cups_of_water_today(username, data):
    today_date = datetime.now().date()
    cups_of_water_today = 0
    cups_of_water_goal = data.get("cups_of_water_goal", CUPS_OF_WATER_GOAL_DEFAULT)

    for meal in data["meal_times"]:
        meal_time = meal["time"]
        if not isinstance(meal_time, datetime):
            meal_time = datetime.fromisoformat(meal_time)
        meal_date = meal_time.date()

        if meal["type"] == "cup of water" and meal_date == today_date:
            cups_of_water_today += 1

    print(f"Today, you have consumed {cups_of_water_today} cups of water.")
    if cups_of_water_today >= cups_of_water_goal:
        print("Congratulations! You have reached your daily water intake goal.")
    else:
        remaining_cups = cups_of_water_goal - cups_of_water_today
        print(f"You need to drink {remaining_cups} more cups of water to reach your daily goal.")


# Define main function
def main():
    # Ask user for name and load user data
    username = input("Enter your name: ")
    data = load_user_data(username)

    # Display main menu and handle user input
    while True:
        print("")
        print("========== Intermediate Fasting ==========")
        display_next_meal_and_fasting_goal(data)
        print("==========================================")
        print("")
        print("Main Menu:")
        print("1. Add meal")
        print("2. Update meal")
        print("3. Delete Meal")
        print("4. Update weight")
        print("5. Change fasting hours")
        print("6. Update cups of water goal")
        print("7. Generate report")
        print("8. Exit")
        selection = int(input("Please select an option: "))
        if selection == 1:
            add_meal(username, data)
        elif selection == 2:
            update_meal(username, data)
        elif selection == 3:
            delete_meal(username, data)
        elif selection == 4:            
            update_weight(username, data)            
        elif selection == 5:
            change_fasting_hours(username, data)
        elif selection == 6:
            update_cups_of_water_goal(username, data)
        elif selection == 7:
            generate_report(username)
            count_cups_of_water_today(username, data)            
        elif selection == 8:
            break
        else:
            print("Invalid selection. Please try again.")

    print("Exiting Intermediate Fasting Application...")

if __name__ == "__main__":
    main()
