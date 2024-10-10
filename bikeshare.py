import time
import pandas as pd
import numpy as np

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
    
    # get user input for city (chicago, new york city, washington). # While loop to handle invalid inputs
    while True:
        city = input('Would like to see data for Chicago, New York City, or Washington?: ')
        city = city.lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid Input: Please type the correct city name')

    # get user input for month (all, january, february, ... , june) # While loop to handle invalid inputs
    while True:
        month = input('Which month? January, February, March, April, May or June? or type "all" for no month filter: ')
        month = month.lower()
        if month in ['january','february','march','april','may','june','all']:
            break
        else:
            print('Invalid Input: Please type the correct month or type "all"')

    # get user input for day of week (all, monday, tuesday, ... sunday) # While loop to handle invalid inputs
    # Input an integer to refer to the day of the week (e.g. 1 = Sunday) or input "all" to select all days
    while True:
        day = input('Which day? Please type your respone as integer (e.g., 1=Sunday) or type "all" for no day filter: ')
        day_of_week = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'] 
        if day in str(list(range(1,8))): 
            # from integer 1-7 will be index to the day of week name
            day = int(day)
            day = day_of_week[day-1] 
            break
        elif day.lower() == "all":
            day = day.lower()
            break
        else:
            print('Invalid Input: Please type the correct day or type "all"')

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] =  df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def raw_data(df):
    """Displays raw data upon request by the user."""
    
    i = 0

    while True: # First 5 raw data display question
        answer = input('\nDo you want to see 5 lines of raw data? Enter yes or no.\n')
        answer = answer.lower()
        if answer == 'yes':
            print(df[i:i+5])
            i += 5
            break
        elif answer == 'no':
            print('Stopping display of raw data.')
            break
        else:
            print('Invalid Input: Please type yes or no.')

    while i < len(df) and answer != 'no': # Next 5 raw data display question 
        answer = input('Do you want to see the next 5 lines? Enter yes or no.\n')
        answer = answer.lower()
        if answer == 'yes':
            print(df[i:i+5])  # Display 5 lines of raw data
            i += 5            # Move to the next 5 lines
            if i >= len(df): # check if there are more raw data to display 
                print('No more raw data to display.')
                break    
        elif answer == 'no':
            print('Stopping display of raw data.')
            break
        else:
            print('Invalid Input: Please type yes or no.')
            continue


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display a summary of the data filtered by the selected month and day 
    print("Filter by month: {} and day: {}".format(month, day.lower()))
    
    # display the most common month
    popular_month = df['month'].mode()[0]
    count_popular_month = df[df['month'] == popular_month].count()['month']
    print("Most popular month: {}, Count: {}".format(popular_month,count_popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    count_popular_day = df[df['day_of_week'] == popular_day].count()['day_of_week']
    print("Most popular day: {}, Count: {}".format(popular_day,count_popular_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour # extract hour from the Start Time column to create an hour column 
    popular_hour = df['hour'].mode()[0] # find the most common hour (from 0 to 23)
    count_popular_hour = df[df['hour'] == popular_hour].count()['hour']
    print("Most popular hour: {}, Count: {}".format(popular_hour,count_popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    count_popular_start = df[df['Start Station'] == popular_start].count()['Start Station']
    print("Most popular start station: {}, Count: {}".format(popular_start,count_popular_start))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    count_popular_end = df[df['End Station'] == popular_end].count()['End Station']
    print("Most popular end station: {}, Count: {}".format(popular_end,count_popular_end))

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] +' Station' + ' -> ' + df['End Station'] + ' Station'
    combi_start_end = df['trip'].mode()[0]
    count_popular_combi_s_e = df['trip'].value_counts().iloc[0]
    print("Most popular trip: {}, Count: {}".format(combi_start_end,count_popular_combi_s_e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    count_travel = df['Trip Duration'].count()
    
    # display total travel time [hours]
    total_travel = df['Trip Duration'].sum()
    total_travel_min,total_travel_sec = divmod(total_travel,60)
    total_travel_hr,total_travel_min = divmod(total_travel_min,60)
    print("Total trip Duration: {} hours {} mins {} seconds, Count: {}".format(int(total_travel_hr),int(total_travel_min),int(total_travel_sec),count_travel))

    # display mean travel time [hours, minutes, seconds]
    mean_travel = df['Trip Duration'].mean()
    mean_travel_min,mean_travel_sec = divmod(mean_travel,60)
    mean_travel_hr,mean_travel_min = divmod(mean_travel_min,60)
    print("Mean trip duration: {} hours {} mins {} seconds, Count: {}".format(int(mean_travel_hr),int(mean_travel_min),int(mean_travel_sec),count_travel))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('-- User --')
    print(user_types)

    # Display counts of gender
    print('\n-- Gender --')
    if 'Gender' in df:
        gender_types = df['Gender'].value_counts()
        print(gender_types)
    else:
        print('No gender data in {}.'.format(city.title()))

    # Display earliest, most recent, and most common year of birth
    print('\n-- Year of Birth --')
    if 'Birth Year' in df:
        year_birth = df['Birth Year']
        popular_birth = year_birth.mode()[0]
        count_popular_birth = df[year_birth == popular_birth].count()['month']
        print('Oldest year of birth: {}, Youngest year of birth: {}'.format(year_birth.min(),year_birth.max()))
        print('Most common year of birth: {}, Count: {}'.format(popular_birth,count_popular_birth))
    else:
        print('No year of birth data in {}.'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        raw_data(df)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
