# This file is for random functions and variables that dont fit anywhere else
days_of_week = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
months = ('January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')

'''Gets the day of the week'''
def get_day(day:int):
    return days_of_week[day]

'''Gets month name from month number from 0 - 11'''
def get_month(month:int):
    return months[month]