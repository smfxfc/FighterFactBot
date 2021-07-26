# FighterFactBot
Reddit bot to deliver MMA fighter stats when called by a user. 

Any user on /r/ufc or /r/mma can call the bot by commenting in the format "FighterFact firstname lastname". A few examples below:

    FighterFact Khabib Nurmagomedov

    FighterFact Chael Sonnen

    FighterFact Calvin Kattar

The bot monitors a live stream of comments made to /r/ufc and /r/mma. The bot triggers when it identifies "FighterFact" in a comment's body. It then parses the fighter's name and looks up their stats, which are stored in an SQL database. Then, one of the fighter's statistics is chosen at random and transformed into a readable sentence. The bot will reply to the triggering comment with this sentence (or an error message, if necessary).

Inspiration for this project came from Jason Chanku's UFC fight predictor web app (https://github.com/jasonchanhku/UFC-MMA-Predictor).

The program's SQL database uses stats from a publicly available Kaggle dataset (https://www.kaggle.com/mdabbert/ultimate-ufc-dataset/code)

Links to UFC and MMA subreddits:
https://www.reddit.com/r/ufc/
https://www.reddit.com/r/mma/

Link to FighterFactBot Reddit account:
https://www.reddit.com/u/FighterFactBot
