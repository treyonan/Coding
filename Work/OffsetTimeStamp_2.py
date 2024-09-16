import math

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

NewTime = CalculateOffset(13, 23, 30, 9000)

for i in NewTime:
    print(i)

daysInMonth = [25, 25, 25, 25, 25]

Month = 2
Day = 15
CurrentDayInYear = 0


for i in range(len(daysInMonth)):
    if i == Month:
        CurrentDayInYear = CurrentDayInYear + Day
        break
    CurrentDayInYear = CurrentDayInYear + daysInMonth[i]

#print(CurrentDayInYear)

