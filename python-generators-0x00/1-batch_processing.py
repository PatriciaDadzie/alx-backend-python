#!/usr/bin/python3
"""
Batch processing with Python generators.
"""

import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data in batches.
    
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",         
            password="password", 
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Processes batches of users and prints those with age > 25.
    """
    for batch in stream_users_in_batches(batch_size):  
        for user in batch:                             
            if user["age"] > 25:                       
                print(user)
