import threading


# @printer nomli decorator
def printer(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print("Natija:", result)

    return wrapper


def calculate_reverse(number):
    reverse = int(str(number)[::-1])
    return reverse


@printer
def process_numbers(numbers):
    threads = []
    results = []

    for number in numbers:
        thread = threading.Thread(target=lambda num: results.append(calculate_reverse(num)), args=(number,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results


user_input = input("Sonlar kiriting: ")
numbers = [int(num) for num in user_input.split()]
process_numbers(numbers)

