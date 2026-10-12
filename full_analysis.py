# import sportsreference.nfl.teams as sref
# KEEP THIS ^^^ just in case

from set_functions import Team
from set_functions import BaseStats as base
from set_functions import SetStats as set
from set_functions import AdvancedStats as adv
from set_functions import RankStats as rank

import pandas as pd # for converting all the data into a DataFrame
import matplotlib.pyplot as plt # for showing plots made with seaborn
import plotly.express as px # for interactive streamlit plots
import streamlit as st # for displaying all my work on a streamlit app thingy
import seaborn as sns # for making plots of statistical data
import math
from sklearn.preprocessing import StandardScaler
# test for things like difference between home and away (if there is a difference)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class InvalidDataError(Exception):
    """ Exception to be raised if input data is in an invalid format.
        This exception will stop the program.
    """
    pass


class UnmatchedNameError(Exception):
    """ Exception to be raised if column names of input data do not match the intended format.
        This exception will not stop the program;
        it will simply notify the user that the column names do not match.
    """
    pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def format_check_template(template, teams):
    """ Compares formatting of 'template' data to what is needed for the program
        to run the rest of the way.
        Performs checks on rows and columns of input data.
    """
    input_col = template.columns
    correct_col = [
        'Location',
        'Mascot',
        'Abbreviation',
        'Conference',
        'Division',
        # 'Net Rating',
        # 'Net Rating Rank',
        # 'Record',
        # 'Record %',
        # 'Overall Points Differential',
        # 'OPD Rank',
        # 'Avg Win Margin',
        # 'AWM Rank',
        # 'Avg Loss Margin',
        # 'ALM Rank',
        # 'Raw set',
        # 'Rset Rank',
        # 'Opp set',
        # 'Oset Rank',
        # 'True set',
        # 'Tset Rank',
        # 'Streak set',
        # 'Sset Rank',
        # 'Home set',
        # 'Hset Rank',
        # 'Away set',
        # 'Aset Rank',
        # 'Win Opp set',
        # 'WOset Rank',
        # 'Loss Opp set',
        # 'LOset Rank',
        # 'Playoff Potential Opp WIN%',
        # 'PPO WIN% Rank'
    ]
      
    if len(input_col) < len(correct_col):
        raise InvalidDataError("Not enough columns in template input data")
    
    if len(input_col) > len(correct_col):
        raise InvalidDataError("Too many columns in template input data")
    
    for i in range(len(input_col)):
        if input_col[i] != correct_col[i]:
            if input_col[i].lower() == correct_col[i].lower():
                raise UnmatchedNameError(f"Column name in template is correct but does not have correct casing: '{correct_col[i]}'")
            else:
                raise UnmatchedNameError(f"Column name in template does not match: '{correct_col[i]}'")

        # if template[input_col[i]].isna().sum() > 0:
            # raise InvalidDataError(f"Missing data found in column: '{input_col[i]}'")
        "^ this is the less intuitive alternative to the code directly below this"
    
    # if (template == '').any().any():
    #     raise InvalidDataError(f"There should be lots of 'NaN' values, but at least one entry has nothing in it all")
    "^ this is only necessary if using 'set-template-full.csv'"

    input_teams = teams # input parameter
    correct_teams = [
        'Bills',
        'Patriots',
        'Jets',
        'Dolphins',
        'Raiders',
        'Chargers',
        'Broncos',
        'Chiefs',
        'Ravens',
        'Bengals',
        'Steelers',
        'Browns',
        'Titans',
        'Colts',
        'Jaguars',
        'Texans',
        'Cowboys',
        'Eagles',
        'Giants',
        'Commanders',
        'Cardinals',
        'Rams',
        '49ers',
        'Seahawks',
        'Packers',
        'Vikings',
        'Bears',
        'Lions',
        'Buccaneers',
        'Saints',
        'Panthers',
        'Falcons'
    ]

    if len(input_teams) < len(correct_teams):
        raise InvalidDataError("Not enough rows in template input data")
    
    if len(input_teams) > len(correct_teams):
        raise InvalidDataError("Too many rows in template input data")
    
    for i in range(len(input_teams)):
        if input_teams[i] != correct_teams[i]:
            if input_teams[i].lower() == correct_teams[i].lower():
                raise UnmatchedNameError(f"Row name in template is correct but does not have correct casing: '{correct_teams[i]}'")
            else:
                raise UnmatchedNameError(f"Row name in template does not match: '{correct_teams[i]}'")


def format_check_gamelog(gamelog):
    """ Compares formatting of 'gamelog' data to what is needed for the program
        to run the rest of the way.
        Performs checks on columns of input data.
        Cannot perform checks on rows, as there may be an unusual but correct number
        of rows in input data (see bottom of this function for more details).
    """
    input_col = gamelog.columns
    correct_col = [
        'Week #',
        'Away Team',
        'Away Team Points',
        'Away Team Offense Yards',
        'Away Team Turnovers Forced',
        'Home Team',
        'Home Team Points',
        'Home Team Offense Yards',
        'Home Team Turnovers Forced'
    ]

    if len(input_col) < len(correct_col):
        raise InvalidDataError("Not enough columns in gamelog input data")
    
    if len(input_col) > len(correct_col):
        raise InvalidDataError("Too many columns in gamelog input data")
    
    for i in range(len(input_col)):
        if input_col[i] != correct_col[i]:
            if input_col[i].lower() == correct_col[i].lower():
                raise UnmatchedNameError(f"Column name in gamelog is correct but does not have correct casing: '{correct_col[i]}'")
            else:
                raise UnmatchedNameError(f"Column name in gamelog does not match: '{correct_col[i]}'")
            
    num_games = len(gamelog.index)

    print(f"The inputted gamelog shows that {num_games} games were played this season.")
    if num_games == 272:
        print(
            f"This number is consistent with an 18-week season.\n"
            f"This schedule change was made starting in the 2021 season.\n"
        )
    elif num_games == 256:
        print(
            f"This number is consistent with a 17-week season.\n"
            f"This schedule was in place before the 2021 season changed it to an 18-week season.\n"
        )
    else:
        print(
            f"This number is not consistent with a 17-/18-week season.\n"
            f"In very rare circumstances, a game may be canceled (e.g. the Damar Hamlin game in 2022) or a season may be shortened by a strike.\n"
            f"Please verify that the data in the inputted gamelog is correct, so as to avoid any errors in the calculations.\n"
        )


def setup(template, gamelog):
    """ Performs necessary checks on all input data.
        Raises exceptions if the data do not match the desired formatting
        in order for the rest of the program to run.
        InvalidDataError will crash the program, whereas UnmatchedNameError
        will be caught if found.

        format_check_template() currently uses 'set-template-minimalized.csv' (no stat/rank columns)
    """
    print("Performing formatting checks on input files ...")
    print()

    try:
        teams = template['Mascot']
        format_check_template(template, teams)
    except UnmatchedNameError as e:
        print(f"{e}:\n"
              "Some of what you see may be misaligned as a result")
    else:
        print("Input template sheet has fully passed formatting check")
        print()

    try:
        format_check_gamelog(gamelog)
    except UnmatchedNameError as e:
        print(f"{e}:\n"
              "Some of what you see may be misaligned as a result")
    else:
        print("Input gamelog sheet has fully passed formatting check")
        print()


def initialize_teams(template):
    """ Creates a dictionary of all teams in the NFL.
        KEY = the mascot name of all teams (this is how I inputted
            the data into the 'gamelog' sheet)
        VALUE = 'Team' class object that stores all info and stats of each team
    """

    teams = {}
    for _, row in template.iterrows(): # for {index}, {row}
        team = Team(
            row['Location'],
            row['Mascot'],
            row['Abbreviation'],
            row['Conference'],
            row['Division']
        )
        teams[row['Mascot']] = team # abbreviations are easier to code with, but gamelog uses mascots
    return teams


def find_team_games(team, gamelog):
    """ 'team' = one specific Team object

        Finds all the games in which the inputted team has played in during the season
            and adds it to the list of games in which that team has played in in the Team object
    """

    for _, game in gamelog.iterrows():
        if team.mascot == game['Home Team'] or team.mascot == game['Away Team']:
            team.base.games.append(game)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def find_base_stats(teams):
    for team in teams.values():
        
        all_games = team.base.games

        win_games = []
        loss_games = []

        home_games = []
        away_games = []

        for game in all_games:
            home = game["Home Team"]
            home_points = game["Home Team Points"]
            away = game["Away Team"]
            away_points = game["Away Team Points"]

            if team.mascot == home:
                home_games.append(game)

                if home_points > away_points:
                    win_games.append(game)
                if home_points < away_points:
                    loss_games.append(game)

            elif team.mascot == away:
                away_games.append(game)

                if away_points > home_points:
                    win_games.append(game)
                if away_points < home_points:
                    loss_games.append(game)

        # do I do 'team.base.collect(games)' or just 'base.collect(games)'?
        team.base.season_stats = base.collect(team, all_games)
        team.base.win_stats = base.collect(team, win_games)
        team.base.loss_stats = base.collect(team, loss_games)
        team.base.home_stats = base.collect(team, home_games)
        team.base.away_stats = base.collect(team, away_games)

        # removed w/l margins for now

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def find_set_stats(teams):

    def snapshot_to_dataframe(teams, snapshot_name):
        snapshot_data = []
        for team in teams.values():
            if not hasattr(team.base, snapshot_name):       # catch potential error
                raise AttributeError(
                    f"{team.mascot} does not have 'base' snapshot '{snapshot_name}'"
                )
            stats = getattr(team.base, snapshot_name)
            snapshot_data.append({
                "team": team.mascot,
                "margin_points": stats.margin_points,
                "margin_yards": stats.margin_yards,
                "margin_turnovers_forced": stats.margin_turnovers_forced,
                "record_pct": stats.record_pct
            })
        return pd.DataFrame(snapshot_data)

    def scale_stats(stats_df):
        scaler = StandardScaler()
        scaled = scaler.fit_transform(
            stats_df[[
                    "margin_points",
                    "margin_yards",
                    "margin_turnovers_forced",
                    "record_pct"
                ]]
        )
        scaled_df = pd.DataFrame(
            scaled,
            columns = [
                "points_scaled",
                "yards_scaled",
                "turnovers_forced_scaled",
                "record_pct_scaled"
            ]
        )
        scaled_df.insert(0, "team", stats_df["team"])
        return scaled_df

    season_df = snapshot_to_dataframe(teams, "season_stats")
    season_scaled = scale_stats(season_df)
    set.populate_scaled_stats(teams, season_scaled, source_snapshot = "season_stats")
    set.find_raw_set(teams, "season_calc")

    home_df = snapshot_to_dataframe(teams, "home_stats")
    home_scaled = scale_stats(home_df)
    set.populate_scaled_stats(teams, home_scaled, source_snapshot = "home_stats")

    away_df = snapshot_to_dataframe(teams, "away_stats")
    away_scaled = scale_stats(away_df)
    set.populate_scaled_stats(teams, away_scaled, source_snapshot = "away_stats")

    win_df = snapshot_to_dataframe(teams, "win_stats")
    win_scaled = scale_stats(win_df)
    set.populate_scaled_stats(teams, win_scaled, source_snapshot = "win_stats")

    loss_df = snapshot_to_dataframe(teams, "loss_stats")
    loss_scaled = scale_stats(loss_df)
    set.populate_scaled_stats(teams, loss_scaled, source_snapshot = "loss_stats")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def find_advanced_stats(teams, gamelog):
    pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def find_ranks(teams, gamelog):
    pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def compile_data(teams, template):
    pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run_streamlit(teams, template):
    pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    # setup and format checks
    template_link = 'https://raw.githubusercontent.com/jackjayleonard/NFL-Season-Statistical-Analysis/refs/heads/main/pwr-template-minimalized.csv'
    gamelog_link = 'https://raw.githubusercontent.com/jackjayleonard/NFL-Season-Statistical-Analysis/refs/heads/main/2025-nfl-basic-game-data.csv'
    template = pd.read_csv(template_link)
    gamelog = pd.read_csv(gamelog_link)
    setup(template, gamelog)
    teams = initialize_teams(template)

    # find all stats
    for team in teams.values():
        find_team_games(team, gamelog)
    find_base_stats(teams)
    find_set_stats(teams)
    find_advanced_stats(teams)
    find_ranks(teams)

    # compile and show results
    compile_data(teams, template)
    run_streamlit(teams, template)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    main()

# if you're trying to replicate this, you'll be using git (useable with vscode)
'''
git clone [code url] (in git terminal)
(on page) 'read me' = what it does, how to run it
'''