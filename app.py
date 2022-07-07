import pandas as pd
from flask import Flask, render_template
from sqlalchemy import false

from DV_Option_1.option_1 import generate_design_option_one
from DV_Option_2.option_2 import generate_design_option_two
from DV_Option_3.option_3 import generate_design_option_three

app = Flask(__name__)

IS_LAST_SESSION_RATED = False # Default for now
CSV_FILE_NAME = 'test.csv'

def read_csv():
    df = pd.read_csv(CSV_FILE_NAME, index_col=0)
    return df

def determine_if_last_session_rated(df):
    rating = df['productivity'].iloc[-1]
    if rating == 0:
        return False
    return True

def update_last_session_rating(is_last_session_rated, df, rating):
    if is_last_session_rated:
        return df
    df['productivity'].iloc[-1]= rating
    df.to_csv(CSV_FILE_NAME, index=false)
    return df

def get_length_df(df):
    length = []
    cur = 0
    for x in range(len(df['light'])):
        length.append(cur)
        cur += 1

@app.route('/')
def start():
    df = read_csv()
    is_last_session_rated = determine_if_last_session_rated(df)
    df = update_last_session_rating(is_last_session_rated, df,2)
    return render_template('index.html', is_last_session_rated=is_last_session_rated)

@app.route('/design-option-1')
def design_option_1():
    df = read_csv()
    is_last_session_rated = determine_if_last_session_rated(df)
    df = update_last_session_rating(is_last_session_rated, df,2)
    length = get_length_df(df)
    generate_design_option_one(df, length)
    return render_template('designoption1.html', is_last_session_rated=is_last_session_rated)

@app.route('/design-option-2')
def design_option_2():
    df = read_csv()
    is_last_session_rated = determine_if_last_session_rated(df)
    df = update_last_session_rating(is_last_session_rated, df,2)
    length = get_length_df(df)
    generate_design_option_two(df, length)
    return render_template('designoption2.html', is_last_session_rated=is_last_session_rated)

@app.route('/design-option-3')
def design_option_3():
    df = read_csv()
    is_last_session_rated = determine_if_last_session_rated(df)
    df = update_last_session_rating(is_last_session_rated, df,2)
    generate_design_option_three(df)
    return render_template('index.html', is_last_session_rated=is_last_session_rated)