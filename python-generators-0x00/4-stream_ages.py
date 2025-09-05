#!/usr/bin/python3
"""
Memory-efficient aggregation with Python generators.
"""

import seed


def stream_user_ages():
    """
    Generator that streams user ages one by one from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data;")
    for row in cursor:  
        yield row["age"]
    cursor.close()
    connection.close()


def compute_average_age():
    """
    Computes the average age using the generator without loading all rows into memory.
    """
    total = 0
    count = 0
    for age in stream_user_ages():  
        total += age
        count += 1
    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")
