import os
import sqlite3
import pandas as pd
import threading
import logging
import smtplib
import time  # For measuring run time
from flask import Blueprint, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

etl_bp = Blueprint("etl", __name__)  # Flask Blueprint for ETL process

# Logging Setup: Log to file and terminal
LOG_FILE = "logs/etl.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

DB_PATH = "weather_data.db"
CHUNK_SIZE = 50000  # Process data in batches for efficiency

def send_email(subject, body, recipient="malhar.rananaware@gmail.com"):
    """
    Sends an email using Gmail's SMTP server.
    Note: For Gmail, you need to use an App Password if 2FA is enabled.
    """
    try:
        # Gmail SMTP server settings
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv("GMAIL_USERNAME")
        password = os.getenv("GMAIL_APP_PASSWORD")

        # Create a secure SSL/TLS connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS
        
        # Login to the server
        server.login(sender_email, password)

        # Create the email message
        message = f"Subject: {subject}\n\n{body}"
        
        # Send the email
        server.sendmail(sender_email, recipient, message)
        server.quit()
        
        logging.info(f"Email sent successfully to {recipient} with subject '{subject}'")
        print(f"Email sent successfully to {recipient} with subject '{subject}'")
    except Exception as e:
        logging.error(f"Failed to send email to {recipient}: {str(e)}")
        print(f"Failed to send email to {recipient}: {str(e)}")

def send_failure_email(error_msg):
    """Send an email alert on ETL failure."""
    subject = "ETL Failure"
    body = f"The ETL process failed with the following error:\n\n{error_msg}"
    send_email(subject, body)

def send_success_email(run_time, total_records):
    """Send an email alert on ETL success."""
    subject = "ETL Success"
    body = (
        "Your ETL job completed successfully!\n\n"
        f"Total run time: {run_time:.2f} seconds\n"
        f"Total records processed: {total_records}\n"
    )
    send_email(subject, body)

def clean_and_transform_data():
    """
    Reads raw weather data from the 'weather_data' table, cleans it,
    and saves aggregated results to a new table 'clean_weather_data'.
    This function drops the old cleaned table so that each ETL run starts fresh.
    """
    start_time = time.time()
    logging.info("=== ETL RUN START ===")
    conn = None
    offset = 0

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Drop old cleaned data table if it exists
        cursor.execute("DROP TABLE IF EXISTS clean_weather_data")
        conn.commit()

        # Create new cleaned data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clean_weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                date TEXT NOT NULL,
                avg_temperature REAL,
                weather TEXT
            )
        """)
        conn.commit()

        # Process data in chunks from the original "weather_data" table
        while True:
            df = pd.read_sql_query(
                f"SELECT * FROM weather_data LIMIT {CHUNK_SIZE} OFFSET {offset}", conn
            )
            if df.empty:
                break  # No more data to process

            # Clean 'city' and 'weather': Replace "" or "UNKNOWN" with NaN
            df["city"] = df["city"].replace(["", "UNKNOWN"], pd.NA)
            df["weather"] = df["weather"].replace(["", "UNKNOWN"], pd.NA)

            # Drop rows where city or weather is NaN
            df = df.dropna(subset=["city", "weather"])

            # Fill temperature NaN with the mean for this chunk
            df["temperature"] = df["temperature"].fillna(df["temperature"].mean())

            # Aggregation: Average temperature per city & date
            agg_df = df.groupby(["city", "date"]).agg({
                "temperature": "mean",
                "weather": "first"
            }).reset_index()
            agg_df.rename(columns={"temperature": "avg_temperature"}, inplace=True)

            # Insert cleaned data into the new table
            agg_df.to_sql("clean_weather_data", conn, if_exists="append", index=False)

            # Log chunk info
            elapsed = time.time() - start_time
            logging.info(
                f"CHUNK PROCESSED: offset={offset}, chunk_size={CHUNK_SIZE}, "
                f"records_added={len(agg_df)}, run_time={elapsed:.2f}s"
            )

            offset += CHUNK_SIZE

        total_time = time.time() - start_time
        logging.info(f"=== ETL RUN COMPLETED in {total_time:.2f}s. Total records processed: {offset} ===")

        # Send success email
        send_success_email(run_time=total_time, total_records=offset)

    except Exception as e:
        logging.error(f"ETL failed: {str(e)}")
        send_failure_email(str(e))
    finally:
        if conn:
            conn.close()

@etl_bp.route("/run", methods=["GET"])
def run_etl():
    """Trigger the ETL process asynchronously."""
    threading.Thread(target=clean_and_transform_data).start()
    return jsonify({"message": "ETL started!"})

@etl_bp.route("/status", methods=["GET"])
def etl_status():
    """Fetch the latest ETL processing logs (last 10 lines)."""
    try:
        with open(LOG_FILE, "r") as log_file:
            last_lines = log_file.readlines()[-10:]
        return jsonify({"status": last_lines})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@etl_bp.route("/cleaned_data", methods=["GET"])
def cleaned_data():
    """
    Return a sample of cleaned data from 'clean_weather_data'
    for display on the dashboard.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT city, date, avg_temperature, weather FROM clean_weather_data LIMIT 20", conn)
        conn.close()
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@etl_bp.route("/health", methods=["GET"])
def health():
    """Health-check endpoint to ensure the ETL service is up."""
    return jsonify({"status": "ok", "message": "ETL service is healthy."})
