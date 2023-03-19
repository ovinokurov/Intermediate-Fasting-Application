# Data Folder

This folder contains the data used by the fasting application.

## Files

- `data.json`: This file stores user information, including names, fasting hours, meals, and weight data. The application reads and writes to this file to persist user data across multiple sessions.

## Usage

This folder should not be accessed or modified directly. The application's DataManager class handles all interactions with the data stored in this folder. If you need to back up or transfer data, you can copy the `data.json` file to another location.
