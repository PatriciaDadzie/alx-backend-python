#!/usr/bin/python3
import sqlite3
import functools

# Simple query cache dictionary
query_cache = {}

# Reuse connection decorator from before
def with_db_connection(func):
    """Decorator to open and close a DB connection automatically"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def cache_query(func):
    """Decorator to cache results of queries based on the query string"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[1] if len(args) > 1 else None)
        if query in query_cache:
            print("Fetching from cache...")
            return query_cache[query]
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users with caching to avoid redundant DB calls"""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # First call will cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call should use cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
