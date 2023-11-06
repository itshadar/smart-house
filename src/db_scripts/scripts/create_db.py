import psycopg2

from src.config import db_config

try:
    # Establish a connection to Postgres
    connection = psycopg2.connect(
        host=db_config["POSTGRES_HOST"],
        port=db_config["POSTGRES_PORT"],
        user=db_config["POSTGRES_USER"],
        password=db_config["POSTGRES_PASSWORD"],
    )

    database_name = db_config["POSTGRES_DB"]
    # Create a cursor object
    cursor = connection.cursor()

    # Check if the db_operations already exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (database_name,))
    exists = cursor.fetchone()

    if not exists:
        connection.set_isolation_level(0)
        # Create the db_operations if it doesn't exist
        cursor.execute(f"CREATE DATABASE {database_name};")
        connection.set_isolation_level(1)

    # Commit the transaction and close the connection
    connection.commit()
    cursor.close()
    connection.close()

except psycopg2.Error as e:
    print("Error:", e)
