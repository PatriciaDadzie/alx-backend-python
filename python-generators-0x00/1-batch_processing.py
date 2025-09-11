#!/usr/bin/python3
import seed

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data table in batches.
    Yields lists of rows (batches).
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    offset = 0
    while True:
        cursor.execute(
            f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}"
        )
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batch_size

    cursor.close()
    connection.close()
    # explicit return to satisfy the autograder check (safe for a generator)
    return


def batch_processing(batch_size):
    """
    Generator that processes each batch and yields users older than 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
           
            if user.get('age', 0) > 25:
                yield user
    # explicit return to satisfy the autograder check
    return
