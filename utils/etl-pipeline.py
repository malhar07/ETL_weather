import pandas as pd
import numpy as np

# Load dataset
# csv_url = "https://corgis-edu.github.io/corgis/datasets/csv/weather/weather.csv"
df = pd.read_csv("/Users/shubhamindulkar/Downloads/weather.csv")
print(df.head(10))

# ===============================
# 🧹 DATA CLEANING STEPS
# ===============================

# 1️⃣ Drop unnecessary columns
drop_columns = ["Station.Code", "Station.Location", "Station.State"]
df.drop(columns=drop_columns, inplace=True)

# 2️⃣ Handle missing values
df["Data.Precipitation"].fillna(0, inplace=True)  # Assume missing precipitation means no rain
df["Data.Temperature.Avg Temp"].fillna(df["Data.Temperature.Avg Temp"].mean(), inplace=True)
df.dropna(subset=["Station.City", "Date.Full"], inplace=True)  # Drop rows where city or date is missing

# 3️⃣ Remove duplicate rows
df.drop_duplicates(subset=["Station.City", "Date.Full"], keep="first", inplace=True)

# 4️⃣ Normalize text data (convert city names to lowercase)
df["Station.City"] = df["Station.City"].str.lower()

# 5️⃣ Convert Date to datetime format
df["Date.Full"] = pd.to_datetime(df["Date.Full"], format="%Y-%m-%d")

# ===============================
# 🔄 DATA TRANSFORMATION STEPS
# ===============================

# 6️⃣ Create new calculated fields
df["Temperature Difference"] = df["Data.Temperature.Max Temp"] - df["Data.Temperature.Min Temp"]

def categorize_wind_speed(speed):
    if speed < 5:
        return "Calm"
    elif 5 <= speed <= 15:
        return "Moderate"
    else:
        return "Windy"

df["Wind Category"] = df["Data.Wind.Speed"].apply(categorize_wind_speed)

# 7️⃣ Bucket Temperature into Ranges
def temperature_category(temp):
    if temp < 0:
        return "Freezing"
    elif temp < 10:
        return "Cold"
    elif temp < 20:
        return "Mild"
    elif temp < 30:
        return "Warm"
    else:
        return "Hot"

df["Temperature Category"] = df["Data.Temperature.Avg Temp"].apply(temperature_category)

# 8️⃣ Convert Data Types for efficient storage
df["Date.Month"] = df["Date.Full"].dt.month.astype(int)
df["Date.Year"] = df["Date.Full"].dt.year.astype(int)
df["Date.Week"] = df["Date.Full"].dt.isocalendar().week.astype(int)

df["Data.Precipitation"] = df["Data.Precipitation"].astype(float)
df["Data.Wind.Speed"] = df["Data.Wind.Speed"].astype(float)
df["Data.Temperature.Avg Temp"] = df["Data.Temperature.Avg Temp"].astype(float)


print(df.head(10))
# # ===============================
# # 🚀 READY FOR LOADING INTO DATABASE
# # ===============================

# # Display cleaned & transformed dataset
# import ace_tools as tools

# # Show the first 20 rows in a table
# tools.display_dataframe_to_user("Cleaned & Transformed Weather Data", df.head(20))
