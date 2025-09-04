#!/usr/bin/python3
"""
Generator function to stream rows from user_data table one by one.
"""

import mysql.connector


def stream_users():
    """Yields rows from the user_data table as dictionaries one by one."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",        # update if using another user
            password="password",# update with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user_data;")

        for row in cursor:  # only one loop
            yield row

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
