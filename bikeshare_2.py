import time
import pandas as pd
import numpy as np
from tabulate import tabulate

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
    valid_city = ['Chicago','New York City','Washington']
    city = 0
    while city not in valid_city:
        city = input('\nEnter the city you want to see the data for (Chicago, New York City, or Washington) :\n' ).title()
    
    # get user input for month (all, january, february, ... , june)
    valid_month = ['january', 'february', 'march', 'april', 'may', 'june','all']
    month = 0
    while month not in valid_month:
        month = input('\nEnter the month you want to see the data for (January, Febrauary, March,....etc OR ALL) :\n' ).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']
    day = 0
    while day not in valid_day:
        day = input('\nEnter the day you want to see the data for (Sunday, Monday,....etc OR ALL) :\n' ).lower()

    print('-'*40)
    return city, month, day


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
    if city == 'Chicago':
        df = pd.read_csv('chicago.csv')
        
    elif city == 'New York City':
        df = pd.read_csv('new_york_city.csv')
        
    elif city == 'Washington':
        df = pd.read_csv('washington.csv')
    
    #Converting Start Time column type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #Filter month
    df['Month'] = df['Start Time'].dt.month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['Month'] == month]
    
    #Filter day
    df['Day of Week'] = df['Start Time'].dt.dayofweek
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    if day != 'all':
        day = days.index(day)
        df = df[df['Day of Week'] == day]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    common_month = df['Month'].mode()[0]
    print('\nMost common month: ', common_month)

    # display the most common day of week
    df['Day'] = df['Start Time'].dt.weekday_name
    common_day = df['Day'].mode()[0]
    print('\nMost common day: ', common_day)

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    print('\nMost common hour: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].value_counts().idxmax()
    start_count = df['Start Station'].value_counts()[0]
    print('\nMost common start station is ',common_start, '\nIt appeared', start_count,' times')
        
    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    end_count = df['End Station'].value_counts()[0]
    print('\nMost common end station is ',common_end, '\nIt appeared', end_count,' times')
        
    # display most frequent combination of start station and end station trip
    df['Commute'] = df['Start Station'] + ' to ' + df['End Station']
    common_commute = df['Commute'].mode()[0]
    commute_count = df['Commute'].value_counts()[0]
    print('\nMost common commute is ',common_commute, '\nIt appeared', commute_count,' times')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
        
    #Creating trip duration column
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Trip Duration'] = df['End Time'] - df['Start Time']
        
    # display total travel time
    total_trip_time = df['Trip Duration'].sum()
    print('\nTotal trip time: ',total_trip_time)

    # display mean travel time
    avg_trip_time = df['Trip Duration'].mean()
    print('\nAverage trip time :', avg_trip_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    type_count = df['User Type'].value_counts()
    print('\nUser types and count:\n',type_count)

    # Display counts of gender
    if city == 'Washington':
        print('\nGender data was not collected for this city')
    else:
        gender_count = df['Gender'].value_counts()
        print('\nGender count:\n',gender_count)

    # Display earliest, most recent, and most common year of birth
    if city == 'Washington':
        print('\nBirth data was not collected for this city')
    else:
        earliest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print('\nYoungest serivce user was born in {}. \nWhile the oldest was born in {}. \nThe most common birth year is {}.'.format(youngest,earliest,common_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def raw_data(df):
    '''Displays raw data for users 5 rows at a time'''
    
    pd.set_option('display.max_columns',200)
    
    i=0
    while True:
        data_prompt = input('\nWould you like to see 5 lines of raw data? Enter yes or no\n').lower()
        if data_prompt != 'yes':
            break
        print(tabulate(df.iloc[np.arange(0+i,5+i)], headers ="keys"))
        i += 5
    
    #data_prompt = input('\nWould you like to see the first 5 rows of data? Enter yes or no.\n').lower()
    #ini_loc = 0
    #while data_prompt == 'yes':
    #    print(df.iloc[ini_loc: ini_loc + 5])
    #    ini_loc += 5
    #    data_prompt = input('\nWould you like to see the next 5 rows of data?\n').lower()'''

    
def main():
    while True:
        city, month, day = get_filters()
        
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
