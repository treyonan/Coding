import math

'''
inOffset = 1525
inYear = 2024
inMonth = 9
inDay = 13
inHour = 15
inMinute = 30
'''

def CalculateOffset(inDay, inHour, inMinute, inOffset):
    _MinutesInDay = 1440
    _MinutesInHour = 60
    _Days = math.floor(inOffset/_MinutesInDay)
    _DayRemainder = inOffset % _MinutesInDay
    _Hours = math.floor(_DayRemainder/_MinutesInHour)
    _HoursRemainder = _DayRemainder % _MinutesInHour
    _Minutes = _HoursRemainder
    outDay = inDay + _Days
    outHour = inHour + _Hours + math.floor((inMinute + _Minutes) / 60)
    outMinute = (inMinute + _Minutes) % 60
    return outDay, outHour, outMinute

NewTime = CalculateOffset(13, 15, 30, 1530)

for i in NewTime:
    print(i)


'''
def calculate_offset(year, month, day, hour, minute, offset_minutes):
    # Calculate the number of days in the current month
    if month in [1, 3, 5, 7, 8, 10, 12]:
        DaysInMonth = 31
    elif month in [4, 6, 9, 11]:
        DaysInMonth = 30
    elif month == 2:
        if (year - 2024) % 4 == 0:
            DaysInMonth = 29  # Leap year
        else:
            DaysInMonth = 28  # Regular year

    # Add the offset to the current minutes
    minute += offset_minutes

    # Handle minute overflow
    if minute >= 60:
        hour += minute // 60      # Add the overflow to hours
        minute = minute % 60      # Get the remaining minutes

    # Handle hour overflow
    if hour >= 24:
        day += hour // 24         # Add the overflow to days
        hour = hour % 24          # Get the remaining hours

    # Handle day and month overflow
    if day > DaysInMonth:
        day -= DaysInMonth
        month += 1

        # Handle month overflow (and increment year)
        if month > 12:
            month = 1
            year += 1

        # Recalculate the number of days in the new month
        if month in [1, 3, 5, 7, 8, 10, 12]:
            DaysInMonth = 31
        elif month in [4, 6, 9, 11]:
            DaysInMonth = 30
        elif month == 2:
            if (year - 2024) % 4 == 0:
                DaysInMonth = 29
            else:
                DaysInMonth = 28

        # Re-check day overflow with the new month
        if day > DaysInMonth:
            day = 1
            month += 1
            if month > 12:
                month = 1
                year += 1

    # Return the adjusted timestamp in the desired format
    return f"{year}-{month:02}-{day:02} {hour:02}:{minute:02}"

# Test case: current timestamp 2024-09-30 17:46, offset of 120 minutes
current_year = 2024
current_month = 9
current_day = 30
current_hour = 17
current_minute = 46
offset = 120

# Call the function
new_timestamp = calculate_offset(current_year, current_month, current_day, current_hour, current_minute, offset)
print(new_timestamp)
'''