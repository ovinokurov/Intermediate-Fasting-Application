# Intermediate Fasting Application

This application helps users to keep track of their intermediate fasting by managing their meals, fasting hours, and weight. Users can add meals, update meals, update their weight, change fasting hours, and generate reports.

## Application Diagram
<table>
  <tr>
    <td colspan="3">
      <strong>main.py</strong>
      <br>
      Main Application
      <br>
      Loop & User Interface
    </td>
  </tr>
  <tr>
    <td>
      <strong>data_manager.py</strong>
      <br>
      DataManager Class
      <br>
      (Load & Save Data)
    </td>
    <td></td>
    <td>
      <strong>user.py</strong>
      <br>
      User Class
      <br>
      (User-related Operations)
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
3. Update weight: Users can input their current weight and receive a goal weight (10% less than their current weight).
4. Change fasting hours: Users can change their fasting hours.
5. Generate report: Users can generate a fasting report that includes meal history with dates, fasting hours, weight, and goal weight.
6. Save and exit: Users can save their data and exit the application.

The application uses a JSON file (`data.json`) to store user information.

