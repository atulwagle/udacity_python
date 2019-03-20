# write your function here
def population_density(population, land_area):
    return population / land_area


# test cases for your function
test1 = population_density(10, 1)
expected_result1 = 10
print("expected result: {}, actual result: {}".format(expected_result1, test1))

test2 = population_density(864816, 121.4)
expected_result2 = 7123.6902801
print("expected result: {}, actual result: {}".format(expected_result2, test2))


################

def readable_timedelta(days):
    return "{} week(s) and {} day(s).".format(int(days / 7), days % 7)  # or use integer division days // 7


print(readable_timedelta(10))

##############

egg_count = 0


def buy_eggs(count):
    count += 12  # purchase a dozen eggs


buy_eggs(egg_count)

print(egg_count)

#################

numbers = [
    [34, 63, 88, 71, 29],
    [90, 78, 51, 27, 45],
    [63, 37, 85, 46, 22],
    [51, 22, 34, 11, 18]
]


def mean(num_list):
    return sum(num_list) / len(num_list)


averages = list(map(mean, numbers))
print(averages)

##############

numbers = [
    [34, 63, 88, 71, 29],
    [90, 78, 51, 27, 45],
    [63, 37, 85, 46, 22],
    [51, 22, 34, 11, 18]
]

averages = list(map(lambda num_list: sum(num_list) / len(num_list), numbers))  # using lamda
print(averages)

#############

cities = ["New York City", "Los Angeles", "Chicago", "Mountain View", "Denver", "Boston"]

def is_short(name):
    return len(name) < 10

short_cities = list(filter(lambda name: len(name) < 10, cities))
print(short_cities)

##############

lessons = ["Why Python Programming", "Data Types and Operators", "Control Flow", "Functions", "Scripting"]

def my_enumerate(iterable, start=0):
    # Implement your generator function here
    for item in iterable:
        yield start, item
        start += 1

for i, lesson in my_enumerate(lessons, 1): # change the value of 1 to any number and see the output
    print("Lesson {}: {}".format(i, lesson))

###############

def chunker(iterable, size):
    # Implement function here
    """Yield successive chunks from iterable of length size."""
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

for chunk in chunker(range(25), 4):
    print(list(chunk))

###############

sq_list = [x**2 for x in range(10)]  # this produces a list of squares

sq_iterator = (x**2 for x in range(10))  # this produces an iterator of squares