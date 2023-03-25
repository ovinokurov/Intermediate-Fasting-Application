# Intermediate Fasting Application

This application helps users to keep track of their intermediate fasting by managing their meals, fasting hours, and weight. Users can add meals, update meals, update their weight, change fasting hours, and generate reports.

## Application Diagram
<table border="1">
  <tr>
    <td colspan="4">
      <strong>main.py</strong>
      <br>
      Main Application
      <br>
      Loop & User Interface
    </td>
  </tr>
  <tr>
    <td colspan="2">
      <strong>Data Management</strong>
      <br>
      <strong>load_user_data</strong>
      <br>
      <strong>save_user_data</strong>
    </td>
    <td>
      <strong>Meal Operations</strong>
      <br>
      <strong>add_meal</strong>
      <br>
      <strong>update_meal</strong>
      <br>
      <strong>delete_meal</strong>
    </td>
    <td>
      <strong>User Operations</strong>
      <br>
      <strong>update_weight</strong>
      <br>
      <strong>change_fasting_hours</strong>
    </td>
  </tr>
  <tr>
    <td>
      <strong>Goal Management</strong>
      <br>
      <strong>update_cups_of_water_goal</strong>
      <br>
      <strong>count_cups_of_water_today</strong>
    </td>
    <td colspan="3">
      <strong>Reporting</strong>
      <br>
      <strong>generate_report</strong>
      <br>
      <strong>calculate_next_meal_time</strong>
    </td>
  </tr>
</table>


## How to Run

1. Ensure Python 3 is installed on your system.
2. Download or clone the repository.
3. Open a terminal or command prompt, navigate to the directory where the files are located.
4. Run `python main.py` or `python3 main.py` depending on your system.
5. Follow the on-screen prompts to use the application.

## Features

1. Add meal: Users can add meals with date and time.
2. Update meal: Users can update the date and time of their previously added meals.
3. Delete meal: Users can delete a previously added meal.
4. Update weight: Users can input their current weight.
5. Change fasting hours: Users can change their fasting hours.
6. Update cups of water goal: Users can update their daily cups of water intake goal.
7. Generate report: Users can generate a fasting report that includes meal history with dates, fasting hours, weight, and daily cups of water intake.
8. Exit: Users can exit the application.

The application uses a JSON file (user_data.json) to store user information.

