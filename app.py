from flask import Flask, render_template, request
import csv
import os
import json

app = Flask(__name__)

# Ensure the responses directory exists
os.makedirs('responses', exist_ok=True)

# Define time slots and days of the week globally
time_slots = ["08:00 - 8:50", "8:50 - 9:40", "9:50 - 10:40", "10:40 - 11:30", "11:40 - 12:30", "12:30 - 13:20", "13:20 - 14:10", "14:10 - 15:00", "15:10 - 16:00"]
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

@app.route('/')
def index():
    # Pass time slots and days to the template
    return render_template('index.html', time_slots=time_slots, days_of_week=days_of_week)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    preferences = request.form.get('preferences')

    if not name or not preferences:
        return '<p>Error: Name or preferences are missing.</p>', 400

    preferences_data = json.loads(preferences)

    # Initialize CSV with headers
    csv_data = [["Time"] + days_of_week]
    for time in time_slots:
        row = [time]
        for day in days_of_week:
            row.append(preferences_data.get(time, {}).get(day, "0"))
        csv_data.append(row)

    # Save to CSV file named after the user
    csv_file_path = f'responses/{name}.csv'
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    return f'<p>Confirmation: Preferences saved successfully for {name}!</p>'

if __name__ == "__main__":
    app.run(debug=True)
