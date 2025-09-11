#!/usr/bin/python3
import seed

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data table in batches
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    offset = 0
    while True:
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows   
        offset += batch_size

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes each batch of users by filtering users over the age of 25
    """
    for batch in stream_users_in_batches(batch_size):   # loop 1
        for user in batch:                              # loop 2
            if user['age'] > 25:
                yield user   
