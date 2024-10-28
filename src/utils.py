# src/utils.py

def is_even(number):
    return number % 2 == 0

def is_odd(number):
    return number % 2 != 0

def max_in_list(numbers):
    if not numbers:
        raise ValueError("List is empty.")
    return max(numbers)

def min_in_list(numbers):
    if not numbers:
        raise ValueError("List is empty.")
    return min(numbers)

