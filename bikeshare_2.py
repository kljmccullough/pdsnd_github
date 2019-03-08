import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def promptUser(data_list, prompt, fail_message):
    value = ""
    valid_input = False
    while not valid_input:
        value = input(prompt).lower()
        if value in data_list:
            valid_input = True
        else:
            print(fail_message)
    return value

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    city_prompt = 'What city do you want to explore?\n'
    city_fail = 'Data for that city is currently unavailable. Please select chicago, new york city, or washington.'
    month_prompt = 'What month do you like statistics for?\n'
    month_fail = "Oops, that isn't a month. Please check your spelling."
    day_prompt = 'What day would you like statistics for?\n'
    day_fail = "Oops, that isn't a day. Please check your spelling."
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = promptUser(CITY_DATA.keys(), city_prompt, city_fail)
       
    # TO DO: get user input for month (all, january, february, ... , june)
    month = promptUser(months, month_prompt, month_fail)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = promptUser(days, day_prompt, day_fail)

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month_index = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month_index]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    popular_month = df['month'].mode()
    month_message = 'Most Common Months: '
    for i in range(0, len(popular_month)):
        mode = popular_month[i]
        month_message += months[mode - 1].title()
        if i != len(popular_month) - 1:
            month_message += ' and '
    print(month_message)
    
    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()
    day_message = 'Most Common Day: '
    for i in range(0, len(popular_day)):
        mode = popular_day[i]
        day_message += mode.title()
        if i != len(popular_day) - 1:
            day_message += ' and ' 
    print(day_message)

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()
    hour_message = 'Most Common Start Hour: '
    for i in range(0, len(popular_hour)):
        mode = popular_hour[i]
        hour_message += str(mode)
        if i != len(popular_hour) - 1:
            hour_message += ' and '
    print(hour_message)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()
    start_station_message = 'Most Popular Start Station: '
    for i in range(0, len(popular_start_station)):
        mode = popular_start_station[i]
        start_station_message += mode.title()
        if i != len(popular_start_station) - 1:
            start_station_message += ' and ' 
    print(start_station_message)
    
    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()
    end_station_message = 'Most Popular End Station: '
    for i in range(0, len(popular_end_station)):
        mode = popular_end_station[i]
        end_station_message += mode.title()
        if i != len(popular_end_station) - 1:
            end_station_message += ' and '
    print(end_station_message)

    # TO DO: display most frequent combination of start station and end station trip
    df['Trips'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['Trips'].mode()
    trip_message = 'Most Popular Trip: '
    for i in range(0, len(popular_trip)):
        mode = popular_trip[i]
        trip_message += mode.title()
        if i != len(popular_trip) - 1:
            trip_message += ' and '
    print(trip_message)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Time Traveled:', total_travel_time)
    
    # TO DO: display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time:', avg_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('Count of User Type: ')
    for name, value in user_type_count.iteritems():
        print('\t' + name + ': ' + str(value))
    
    # TO DO: Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('Count by Gender: ')
        for name, value in gender_count.iteritems():
            print('\t' + name + ': ' + str(value))
    except Exception as e:
        print('No gender data is available for this city.')
        
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        sorted_yob = df['Birth Year'].dropna().sort_values()
        print('Earliest Birth Year: ', sorted_yob.iloc[0])
        print('Most Recent Birth Year: ', sorted_yob.iloc[len(sorted_yob) - 1])
    
        yob_mode = df['Birth Year'].mode()     
        yob_mode_message = 'Most Common Year of Birth: '
        for i in range(0, len(yob_mode)):
            mode = yob_mode[i]
            yob_mode_message += mode
            if i != len(yob_mode) -1:
                yob_mode_message += ' and '
        print(yob_mode_message)
    except Exception as e:
        print('No birth year data is available for this city.')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    accepted_responses = ['yes', 'ye', 'y', 'no', 'n']
    raw_prompt = 'Would you like to view raw data?'
    raw_fail = "Oops, your response could not be understood. Please enter yes or no."   
    keep_going = True
    user_input = promptUser(accepted_responses, raw_prompt, raw_fail)
    if user_input == 'yes' or user_input == 'ye' or user_input == 'y':
        a = 0
        while keep_going:
            print(df.loc[a:a+4])
            keep_going_prompt = 'Would you like to view more rows?'
            keep_going_input = promptUser(accepted_responses, keep_going_prompt, raw_fail)
            a += 5
            if keep_going_input == 'no' or keep_going_input == 'n':
                keep_going = False
            

def main():
    while True:
        city, month, day = get_filters()
        result = load_data(city, month, day)
        time_stats(result)
        station_stats(result)
        trip_duration_stats(result)
        user_stats(result)
        raw_data(result)
    
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
