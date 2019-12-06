def has_two_adjacent_digits_same(n: int) -> bool:
    digit, n = n % 10, n // 10
    while n > 0:
        next_digit, n = n % 10, n // 10
        if digit == next_digit:
            return True
        digit = next_digit
    return False

def increasing(n: int) -> bool:
    digit, n = n % 10, n // 10
    while n > 0:
        next_digit, n = n % 10, n // 10
        if digit < next_digit:
            return False
        digit = next_digit
    return True

def run_length_exactly_two(n: int) -> bool:
    digit, n = n % 10, n // 10
    current_run_length = 1
    while n > 0:
        next_digit, n = n % 10, n // 10
        if digit == next_digit:
            current_run_length += 1
        else:
            if current_run_length == 2:
                return True
            current_run_length = 1
        digit = next_digit
    if current_run_length == 2:
        return True
    return False


assert has_two_adjacent_digits_same(12345) == False
assert has_two_adjacent_digits_same(2) == False
assert has_two_adjacent_digits_same(1123) == True
assert has_two_adjacent_digits_same(1223) == True
assert has_two_adjacent_digits_same(1233) == True
assert has_two_adjacent_digits_same(22) == True
assert increasing(12345) == True
assert increasing(54321) == False
assert increasing(123345) == True
assert increasing(12321) == False
assert run_length_exactly_two(12345) == False
assert run_length_exactly_two(11234) == True
assert run_length_exactly_two(12234) == True
assert run_length_exactly_two(112233) == True
assert run_length_exactly_two(111122) == True
assert run_length_exactly_two(111122223334455566666) == True
assert run_length_exactly_two(111122233345666) == False

n_good_passwords = sum(
    has_two_adjacent_digits_same(n) and increasing(n)
    for n in range(246540, 787419 + 1)
)
print(f"The number of good passwords in the range is: {n_good_passwords}")

n_very_good_passwords = sum(
    increasing(n) and run_length_exactly_two(n)
    for n in range(246540, 787419 + 1)
)
print(f"The number of very good passwords in the range is: {n_very_good_passwords}")