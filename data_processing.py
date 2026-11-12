import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def filter_items(condition, dict_list):
    """
    Return a new list containing only the dictionaries that satisfy
    the given condition function.

    Args:
        condition: A function that takes a dictionary and returns True or
            False.
        dict_list: A list of dictionaries.

    Returns:
        A list of dictionaries for which condition(item) is True.

    Examples:
        >>> students = [
        ...     {"name": "Alice", "score": 90},
        ...     {"name": "Bob", "score": 70},
        ...     {"name": "Charlie", "score": 85}
        ... ]
        >>> filter_items(lambda s: s["score"] >= 85, students)
        [{'name': 'Alice', 'score': 90}, {'name': 'Charlie', 'score': 85}]
        >>> filter_items(lambda s: s["name"].startswith("A"), students)
        [{'name': 'Alice', 'score': 90}]
        >>> filter_items(lambda s: s["score"] > 100, students)
        []
    """
    result = []
    for item in dict_list:
        if condition(item):
            result.append(item)
    return result


def aggregate(aggregation_key, aggregation_function, dict_list):
    """
    Aggregate values associated with aggregation_key using the
    provided aggregation function.

    Args:
        aggregation_key: The dictionary key whose values should be aggregated.
        aggregation_function: A function such as sum, max, min, etc.
        dict_list: A list of dictionaries.

    Returns:
        The aggregated result.

    Examples:
        >>> students = [
        ...     {"name": "Alice", "score": 90},
        ...     {"name": "Bob", "score": 70},
        ...     {"name": "Charlie", "score": 85}
        ... ]
        >>> aggregate("score", sum, students)
        245
        >>> aggregate("score", max, students)
        90
        >>> aggregate("score", min, students)
        70
        >>> aggregate(
        ...     "score",
        ...     lambda scores: sum(scores) / len(scores),
        ...     students
        ... )
        81.66666666666667
    """
    values = []
    for item in dict_list:
        values.append(item[aggregation_key])
    return aggregation_function(values)


cities = []
with open(os.path.join(__location__, 'Cities.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        city = dict(r)
        city['latitude'] = float(city['latitude'])
        city['longitude'] = float(city['longitude'])
        city['temperature'] = float(city['temperature'])
        cities.append(city)

# Print first 5 cities only
for city in cities[:5]:
    print(city)

# Print the average temperature of all the cities
print("The average temperature of all the cities:")
print(aggregate('temperature', lambda temps: sum(temps) / len(temps), cities))
print()

# Print all cities in Germany
print("All cities in Germany:")
germany = filter_items(lambda city: city['country'] == 'Germany', cities)
for city in germany:
    print(city['city'])
print()

# Print all cities in Spain with a temperature above 12°C
print("Cities in Spain with a temperature above 12°C:")
spain_warm = filter_items(
    lambda city: city['country'] == 'Spain' and city['temperature'] > 12,
    cities)
for city in spain_warm:
    print(city['city'])
print()

# Count the number of unique countries
print("The number of unique countries:")
print(aggregate('country', lambda countries: len(set(countries)), cities))
print()

# Print the average temperature for all the cities in Germany
print("The average temperature for all the cities in Germany:")
print(aggregate('temperature', lambda temps: sum(temps) / len(temps), germany))
print()

# Print the max temperature for all the cities in Italy
print("The max temperature for all the cities in Italy:")
italy = filter_items(lambda city: city['country'] == 'Italy', cities)
print(aggregate('temperature', max, italy))