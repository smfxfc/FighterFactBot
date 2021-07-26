#! python3

import json
import praw
import time
from datetime import datetime
from pprint import pprint

from credentials import config
from . import find_trigger, ff_dbutils

sr = "ufc+mma"


def bot_login():
    # creates a Reddit instance
    r = praw.Reddit(
        username=config.username,
        password=config.password,
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent="FighterFactBot v0.1",
    )
    return r


r = bot_login()


def stream_comments():
    """The main function of the program. Yields new comments as they are made and monitors for the "FighterFact"
    bot trigger substring. If a comment triggers the bot, it parses the fighter name and attempts to retrieve
    their stats from the SQL database. Last, the bot replies to the comment, either with a random fact (in a
    successful case) or an error message."""

    subreddit = r.subreddit(sr)

    start = 1
    for comment in subreddit.stream.comments(skip_existing=True):
        print(f"Comment #{start}.")

        # if comment triggers bot, extract the fighter's name
        if find_trigger.detect_trigger(comment.body):
            fighter = find_trigger.get_fighter(comment.body)
            print(f"BOT ALERT: {fighter}")

            # check SQL db for fighter stats. If any errors occur, reply with error message
            try:
                fact_output = ff_dbutils.fighter_fact(fighter)
                comment.reply(fact_output)  # replies to comment on reddit
                print("BOT REPLIED - SUCCESS\n")
            except:
                error_msg = (
                    f"Oh no! I couldn't pull data on {fighter}. Sorry about that."
                )
                comment.reply(error_msg)
            print("BOT REPLIED - ERROR\n")

        else:
            print("Non-triggering comment processed...\n")

        start += 1
