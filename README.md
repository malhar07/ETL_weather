# Weather Data Analytics App

A Flask-based web application designed to analyze and visualize weather data. It allows users to:

- Fetch weather data from a CSV file (external source)
- Perform ETL (Extract, Transform, Load) operations
- Display data in interactive tables and visual charts

---

## Requirements

Make sure the following tools are installed before proceeding:

- Python 3.8 or higher
- pip
- Virtual environment tool (`venv` recommended)

---

## Getting Started

### Step 1: Set Up a Virtual Environment

1. Navigate to your project directory and run:
   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```

### Step 2: Install Dependencies

3. Install all required libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. If Flask isn’t listed in the requirements file, install it manually:
   ```bash
   pip install Flask
   ```

### Step 3: Database Setup

The SQLite database (`weather_data.db`) is automatically created the first time the app is run, if it doesn’t already exist.

---

## Running the App

Run the Flask server using:

```bash
python app.py
```

Then open your browser and go to: `http://127.0.0.1:8080/`

---

## Project Structure

```
/weather-data-analytics-app
├── app.py               # Main Flask app
├── controllers/         # ETL and data control logic
├── models/              # SQLAlchemy data models
├── static/css/          # Stylesheets
├── templates/           # HTML templates
│   ├── index.html
│   └── dashboard.html
├── weather_data.db      # SQLite database
├── requirements.txt     # Python dependencies
└── README.md            # This documentation
```

---

## Features

- **Home Page**: View weather data in a paginated table.
- **Dashboard**: Monitor ETL logs, get temperature by city/date, and visualize temperature trends using graphs.

---

## Dashboard Access

Visit the dashboard at:

```
http://127.0.0.1:8080/dashboard
```

Here, users can trigger the ETL process, refresh logs, fetch weather data by date/city, and view average temperature graphs.

---

## Bulk Data Fetching

From the homepage, use the **Fetch & Mock Bulk Data** button to populate the database with weather records for testing and analysis.

---

## ETL Process

- **Extract**: Read data from a remote CSV source.
- **Transform**: Clean, filter, and process weather data.
- **Load**: Store the processed data into the SQLite database.

---

## Logs and Error Handling

- ETL logs are shown in real-time on the dashboard.
- Users are notified if data is missing or a fetch fails.

---

## Database Schema

**Table**: `weather_data`

| Column       | Type    | Description                                   |
|--------------|---------|-----------------------------------------------|
| `id`         | INTEGER | Auto-incremented primary key                  |
| `city`       | TEXT    | City name                                     |
| `date`       | TEXT    | Date of weather record (e.g., "2021-05-10")   |
| `temperature`| REAL    | Recorded temperature in Celsius               |
| `weather`    | TEXT    | Weather condition (e.g., Sunny, Rainy)        |

**Sample Rows**:

| id | city   | date       | temperature | weather |
|----|--------|------------|-------------|---------|
| 1  | London | 2021-05-10 | 23.5        | Sunny   |
| 2  | Mumbai | 2021-05-10 | 18.0        | Cloudy  |

*Indexes are applied on `city` and `date` for optimized lookups.*

---

## Email Notification System

To simulate email alerts for ETL success/failure:

1. Run a local SMTP server:
   ```bash
   python3 -m smtpd -n -c DebuggingServer localhost:1025
   ```

2. Emails are sent when:
   - The ETL completes successfully
   - An error occurs during the ETL process

> The SMTP setup is for local testing. In production, use services like Amazon SES, SendGrid, or Mailgun.

---

## Health Check Endpoint

Monitor the service health using:

```bash
curl http://127.0.0.1:5000/etl/health
```

Returns a `200 OK` if everything is running fine, or a `500` if there are issues.

---

## UI Snapshots

### Image 1 – Dashboard
Displays the ETL log panel, temperature graphs, and controls to fetch data by city/date.

### Image 2 – Email
Displays example email alerts sent after ETL runs. Uses local SMTP for testing notifications.

### Image 3 – Health Check
Illustrates how the `/health` endpoint returns service status.

### Image 4 – Home Page
A data table listing weather records with pagination and options to mock bulk data.

### Image 5 – Weather Info
Shows city/date-specific temperature results and ETL logs.

---

## Conclusion

This app offers a complete workflow for weather data processing and visualization. It includes real-time logging, email alerts, data validation, and user-friendly interfaces—all powered by Flask and SQLite.
