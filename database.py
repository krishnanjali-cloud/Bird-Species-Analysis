import sqlite3
from data_processing import(
    load_excel_data
)

df = load_excel_data()

def create_database(df):

    connection = sqlite3.connect(
        "database/Birds.db"
    )

    df.to_sql(
        "bird_observations",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()

