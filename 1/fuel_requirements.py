from math import floor

def fuel_given_mass(mass):
    return floor(mass / 3) - 2

def total_fuel_given_mass(mass, current_total=0):
    new_mass = fuel_given_mass(mass)
    if new_mass <= 0:
        return current_total
    else:
        return total_fuel_given_mass(new_mass, current_total=(current_total + new_mass))


# Examples from problem statement.
assert fuel_given_mass(12) == 2.0
assert fuel_given_mass(14) == 2.0
assert fuel_given_mass(1969) == 654.0
assert fuel_given_mass(100756) == 33583.0
assert total_fuel_given_mass(14) == 2.0
assert total_fuel_given_mass(1969) == 966.0
assert total_fuel_given_mass(100756) == 50346.0

with open('./data/1a.txt', 'rb') as f:
    fuel_requirement = sum(fuel_given_mass(int(line)) for line in f)
with open('./data/1a.txt', 'rb') as f:
    recursive_fuel_requirement = sum(total_fuel_given_mass(int(line)) for line in f)

print(f"The total näive fuel requirement is {fuel_requirement}")
print(f"The total recursive fuel requirement is {recursive_fuel_requirement}")