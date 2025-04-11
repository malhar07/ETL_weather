# Weather Data Analytics App

This is a Flask-based web application that provides weather data analytics and visualization. The app allows you to:

- Fetch weather data from an external source.(CSV file)
- Process the data using ETL (Extract, Transform, Load) operations.
- Display the processed data in an interactive table and graph.

---

## Requirements

Before you begin, ensure that you have the following installed:

- Python 3.8 or later
- pip (Python's package installer)
- A virtual environment manager (recommended: `venv`)

---

## Setup and Installation

### Step 1: Create a Virtual Environment

Start by creating a virtual environment to isolate the project dependencies.

1. **Create a virtual environment**:
   Open your terminal and navigate to the project directory. Run the following command to create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:

   - **For macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - **For Windows**:
     ```bash
     venv\Scripts\activate
     ```

   After activating the virtual environment, you should see `(venv)` in your terminal prompt.

### Step 2: Install Dependencies

3. **Install the project dependencies**:
   Use `pip` to install the required libraries. Run the following command in your terminal:

   ```bash
   pip install -r requirements.txt
   ```

   This will install Flask, SQLAlchemy, requests, and other dependencies required for the app.

4. **Install Flask** (if not already installed):
   If Flask is not already listed in your `requirements.txt`, you can manually install it by running:

   ```bash
   pip install Flask
   ```

### Step 3: Set Up the Database

The application uses SQLite as the database.

1. **Ensure that the database file exists**:
   The app will automatically create the `weather_data.db` SQLite database when it is run for the first time, if it doesn't already exist. The database will store all the weather data fetched during the ETL process.

---

## Running the Application

### Step 4: Run the App

Once you've installed the dependencies and set up the virtual environment, you can run the Flask app.

1. **Run the Flask application**:

   In your terminal, run:

   ```bash
   python app.py
   ```

   Flask will start a development server at `http://127.0.0.1:5000/`. You can open this URL in your web browser to access the application.

---

## Project Structure

Here is an overview of the project structure:

```
/weather-data-analytics-app
│
├── app.py               # Main Flask application
├── controllers/         # Contains the controllers (ETL, bulk data handling)
├── models/              # Contains the data models (SQLAlchemy models)
├── static/              # Contains static files (CSS, JS)
│   └── css/
│       └── style.css    # Styles for the web app
├── templates/           # Contains HTML templates
│   ├── index.html       # Main page template
│   └── dashboard.html   # Dashboard page template
├── requirements.txt     # Python dependencies
├── weather_data.db      # SQLite database for weather data
└── README.md            # Project documentation (this file)
```

---

## Features

- **Home Page**: Displays a table of weather data with pagination. You can view weather details such as city, date, temperature, and weather condition.
- **Dashboard**: Allows you to interact with ETL logs, view processed records, and display weather data in charts.

---

## Accessing the Dashboard

1. After running the app, go to the following URL in your browser:
   ```
   http://127.0.0.1:5000/dashboard
   ```
   Here you can interact with weather data logs, select dates and cities, and view visual graphs.

---

## Fetching Bulk Weather Data

To fetch and mock bulk data, you can navigate to the homepage (`/`) and click on **"Fetch & Mock Bulk Data"**. This will download weather data and insert it into the database.

---

## ETL Process

- **Extract**: Data is extracted from a CSV file available at an external URL.
- **Transform**: The weather data is processed (e.g., handling missing values, cleaning data).
- **Load**: The data is inserted into the SQLite database (`weather_data.db`).

---

## Logs and Error Handling

- The **ETL Logs** section in the dashboard will show real-time logs of the ETL process. These logs are updated dynamically and provide insight into the current state of the data processing.
- If no data is available for a specific city or date, an error message will be displayed notifying the user.

---

## Database Schema

The database used in this project is an SQLite database, named `weather_data.db`. Below is the schema of the main table, which stores the weather data.

Table: `weather_data`

This table contains the processed weather data.

| Column Name   | Data Type | Description                                                                           |
| ------------- | --------- | ------------------------------------------------------------------------------------- |
| `id`          | INTEGER   | Primary key, auto-incremented identifier for each record.                             |
| `city`        | TEXT      | The name of the city for which the weather data is recorded. (e.g., "Berlin")         |
| `date`        | TEXT      | The date when the weather data was recorded, stored as a string (e.g., "2021-05-10"). |
| `temperature` | REAL      | The recorded temperature for the city on the given date. (e.g., 23.5)                 |
| `weather`     | TEXT      | The weather condition for the city on the given date (e.g., "Sunny", "Rainy").        |

#### Example Record:

| id  | city     | date       | temperature | weather |
| --- | -------- | ---------- | ----------- | ------- |
| 1   | Berlin   | 2021-05-10 | 23.5        | Sunny   |
| 2   | Paris    | 2021-05-10 | 18.0        | Cloudy  |
| 3   | New York | 2021-05-10 | 15.3        | Rainy   |

---

Notes:

- Indexes: To optimize performance for querying by city and date, appropriate indexes are created in the database for these columns.
- Data Integrity: The database ensures that no rows with missing or invalid city or date information can be inserted, maintaining the integrity of the data.

---

## Conclusion

This project provides a simple yet powerful way to manage and visualize weather data through a Flask web application. It fetches, processes, and displays weather data in an interactive and engaging way.

## Project Screenshots

I've also added images of the working Weather App project in the images folder. Below is the description of each image to provide clarity on how the project functions and the UI elements.

## image 1- Dashboard

Weather Data Dashboard Page This image showcases the Weather Data Analytics Dashboard. On the left side, it displays the ETL Process Logs where the user can view the logs of the ETL process. It also provides the Records Processed count and an option to refresh the logs. A Get Temperature button is provided below to fetch weather data based on the selected date and city. On the right side, the Average Temperature graph is presented, showcasing temperature data for various cities in a visually appealing bar chart format. This dashboard page allows users to interact with the data by selecting the desired city and date, offering a quick overview of the average temperature trends and ETL process status. The Run ETL Process button at the top triggers the ETL process, and the email functionality triggers once the ETL process completes successfully or encounters an error.

## image 2- Email

To get the results shown in the image-"email" provided in the repository, you need to first ensure that the necessary services are running. Below are the commands you need to execute:
To start the SMTP server for email functionality:
`python3 -m smtpd -n -c DebuggingServer localhost:1025`
This command starts a local SMTP server on port 1025 for email debugging. It allows the application to send email notifications related to the ETL process.

To improve the user experience and streamline the ETL process management, email notifications are sent when certain events occur during the ETL process. These notifications inform administrators about the outcome of the ETL run—whether it succeeded or failed—helping them take timely actions.

Key Features:
Email Notifications on Success: When the ETL job completes successfully, an email is sent to the system administrator. This email provides information about the ETL run, such as the number of records processed and a confirmation that the process completed successfully.

Email Notifications on Failure: In case of any errors during the ETL process, an error notification email is automatically sent. This email details the error message and any relevant information needed to troubleshoot and resolve the issue.

Local SMTP Server Setup: Due to resource constraints, the SMTP server is hosted locally within the application. The local SMTP server is used to send emails when the ETL process is triggered. The system ensures that emails are sent immediately upon either success or failure of the ETL process.

SMTP Configuration: The application uses an SMTP protocol for email sending. A local server is configured to handle outgoing emails. In a production setup, it is highly recommended to use more robust solutions such as Amazon SES, SendGrid, or Mailgun to ensure high deliverability, scalability, and reliability.

Why a Local SMTP Server?
Ease of Setup: The local SMTP server was chosen because it is easy to set up and doesn't require external dependencies or configuration of third-party services.
Resource Constraints: As the application runs locally for testing or development, using a local SMTP server offers a quick solution for email notifications without the need for additional resources.

## image 3- Health Check

To get the results shown in the image-"Health check" provided in the repository, you need to first ensure that the necessary services are running. Below are the commands you need to execute: `curl http://127.0.0.1:5000/etl/health`
The command sends an HTTP GET request to the `/etl/health` endpoint on the local server running at `127.0.0.1` on port `5000`. It is typically used to check the health status of the ETL service and ensure it is running properly.

The application includes a health check endpoint to monitor the health of the system. This endpoint ensures that all services (such as the database, API, and backend) are operating correctly.

Key Features:
Health Check Endpoint: The /health endpoint is used to confirm the application's operational status. It returns a 200 OK status if the application is functioning normally, and a 500 Internal Server Error if there is an issue with any part of the system.

Use Case: This is particularly useful for monitoring and alerting systems such as CloudWatch, Prometheus, or New Relic, which can continuously check the status of the application and send alerts if something goes wrong.

Purpose: By using this endpoint, users can proactively identify downtime or operational issues before they become critical.

## image 4- Home Page

Weather Data Table Page This image illustrates the Weather Data Table page, where users can view the weather data in a tabular format. The table includes details such as City, Date, Temperature (°C), and Weather Condition. Below the table, pagination controls are available to navigate through large datasets efficiently. This page is used to display raw weather data and provides an easy way for users to browse through data entries, with options to move between pages of the data. The Fetch & Mock Bulk Data button allows the user to generate mock data, while the Go to Dashboard button takes the user back to the Weather Data Analytics Dashboard for a more comprehensive view of the weather trends and ETL process status.

## image 5- Weather Info

Weather Data for a Specific Date and City This image shows the Weather Data Analytics Dashboard with a focus on fetching temperature for a specific city and date. In this case, the user has selected Aberdeen as the city and 01/03/2016 as the date. After clicking the Get Temperature button, a popup is displayed with the result: Temperature on 2016-01-03 in Aberdeen: 18°C. This is a feature where the user can easily retrieve temperature data for any selected date and city. The ETL Process Logs are displayed to track the progress of the data processing, and the Average Temperature graph provides a visual representation of the temperature data across multiple cities, helping the user understand temperature trends. Additionally, the cleaned data sample is shown in a table format below, showcasing the temperature data for different cities, along with their weather conditions. The Run ETL Process button can be used to initiate the ETL process for inserting new weather data, and the Refresh Logs button allows users to get the most updated log details.
