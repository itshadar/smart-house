import psycopg2

from config import db_config

try:
    # Establish a connection to Postgres
    connection = psycopg2.connect(
        host=db_config["POSTGRES_HOST"],
        port=db_config["POSTGRES_PORT"],
        user=db_config["POSTGRES_USER"],
        password=db_config["POSTGRES_PASSWORD"],
        database=db_config["POSTGRES_DB"]
    )

    database_name = db_config["POSTGRES_DB"]
    # Create a cursor object
    cursor = connection.cursor()

    # Check if the db_operations already exists
    cursor.execute("TRUNCATE electronicdevice CASCADE;")

    # Commit the transaction and close the connection
    connection.commit()
    cursor.close()
    connection.close()

except psycopg2.Error as e:
    print("Error:", e)
