from math import floor

def fuel_given_mass(n):
    return floor(n / 3) - 2

# Examples from problem statement.
assert fuel_given_mass(12) == 2.0
assert fuel_given_mass(12) == 2.0
assert fuel_given_mass(1969) == 654.0
assert fuel_given_mass(100756) == 33583.0

with open('./data/1a.txt', 'rb') as f:
    fuel_requirement = sum(fuel_given_mass(int(line)) for line in f)

print(f"The total fuel requirement is {fuel_requirement}")