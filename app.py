from statistics import mean, pstdev
from numpy import False_
from flask import Flask, render_template, request
from sqlalchemy import false
import pandas as pd

from DV_Option_1.option_1 import generate_design_option_one
from DV_Option_2.option_2 import generate_design_option_two
from DV_Option_3.option_3 import generate_design_option_three

# This file contains all the code that starts up the flask server for our webapp.

app = Flask(__name__)

productivityResult = 0

IS_LAST_SESSION_RATED = False # Default when server starts up
TOTAL_SESSIONS_DATA_CSV = 'CSV/test.csv' # CSV record that contains data for the Design Option Visualizations

# CSV record that contains data for a single study session to compute average lux and humididty averages to represent a singular study session
TEST_INDIVIDUAL_SESSION_DATA_CSV = 'CSV/10_55_54_7_7_2022.csv'

# Function that reads csv files and converts them into a Pandas Dataframe
# that can be used to easily manipulate the data and create data visualizations.
def read_csv(is_individual_session_file=False):
    # Depends on what action is performed by the user on the web app,
    # we decide which csv file to be read
    if is_individual_session_file:
        df = pd.read_csv(TEST_INDIVIDUAL_SESSION_DATA_CSV)
    else:
        df = pd.read_csv(TOTAL_SESSIONS_DATA_CSV, index_col=0)
    return df

# Function that processes the individual study session data csv
def process_indiviual_session_data():
    df_individual = read_csv(True)
    print(df_individual.head())

    # Computing Averages to represent session
    session_average_lux = mean(list(df_individual['Lux']))
    session_average_humididty= mean(list(df_individual['Humidity']))

    # Computing Standard Deviation to account for variation in data
    session_std_lux = pstdev(list(df_individual['Lux']))
    session_std_humididty= pstdev(list(df_individual['Humidity']))

    # Updating Total Session csv with new row for new individual session
    df_total = read_csv()
    df_total.iloc[-1] = [session_average_lux, session_average_humididty, 0, session_std_lux, session_std_humididty]
    df_total.to_csv(TOTAL_SESSIONS_DATA_CSV, index=false)
    
# Function that determines if the user has completed the questionaire (rated their productivity) for the last study session    
def determine_if_last_session_rated(df):
    # Get last productivity value in dataframe
    rating = df['productivity'].iloc[-1]

    # A rating of 0 means that the value is empty and no rating has been assigned
    if rating == 0:
        return False
    return True

# Function that updates the productivity rating of the last study session row, based on the questionnaire rating from the user
def update_last_session_rating(is_last_session_rated, df, rating):
    if is_last_session_rated:
        return df
    df['productivity'].iloc[-1]= rating

    # Updating the total sessions csv by writing the dataframe into a csv
    df.to_csv(TOTAL_SESSIONS_DATA_CSV, index=false)
    return df

# Function that creates a list from [0,.., n] where n is the number of rows in the total sessions csv
def get_length_df(df):
    length = []
    cur = 0
    for x in range(len(df['light'])):
        length.append(cur)
        cur += 1

# Function that computes the optimal light and humidity environment value based on productivity ratings
def compute_optimal_light_and_humidity_value(df):
    # Finding max productivity rating and finding all rows with this value
    max_rating = df['productivity'].max()
    df.loc[df['productivity'] == max_rating]

    # Computing average from optimal light and humidity values
    average_optimal_light_value = mean(list(df['light']))
    average_optimal_humidity_value = mean(list(df['humidity']))

    return [round(average_optimal_light_value,2), round(average_optimal_humidity_value,2)]

# app.route dictates what html page is loaded when the user enters the website based on their url
# ex. {WEBSITE_URL}/ - opens homepage
# ex. {WEBSITE_URL}/design-option-1 - opens design option #1
# ex. {WEBSITE_URL}/design-option-3 - opens design option #3

# Launch homepage
@app.route('/')
def start():
    return render_template('homepage.html')

# Launch the questionaire after a user stops a study session
@app.route('/dashboard')
def index():
    # Read total number of sessions csv to determine if a productivity rating was assigned 
    # to the last study session row. If yes, do not launch the productivity questionaire and if no,
    # launch the questionnaire and update the csv record with the newly computed value
    df = read_csv()
    is_last_session_rated = determine_if_last_session_rated(df)
    df = update_last_session_rating(is_last_session_rated, df,productivityResult)
    return render_template('index.html', is_last_session_rated=is_last_session_rated)

# show the productivity score after completing the study session questionaire
@app.route('/productivityResult', methods=['GET', 'POST']) #obtain the required information using http requests
def productivityResult():
    # using the post method get the required information from the questionaire using the name tag of the input fields
    try:
        if request.method == 'POST':
            stressStart = request.form.get('stressSelect')
            stressEnd = request.form.get('stressSelectEnd')
            energyStart = request.form.get('energySelect')
            energyEnd = request.form.get('energySelectEnd')

            # calculate a productivity score for the user inputed data
            productivity = stressStart - stressEnd + (5-energyStart-energyEnd)
            if productivity>6:
                productivityResult = 3
            elif productivity>3:
                productivityResult = 2
            else:
                productivityResult = 1
                
        df = read_csv()
        is_last_session_rated = determine_if_last_session_rated(df)
        df = update_last_session_rating(is_last_session_rated, df,productivityResult) #pass the productivity score to the DV csv
        return render_template('productivityResult.html', is_last_session_rated=is_last_session_rated, surveyResult = str(productivityResult))

    except:
        return render_template('productivityResult.html', is_last_session_rated=is_last_session_rated,  surveyResult = "0")

# Shows the first design option
@app.route('/design-option-1')
def design_option_1():
    df = read_csv()
    is_last_session_rated = determine_if_last_session_rated(df)
    df = update_last_session_rating(is_last_session_rated, df,productivityResult)
    length = get_length_df(df)
    generate_design_option_one(df, length)
    average_optimal_light_value, average_optimal_humidity_value = compute_optimal_light_and_humidity_value(df)
    return render_template('designoption1.html', is_last_session_rated=is_last_session_rated, average_optimal_light_value=average_optimal_light_value, average_optimal_humidity_value=average_optimal_humidity_value)

# Shows the second design option
@app.route('/design-option-2')
def design_option_2():
    df = read_csv()
    is_last_session_rated = determine_if_last_session_rated(df)
    df = update_last_session_rating(is_last_session_rated, df,productivityResult)
    length = get_length_df(df)
    generate_design_option_two(df, length)
    average_optimal_light_value, average_optimal_humidity_value = compute_optimal_light_and_humidity_value(df)
    return render_template('designoption2.html', is_last_session_rated=is_last_session_rated, average_optimal_light_value=average_optimal_light_value, average_optimal_humidity_value=average_optimal_humidity_value)

# Shows the third design option
@app.route('/design-option-3')
def design_option_3():
    df = read_csv()
    is_last_session_rated = determine_if_last_session_rated(df)
    df = update_last_session_rating(is_last_session_rated, df,productivityResult)
    generate_design_option_three(df)
    average_optimal_light_value, average_optimal_humidity_value = compute_optimal_light_and_humidity_value(df)
    return render_template('designoption3.html', is_last_session_rated=is_last_session_rated, average_optimal_light_value=average_optimal_light_value, average_optimal_humidity_value=average_optimal_humidity_value)
