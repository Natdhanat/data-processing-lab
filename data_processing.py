import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Table:
    def __init__(self, rows):
        self.rows = rows

    def filter(self, condition):
        result = []
        for row in self.rows:
            if condition(row):
                result.append(row)
        return Table(result)

    def aggregate(self, key, function):
        values = []
        for row in self.rows:
            values.append(row[key])
        return function(values)


class DataLoader:
    def __init__(self, filename):
        self.filepath = os.path.join(__location__, filename)

    def load(self):
        rows = []
        with open(self.filepath, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                row = {}
                for key in r:
                    try:
                        row[key] = float(r[key])
                    except ValueError:
                        row[key] = r[key]
                rows.append(row)
        return Table(rows)


loader = DataLoader('Cities.csv')
cities = loader.load()

# Print first 5 cities only
for city in cities.rows[:5]:
    print(city)

# Print the average temperature of all the cities
print("The average temperature of all the cities:")
print(cities.aggregate('temperature', lambda temps: sum(temps) / len(temps)))
print()

# Print all cities in Germany
print("All cities in Germany:")
germany = cities.filter(lambda city: city['country'] == 'Germany')
for city in germany.rows:
    print(city['city'])
print()

# Print all cities in Spain with a temperature above 12°C
print("Cities in Spain with a temperature above 12°C:")
spain_warm = cities.filter(
    lambda city: city['country'] == 'Spain' and city['temperature'] > 12)
for city in spain_warm.rows:
    print(city['city'])
print()

# Count the number of unique countries
print("The number of unique countries:")
print(cities.aggregate('country', lambda countries: len(set(countries))))
print()

# Print the average temperature for all the cities in Germany
print("The average temperature for all the cities in Germany:")
print(germany.aggregate('temperature', lambda temps: sum(temps) / len(temps)))
print()

# Print the max temperature for all the cities in Italy
print("The max temperature for all the cities in Italy:")
italy = cities.filter(lambda city: city['country'] == 'Italy')
print(italy.aggregate('temperature', max))