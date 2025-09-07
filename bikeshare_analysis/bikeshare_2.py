import datetime
import calendar
import time
import pandas as pd
import numpy as np
import re

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while(True):
        city = input("Enter the name of the city you want to explore (chicago, new york city, washington): \n")
        city = city.lower().strip()
        possible_city = {r'new york( city)?':'new york city', r'chicago':'chicago', 
                         r'washington( city)?': 'washington'}

        flag = False
        for pos_city, norm_city in possible_city.items():
            if(re.fullmatch(pos_city, city)):
                city = norm_city
                flag = True
                break
        if (flag):
            break
        else:
            print("Oops.. It seems that we don't provide our services in city '{}'!".format(city))
            print("Try to enter one of the three given cities again\n")

    # get user input for month (all, january, february, ... , june)
    month = ''
    while(True):
        month = input("Enter a month you want to get data on (all, january, february...): \n")
        month = month.lower().strip()
        possible_months = {r'all( months)?': 'all', r'jan(uary)?':'january', r'feb(ruary)?':'february', r'mar(ch)?':'march',
                           r'apr(il)?':'april', 'may':'may', r'jun(e)?':'june', r'jul(y)?':'july', r'aug(ust)?':'august',
                           r'sep(tember)?':'september', r'oct(ober)?':'october', r'nov(ember)?':'november', r'dec(ember)?':'december'}
        
        flag = False
        for pos_mon,norm_mon in possible_months.items():
            if(re.fullmatch(pos_mon, month)):
                month = norm_mon
                flag = True
                break
        if(flag):
            break
        else:
            print("Oops.. There is no such month as {}!".format(month))
            print("Try enetering a month again\n")       

    # get user input for day of week (all, monday, tuesday, ... sunday)
    dow = ''
    while(True):
        dow = input("Enter a day of the week you want to get a data on (all, monday, tuesday,): \n")
        dow = dow.lower().strip()
        possible_dow = {r'all( days)?':'all', r'mon(day)?':'monday', r'tue(sday)?':'tuesday', 
                            r'wed(nesday)?':'wednesday',r'thu(rsday)?':'thursday', r'fri(day)?':'friday',
                            r'sat(urday)?':'saturday', r'sun(day)?':'sunday'}
        
        flag = False
        for pos_dow, norm_dow in possible_dow.items():
            if(re.fullmatch(pos_dow, dow)):
                dow = norm_dow
                flag = True
                break
        if(flag):
            break
        else:
            print("Oops.. There is no such day as {}!".format(dow))
            print("Try enetering a day again\n") 

    print('-'*40)
    return city, month, dow


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    global CITY_DATA
    MONTHS = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6,
              'july':7, 'august':8, 'september':9, 'october':10, 'november':11, 'december':12}
    DAYS = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6}
    
    df = pd.read_csv(f'./{CITY_DATA[city]}', parse_dates=['Start Time', 'End Time'])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    if(month!='all'):
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month'] == month]
    
    if(day!='all'):
        days = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6}
        df = df[df['day_of_week'] == days[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print(f"Most common month: {calendar.month_name[df['Start Time'].dt.month.mode()[0]]}") 

    # display the most common day of week
    print(f"Most common day of week: {calendar.day_name[df['Start Time'].dt.dayofweek.mode()[0]]}")

    # display the most common start hour
    print(f"Most common start hour: {df['Start Time'].dt.hour.mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station


    # display most commonly used end station


    # display most frequent combination of start station and end station trip


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time


    # display mean travel time


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types


    # Display counts of gender


    # Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
