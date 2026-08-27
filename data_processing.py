import pandas as pd
import numpy as np


def load_excel_data():

    forest_file = "FOREST.XLSX"
    grassland_file = "GRASSLAND.XLSX"

    forest_excel = pd.ExcelFile(forest_file)
    grassland_excel = pd.ExcelFile(grassland_file)

    forest_list = []
    grassland_list = []

    # Forest
    for sheet in forest_excel.sheet_names:

        df = pd.read_excel(forest_file, sheet_name=sheet)

        if not df.empty:
            df["Habitat"] = "Forest"
            df["Source_Sheet"] = sheet
            forest_list.append(df)

    # Grassland
    for sheet in grassland_excel.sheet_names:

        df = pd.read_excel(grassland_file, sheet_name=sheet)

        if not df.empty:
            df["Habitat"] = "Grassland"
            df["Source_Sheet"] = sheet
            grassland_list.append(df)

    forest_df = pd.concat(forest_list, ignore_index=True)
    grassland_df = pd.concat(grassland_list, ignore_index=True)

    df = pd.concat(
        [forest_df, grassland_df],
        ignore_index=True
    )

    return df

def clean_data(df):

    df = df.copy()

    # Remove duplicate records
    df = df.drop_duplicates()

    # Date
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Year
    df["Year"] = pd.to_numeric(
        df["Year"],
        errors="coerce"
    )

    # Numeric columns
    numeric_columns = [
        "Temperature",
        "Humidity",
        "Visit",
        "AcceptedTSN",
        "Initial_Three_Min_Cnt"
    ]

    for col in numeric_columns:

        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # Standardize text columns
    text_columns = [
        "Habitat",
        "Common_Name",
        "Scientific_Name",
        "Location_Type",
        "ID_Method",
        "Sky",
        "Wind",
        "Disturbance",
        "Sex",
        "Distance"
    ]

    for col in text_columns:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype("string")
                .str.strip()
            )

    # Create month
    df["Month"] = df["Date"].dt.month_name()

    # Create month number
    df["Month_Number"] = df["Date"].dt.month

    # Create day
    df["Day"] = df["Date"].dt.day

    # Create weekday
    df["Day_Name"] = df["Date"].dt.day_name()

    # Extract observation hour
    df["Observation_Hour"] = pd.to_datetime(
        df["Start_Time"].astype(str),
        errors="coerce",
        format="%H:%M:%S"
    ).dt.hour

    return df

def add_features(df):

    df = df.copy()
    df["Observations"] = 1

    # Time period
    def classify_time(hour):

        if pd.isna(hour):
            return "Unknown"

        if hour < 7:
            return "Early Morning"

        elif hour < 10:
            return "Morning"

        elif hour < 13:
            return "Midday"

        elif hour < 16:
            return "Afternoon"

        else:
            return "Evening"

    df["Time_Period"] = df["Observation_Hour"].apply(
        classify_time
    )
    
    return df

df = load_excel_data()
df = clean_data(df)
df = add_features(df)
# print("Everything is okay.")