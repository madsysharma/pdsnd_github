import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_list=["january","february","march","april","may","june","july","august","september","october","november","december"]
day_list=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while(True):
        input_city = input("Please enter a city: Chicago, New York City or Washington: ")
        if input_city.lower() not in CITY_DATA:
            '''Checking for whether city was spelt wrongly/city not present in data'''
            print("Sorry, data not present for city entered. Please enter Chicago, New York City or Washington")
            continue
        else:
            print("City option {} selected!".format(input_city.lower().title()))
            break

    # get user input for month (all, january, february, ... , june)
    while(True):
        input_month = input("Please enter the month you want to filter results by: ")
        if input_month.lower() in [x for x in month_list] or input_month.lower() == "all" or input_month.lower() in [x[0:3] for x in month_list]:
            print("Month option {} selected!".format(input_month.lower().title()))
            break
        else:
            '''Checking for whether the wrong month was entered/month was spelt wrongly'''
            print("Sorry, data not present for the option entered. Please enter a valid month.")
            continue
    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while(True):
        input_day = input("Please enter the day you want to filter results by: ")
        if input_day.lower() in [x for x in day_list] or input_day.lower() == "all" or input_day.lower() in [x[0:3] for x in day_list]:
            print("Day option {} selected!".format(input_day.lower().title()))
            break
        else:
            '''Checking for wrong day/day spelt wrongly'''
            print("Sorry, data not present for the option entered. Please enter a valid day.")
            continue

    print('-'*40)
    return input_city, input_month, input_day


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
    print("Obtaining data for:\n")
    print("City: {}\n".format(city))
    print("Month: {}\n".format(month))
    print("Day of the week: {}\n".format(day))
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of the Week'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour
    df['End Hour'] = df['End Time'].dt.hour
    if month.lower() != "all":
       abbr_month_list = [x[0:3] for x in month_list]
       if month.lower() in abbr_month_list:
        """Handles for whether user entered abbreviated month"""
        filter_abbr_month = abbr_month_list.index(month.lower())+1
        df=df[df['Month'] == filter_abbr_month]
       else:
        filter_month = month_list.index(month.lower())+1
        df=df[df['Month'] == filter_month]

    if day.lower() != "all":
        abbr_day_list = [x[0:3] for x in day_list]
        if day.lower() in abbr_day_list:
            """Handles for whether user entered the abbreviated day of week"""
            day_index = abbr_day_list.index(day.lower())
            print("Day index: {}\n".format(day_list[day_index]))
            df=df[df['Day of the Week'] == day_list[day_index].lower().title()]
        else:
            df=df[df['Day of the Week'] == day.lower().title()]
    
    ind1= 0
    ind2= 5 #these two indices are for checking row numbers in the data frame
    while(True):
        """Asks for whether user wants to see raw input for every 5 rows or not."""
        answer = input("Would you like to see the raw data printed for every 5 rows? Enter yes or no:\n")
        if answer.lower() == "yes" or answer.lower() == "y":
            if(ind2 != df.shape[0]):
                print("Showing the entries:\n")
                print(df.iloc[ind1:ind2])
                ind1+=5
                ind2+=5
                continue
            elif(ind2 == df.shape[0] or ind2 > df.shape[0]):
                print("End of entries reached!\n")
                break
        else:
            print("Moving on to the statistical information....\n")
            break

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    '''Args:
       df - data frame for which the stats are to be calculated
    '''

    start_time = time.time()
    if df.size == 0:
        # checks for whether there's actually any data available
        print("Sorry, no travel time data available for the filters applied.")
    else:
        print('\nCalculating The Most Frequent Times of Travel...\n')
        # display the most common month
        if(df['Month'].unique().size > 1):
            month_mode = df['Month'].mode()[0]
            print("Most frequent month for travel is: {}".format(month_list[month_mode-1].title()))
        elif(df['Month'].unique().size == 1):
            print("Since this is already filtered by month , there's no month most frequently travelled to be shown.")
        
        # display the most common day of week
        if(df['Day of the Week'].unique().size > 1):
            day_mode = df['Day of the Week'].mode()[0]
            print("Most frequent day for travel is: {}".format(day_mode))
        elif(df['Day of the Week'].unique().size == 1):
            print("Since this is already filtered by day of the week, there's no frequently travelled day of the week to be shown")
        
        # display the most common start hour
        if(df['Start Hour'].unique().size > 1):
            hour_common = df['Start Hour'].mode()[0]
            if hour_common in range(0,12):
                time_str = str(hour_common) + " AM"
            elif hour_common in range(13,24):
                time_str = str(hour_common-12) + " PM"
            elif hour_common == 12:
                time_str="12 PM"
            print("Most frequent starting hour is: {}".format(time_str))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    '''Args:
       df - data frame for which the stats are to be calculated
    '''

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    if(df.size == 0):
        # checks if there's any data available
        print("Sorry, no station data available for filters applied.")
    else: 
        # display most commonly used start station
        if(df['Start Station'].unique().size > 1):
            common_start_station = df['Start Station'].mode()[0]
            print("The most popular starting station: {}".format(common_start_station))
        # display most commonly used end station
        if(df['End Station'].unique().size > 1):
            common_end_station = df['End Station'].mode()[0]
            print("The most popular ending station: {}".format(common_end_station))
        # display most frequent combination of start station and end station trip
        grouped_df = df.groupby(['Start Station','End Station'])['Trip Duration'].count().reset_index(name="Total Count") #groups by combination of starting and ending station
        sorted_group = grouped_df.sort_values(by="Total Count", ascending=False) #sorts in descending order
        print("The most frequently travelled station combination consists of {} as the starting station and {} as the ending station, with a grand total of {} trips".format(sorted_group.iloc[0]['Start Station'], sorted_group.iloc[0]['End Station'],sorted_group.iloc[0]['Total Count']))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    '''Args:
       df - data frame for which the stats are to be calculated
    '''
    start_time = time.time()
    if(df.size == 0):
        #checks if there's any data available
        print("Sorry, no trip duration details available for the filters applied.")
    else:
        print('\nCalculating Trip Duration...\n')
        
        # display mean travel time
        mean_travel_time = df['Trip Duration'].mean()
        print("Mean travel time: {}".format(mean_travel_time))
        
        # display total travel time
        total_travel_time = df['Trip Duration'].sum()
        print("Total travel time: {}".format(total_travel_time))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    '''Args:
       df - data frame for which the stats are to be calculated
    '''
    
    start_time = time.time()
    if(df.size == 0):
        #checks if there is any data available
        print("Sorry, no user statistics available for the filters applied.")
    else:
        print('\nCalculating User Stats...\n')
        # Display counts of user types
        user_group_df = df.groupby(['User Type'])['Trip Duration'].count().reset_index(name="Total Count of User Group")
        print("The total count for each user type:\n")
        print(user_group_df)
        print("\n")
        # Display counts of gender
        if 'Gender' in df:
            gender_group_df = df.groupby(['Gender'])['Trip Duration'].count().reset_index(name="Total Count of Gender")
            print("The total count for each gender:\n")
            print(gender_group_df)
            print("\n")
        else:
            print("Sorry, no gender-related data available for city selected.")
        # Display earliest, most recent, and most common year of birth
        if 'Birth Year' in df:
            print("The earliest birth year: {}\n".format(int(df['Birth Year'].min(skipna=True))))
            print("The latest birth year: {}\n".format(int(df['Birth Year'].max(skipna=True))))
            print("The most common year of birth: {}\n".format(int(df['Birth Year'].mode()[0])))
        else:
            print("Sorry, no information regarding birth year for city selected.\n")

        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """Calling all functions for loading data and getting the statistical information"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' or restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
