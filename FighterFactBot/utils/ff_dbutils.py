# db_utils.py
"""Interfaces with the SQL database and transforms fighter stats into sentences. Note - think 
this would work better in two distinct modules: one for SQL interaction, one for transforming 
that data into a human-readable string.."""

import os
import sqlite3
import random
import time

from pprint import pprint

# create a default path to connect to and create (if necessary) a database
# called 'database.sqlite3' in the same directory as this script
DEFAULT_PATH = os.path.join(
    os.path.dirname(__file__), "/home/thinky/FighterFactBot/sql/mmadb.sqlite3"
)


def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con


con = db_connect()  # instantiate sql connection


def get_data(fighter):
    """Takes input string and checks SQL database
    for fighter data. Returns a nested list of stats."""

    cur = con.cursor()
    con.row_factory = (
        sqlite3.Row
    )  # sets output format to be a dict with column names as keys
    cur = con.cursor()
    qry = f"SELECT * FROM raw_fighter_details WHERE UPPER(fighter_name) like UPPER('{fighter}')"
    cur.execute(qry)
    output = cur.fetchall()
    return output


def clean_data(datadict):
    """Cleans data to return a more palatable datadict. SQL default output
    is a deeply nested list and is a bit awkward to work with initially."""
    out = [dict(row) for row in datadict]
    out = out[0]  # removes outer list brackets in order to return dictionary
    return out


def select_rand(datadict):
    """Select a random stat from a fighter's cleaned datadict.
    Note: The datadict stores the fighter's name as an element;
    this function will restart if the random data selection is the fighter's name.
    """
    selection = random.choice(list(datadict.items()))  # selects random key:value pair

    # if value is Null, redo selection
    if not selection[1]:
        selection = select_rand(datadict)
    # if random fact is the fighter's name, redo selection
    if selection[0] == "fighter_name":
        selection = select_rand(datadict)
    return selection  # returns tuple (statname, statvalue)


def factstring(fighter, stat):
    """Take input stat (tuple) and transform into a sentence that the bot can post.
    This function's output will be the message the bot replies with."""
    if stat[0] == "Height":
        output = f"{fighter} stands at {stat[1]} tall."
    elif stat[0] == "Weight":
        output = f"{fighter} fights at a weight of {stat[1]}"
    elif stat[0] == "Reach":
        output = f"{fighter} has a reach of {stat[1]}."
    elif stat[0] == "Stance":
        output = f"{fighter} fights with an {stat[1]} stance."
    elif stat[0] == "DOB":
        output = f"{fighter} was born on {stat[1]}."
    elif stat[0] == "SLpM":
        output = f"{fighter} lands {stat[1]} strikes per minute of fight time."
    elif stat[0] == "Str_Acc":
        output = f"{fighter} boasts a strike accuracy of {stat[1]}."
    elif stat[0] == "SApM":
        output = f"{fighter} absorbs {stat[1]} strikes per minute."
    elif stat[0] == "Str_Def":
        output = f"{fighter} maintains a {stat[1]} striking defense rate."
    elif stat[0] == "TD_Avg":
        output = f"{fighter} averages {stat[1]} takedowns per 15 minutes of fight time."
    elif stat[0] == "TD_Acc":
        output = f"{fighter} completes takedowns at a rate of {stat[1]}."
    elif stat[0] == "TD_Def":
        output = f"{fighter} successfully defends {stat[1]} of takedowns."
    elif stat[0] == "Sub_Avg":
        output = f"{fighter} averages {stat[1]} submission attempts per 15 minutes of fight time."

    return output


# Takes fighter name and returns a random stat in sentence-format.
def fighter_fact(fighter):
    fighter = fighter.title()
    data = get_data(fighter)
    cleaned = clean_data(data)
    randfact = select_rand(cleaned)
    fact_output = factstring(fighter, randfact)
    return fact_output
