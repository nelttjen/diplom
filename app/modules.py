import functools
import time

from django.db import connection, reset_queries

from diplom.settings import DEBUG


class LessonsGenerator:
    def __init__(self):
        pass


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        if DEBUG:
            print(f"View (function name): {func.__name__}")
            print(f"Queries quantity: {end_queries - start_queries}")
            print(f"Execution time: {(end - start):.2f}s")

        return result

    return inner_func