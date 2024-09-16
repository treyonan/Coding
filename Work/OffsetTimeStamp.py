import math

# Function to calculate the day of the year based on the given date
def day_of_year(month, day, year):
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Check for leap year
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        days_in_month[1] = 29
    
    return sum(days_in_month[:month - 1]) + day

# Function to calculate the month and day from a given day of the year, including handling transitions between years
def month_day_from_day_of_year(day_of_year, year):
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    # Check for leap year
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        days_in_month[1] = 29

    # Handle transitions between years
    while day_of_year > (366 if days_in_month[1] == 29 else 365):
        day_of_year -= (366 if days_in_month[1] == 29 else 365)
        year += 1
        # Recheck for leap year as the year changes
        days_in_month[1] = 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28

    month = 1
    while day_of_year > days_in_month[month - 1]:
        day_of_year -= days_in_month[month - 1]
        month += 1
    
    return month, day_of_year, year

# Function to calculate the new timestamp based on the offset in minutes
def calculate_offset(inYear, inMonth, inDay, inHour, inMinute, inOffset):
    _MinutesInDay = 1440
    _MinutesInHour = 60
    
    # Calculate how many full days and leftover hours/minutes
    _Days = math.floor(inOffset / _MinutesInDay)
    _DayRemainder = inOffset % _MinutesInDay
    _Hours = math.floor(_DayRemainder / _MinutesInHour)
    _Minutes = _DayRemainder % _MinutesInHour
    
    # Add the offset to the current day, hour, and minute
    outDay = inDay + _Days
    outHour = inHour + _Hours + math.floor((inMinute + _Minutes) / 60)
    outMinute = (inMinute + _Minutes) % 60

    # If the hour goes beyond 24, adjust day and hour
    if outHour >= 24:
        outDay += math.floor(outHour / 24)
        outHour = outHour % 24
    
    # Calculate the day of the year
    initial_day_of_year = day_of_year(inMonth, inDay, inYear)
    final_day_of_year = initial_day_of_year + _Days

    # Get the new month, day, and possibly adjusted year
    newMonth, newDay, newYear = month_day_from_day_of_year(final_day_of_year, inYear)
    
    # Return the new timestamp as a formatted string
    return f"{newYear:04}-{newMonth:02}-{newDay:02} {outHour:02}:{outMinute:02}"

# Test cases for different offsets
def run_tests():
    test_cases = [
        {"year": 2024, "month": 9, "day": 13, "hour": 15, "minute": 26, "offset": 12, "expected": "2024-09-13 15:38"},
        {"year": 2024, "month": 9, "day": 13, "hour": 15, "minute": 26, "offset": 120, "expected": "2024-09-13 17:26"},
        {"year": 2024, "month": 9, "day": 13, "hour": 15, "minute": 26, "offset": 1440, "expected": "2024-09-14 15:26"},
        {"year": 2024, "month": 9, "day": 13, "hour": 15, "minute": 26, "offset": 2880, "expected": "2024-09-15 15:26"},
        {"year": 2024, "month": 9, "day": 13, "hour": 15, "minute": 26, "offset": 525600, "expected": "2025-09-13 15:26"},
        {"year": 2023, "month": 12, "day": 31, "hour": 23, "minute": 59, "offset": 1, "expected": "2024-01-01 00:00"},
        {"year": 2024, "month": 2, "day": 28, "hour": 23, "minute": 59, "offset": 2, "expected": "2024-03-01 00:01"},
        {"year": 2024, "month": 2, "day": 29, "hour": 12, "minute": 0, "offset": 1440, "expected": "2024-03-01 12:00"},
        {"year": 2024, "month": 12, "day": 31, "hour": 23, "minute": 59, "offset": 1440, "expected": "2025-01-01 23:59"},
    ]

    for test in test_cases:
        result = calculate_offset(test["year"], test["month"], test["day"], test["hour"], test["minute"], test["offset"])
        if result == test["expected"]:
            print(f"Test Passed for Offset {test['offset']} with result: {result}")
        else:
            print(f"Test Failed for Offset {test['offset']}. Expected {test['expected']}, but got {result}")

# Example usage
new_timestamp = calculate_offset(2024, 9, 13, 15, 30, 1530)
print(new_timestamp)

# Run the test cases
run_tests()
