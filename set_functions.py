class Team:
    """ Holds everything you need to know about each team; the ultimate
            superclass of this program.
    """
    
    def __init__(self, location, mascot, abbreviation, conference, division):
        self.location = location
        self.mascot = mascot
        self.abbreviation = abbreviation
        self.conference = conference
        self.division = division

        self.base = BaseStats(self)
        # ^^ since I defined that this way, this is how I would reference things in this class
        self.set = SetStats(self)
        self.adv = AdvancedStats(self)
        self.rank = RankStats(self)


    def __str__(self):
        return f"The {self.location} {self.mascot} ({self.abbreviation}) play in the {self.conference} {self.division}."
    
    def __repr__(self):
        return f"Team('{self.location}', '{self.mascot}', '{self.abbreviation}', '{self.conference}', '{self.division}')"
    
    def __eq__(self, other):
        if self.location != other.location:
            return False
        if self.mascot != other.mascot:
            return False
        if self.abbreviation != other.abbreviation:
            return False
        if self.conference != other.conference:
            return False
        if self.division != other.division:
            return False
        return True


class StatsSnapshot:
    """ Interface class for storage of basic values.
        Used in BaseStats, and used later for setStats
    """

    def __init__(self):

        self.games_played = 0
        
        self.record = {
            "wins": 0,
            "losses": 0,
            "ties": 0
        }
        self.record_pct = 0.0

        self.total_points = 0
        self.total_opp_points = 0

        self.total_yards = 0
        self.total_opp_yards = 0

        self.total_turnovers_forced = 0
        self.total_opp_turnovers_forced = 0

        self.margin_points = 0.0
        self.margin_yards = 0.0
        self.margin_turnovers_forced = 0.0


class BaseStats:
    """ Basic calculations on input data
        Know this difference (for future reference)!
        - the values are stored in the variables
        - the methods are only called once for ALL teams
        ^^ not fully true actually...
    """
    
    def __init__(self, team):
        self.team = team
        self.games = []

        self.season_stats = None
        
        self.home_stats = None
        self.away_stats = None

        self.win_stats = None
        self.loss_stats = None
        

    @staticmethod
    def collect(team, games):
        """ 'games' = a collection of games used for a particular statistic

            Takes a collection of games and returns a series of basic statistics for them
                in a 'StatsSnapshot.'
            The 'StatsSnapshot' can then be called for later various calculations.
        """

        snapshot = StatsSnapshot() # re-initialize with each use
        for game in games:
            
            home = game["Home Team"]
            home_points = game["Home Team Points"]
            home_yards = game["Home Team Offense Yards"]
            home_turnovers_forced = game["Home Team Turnovers Forced"]

            away = game["Away Team"]
            away_points = game["Away Team Points"]
            away_yards = game["Away Team Offense Yards"]
            away_turnovers_forced = game["Away Team Turnovers Forced"]

            if team.mascot == home:
                # update points
                snapshot.total_points += home_points
                snapshot.total_opp_points += away_points

                # update yards
                snapshot.total_yards += home_yards
                snapshot.total_opp_yards += away_yards

                # update turnovers forced
                snapshot.total_turnovers_forced += home_turnovers_forced
                snapshot.total_opp_turnovers_forced += away_turnovers_forced

                # update record
                if home_points > away_points:
                    snapshot.record["wins"] += 1
                elif home_points < away_points:
                    snapshot.record["losses"] += 1
                elif home_points == away_points:
                    snapshot.record["ties"] += 1

            elif team.mascot == away:
                # update points
                snapshot.total_points += away_points
                snapshot.total_opp_points += home_points

                # update yards
                snapshot.total_yards += away_yards
                snapshot.total_opp_yards += home_yards

                # update turnovers forced
                snapshot.total_turnovers_forced += away_turnovers_forced
                snapshot.total_opp_turnovers_forced += home_turnovers_forced

                # update record
                if away_points > home_points:
                    snapshot.record["wins"] += 1
                elif away_points < home_points:
                    snapshot.record["losses"] += 1
                elif away_points == home_points:
                    snapshot.record["ties"] += 1

            snapshot.games_played += 1

        # get individual pieces of record
        wins = snapshot.record["wins"]
        losses = snapshot.record["losses"]  # not used, but still nice to have
        ties = snapshot.record["ties"]

        try:
            # calculate record %
            snapshot.record_pct = (wins + (ties / 2)) / snapshot.games_played
            snapshot.record_pct = round(snapshot.record_pct, 3)

            # calculate margins
            snapshot.margin_points = (snapshot.total_points - snapshot.total_opp_points) / snapshot.games_played
            snapshot.margin_points = round(snapshot.margin_points, 2)

            snapshot.margin_yards = (snapshot.total_yards - snapshot.total_opp_yards) / snapshot.games_played
            snapshot.margin_yards = round(snapshot.margin_yards, 2)

            snapshot.margin_turnovers_forced = (snapshot.total_turnovers_forced - snapshot.total_opp_turnovers_forced) / snapshot.games_played
            snapshot.margin_turnovers_forced = round(snapshot.margin_turnovers_forced, 2)
        
        except ZeroDivisionError:
            # catch the error for win/loss games if a team has gone undefeated OR lost all games in a season
            snapshot.record_pct = 0.000
            snapshot.margin_points = 0.00
            snapshot.margin_yards = 0.00
            snapshot.margin_turnovers_forced = 0.00

        return snapshot
      

class SetSnapshot: # this is like the StatsSnapshot of earlier, but for SET calcs
    
    def __init__(self):
        
        self.points_scaled = 0.00
        self.yards_scaled = 0.00
        self.turnovers_forced_scaled = 0.00
        self.record_pct_scaled = 0.00

        self.raw_set = 0.00
        self.opp_set = 0.00
        self.true_set = 0.00
    """ right now the formula just equally scales everything, even though not every stat has equal importance
        as a rough draft, i can just add all the scaled stats together (pts, yds, to's, pct)
        however later on i'll adjust for importance
    """


class SetStats:
    """ Algorithmic calculations using base data and base data calculations
    """

    def __init__(self, team):
        self.team = team

        self.season_calc = None

        self.home_calc = None
        self.away_calc = None

        self.win_calc = None
        self.loss_calc = None

        self.raw_set = 0.0
        self.opp_set = 0.0
        self.true_set = 0.0
        self.streak_set = 0.0
        self.home_set = 0.0
        self.away_set = 0.0
        self.win_opp_set = 0.0
        self.loss_opp_set = 0.0
        self.ppo_record = {
            "wins": 0,
            "losses": 0,
            "ties": 0
            }
        self.ppo_record_pct = 0.0
        self.net_rating = 0.0


    # margin_total = margin_points + margin_yards + margin_turnovers_forced
    # record_pct_damper = 0.5
    # self.set = margin_total * (record_pct_damper + self.record_pct)

    @staticmethod
    def populate_scaled_stats(teams, scaled_df, source_snapshot):

        calc_name = source_snapshot.replace("_stats", "_calc")

        for _, row in scaled_df.iterrows():

            team = teams[row["team"]]

            calc = SetSnapshot()

            calc.points_scaled = row["points_scaled"]
            calc.yards_scaled = row["yards_scaled"]
            calc.turnovers_forced_scaled = row["turnovers_forced_scaled"]
            calc.record_pct_scaled = row["record_pct_scaled"]
            
            setattr(team.set, calc_name, calc)

    
    def find_raw_set(teams, target_snapshot):
        for team in teams.values():
            if not hasattr(team.set, target_snapshot):       # catch potential error
                raise AttributeError(
                    f"{team.mascot} does not have 'set' snapshot '{target_snapshot}'"
                )
            calc = getattr(team.set, target_snapshot)

            raw = calc.points_scaled + calc.yards_scaled + calc.turnovers_forced_scaled + calc.record_pct_scaled
            calc.raw_set = raw
        

    def populate_opp_set():
        pass

    def populate_true_set():
        pass


    # SET = Score of Efficiency of Team
    # finds raw, opp, and true set of any set of stats/games
    @staticmethod
    def crunch(team, games):

        calc = SetSnapshot()
        calc.raw_set = 'pass'

        for game in games:
            pass

            
    

    # @staticmethod
    # def find_raw_set(teams):
    #     # need yards
    #     # need turnovers forced
    #     for team in teams.values():

    #         games_played = team.base.games_played
    #         margin_pts = (team.base.total_points - team.base.total_opp_points) / games_played
    #         margin_yards = (team.base.total_yards - team.base.total_opp_yards) / games_played
    #         margin_turnovers_forced = (team.base.total_turnovers_forced - team.base.total_opp_turnovers_forced) / games_played
            

    #         margin_set = (team.base.total_points - team.base.total_opp_points) / team.base.games_played
    #         record_pct_damper = 0.5
    #         raw_set = margin_set * (record_pct_damper + team.base.record_pct)
    #         # record_pct_scaler = 0.75
    #         # raw_set = margin_set * (team.base.record_pct ** record_pct_scaler)
    #         team.set.raw_set = round(raw_set, 3)


    # @staticmethod
    # def find_opp_set(teams, gamelog):

    #     for team in teams.values():
    #         opp_set_tracker = []

    #         for _, game in gamelog.iterrows():

    #             # do I even need points?
    #             home = teams[game["Home Team"]]
    #             home_points = game["Home Team Points"]
    #             away = teams[game["Away Team"]]
    #             away_points = game["Away Team Points"]

    #             if team == home:
    #                 opp_set_tracker.append(teams[away.mascot].set.raw_set) # how to get opp's raw set?

    #             if team == away:
    #                 opp_set_tracker.append(teams[home.mascot].set.raw_set)
            
    #         opp_set = sum(opp_set_tracker) / team.base.games_played # if issue exists in games played, this may be inaccurate
    #         team.set.opp_set = round(opp_set, 3)


    # @staticmethod
    # def find_league_avg_opp_set(teams):
    #     total_opp_set = []

    #     for team in teams.values():
    #         total_opp_set.append(team.set.opp_set)

    #     league_avg_opp_set = sum(total_opp_set) / len(total_opp_set)
    #     return league_avg_opp_set

    
    # @staticmethod
    # def find_true_set(teams, league_avg_opp_set):
    #     for team in teams.values():

    #         opp_adjustment = team.set.opp_set - league_avg_opp_set
    #         opp_set_damper = 0.5    # feasible range of 0.3-0.7
    #         true_set = team.set.raw_set + (opp_set_damper * opp_adjustment)
    #         team.set.true_set = round(true_set, 3)


    # @staticmethod
    # def find_streak_set(teams, gamelog):
    #     """ This entire method is such a grotesque violation of D.R.Y. lol """
    #     # this method produces some crazy numbers in the dozens for some teams
    #     for team in teams.values():
    #         last_games = 0
    #         last_games_total_points = 0
    #         last_games_total_opp_points = 0
    #         last_games_record = {
    #             "wins": 0,
    #             "losses": 0,
    #             "ties": 0
    #             }

    #         # the issue is probably here
    #         for _, game in gamelog[::-1].iterrows():
    #             if last_games >= 5:
    #                 break

    #             home = teams[game["Home Team"]]
    #             home_points = game["Home Team Points"]
    #             away = teams[game["Away Team"]]
    #             away_points = game["Away Team Points"]                

    #             if team == home:
    #                 last_games += 1
    #                 last_games_total_points += home_points
    #                 last_games_total_opp_points += away_points 

    #                 if home_points > away_points:
    #                     last_games_record['wins'] += 1
    #                 elif home_points < away_points:
    #                     last_games_record['losses'] += 1
    #                 elif home_points == away_points:
    #                     last_games_record['ties'] += 1

    #             if team == away:
    #                 last_games += 1
    #                 last_games_total_points += away_points
    #                 last_games_total_opp_points += home_points

    #                 if away_points > home_points:
    #                     last_games_record['wins'] += 1
    #                 elif away_points < home_points:
    #                     last_games_record['losses'] += 1
    #                 elif away_points == home_points:
    #                     last_games_record['ties'] += 1

    #         wins = last_games_record["wins"]
    #         losses = last_games_record["losses"]
    #         ties = last_games_record["ties"]
    #         total = wins + losses + ties

    #         last_games_record_pct = round(((wins + (ties / 2)) / total), 3)
            
    #         last_games_margin_set = (last_games_total_points - last_games_total_opp_points) / 5
    #         last_games_record_pct_damper = 0.5
    #         streak_set = last_games_margin_set * (last_games_record_pct_damper + last_games_record_pct)
    #         # last_games_record_pct_scaler = 0.75
    #         # streak_set = last_games_margin_set * (last_games_record_pct ** last_games_record_pct_scaler)
    #         team.set.streak_set = round(streak_set, 3)


    # @staticmethod
    # def find_home_set(teams, gamelog):
    #     for team in teams.values():
    #         home_games = 0
    #         home_games_total_points = 0
    #         home_games_total_opp_points = 0
    #         home_games_record = {
    #             "wins": 0,
    #             "losses": 0,
    #             "ties": 0
    #             }

    #         for _, game in gamelog[::-1].iterrows():

    #             home = teams[game["Home Team"]]
    #             home_points = game["Home Team Points"]
    #             away = teams[game["Away Team"]]
    #             away_points = game["Away Team Points"]                

    #             if team == home:
    #                 home_games += 1
    #                 home_games_total_points += home_points
    #                 home_games_total_opp_points += away_points 

    #                 if home_points > away_points:
    #                     home_games_record['wins'] += 1
    #                 elif home_points < away_points:
    #                     home_games_record['losses'] += 1
    #                 elif home_points == away_points:
    #                     home_games_record['ties'] += 1

    #         wins = home_games_record["wins"]
    #         losses = home_games_record["losses"]
    #         ties = home_games_record["ties"]
    #         total = wins + losses + ties

    #         home_games_record_pct = round(((wins + (ties / 2)) / total), 3)
            
    #         home_games_margin_set = (home_games_total_points - home_games_total_opp_points) / home_games
    #         home_games_record_pct_damper = 0.5
    #         home_set = home_games_margin_set * (home_games_record_pct_damper + home_games_record_pct)
    #         # last_games_record_pct_scaler = 0.75
    #         # streak_set = last_games_margin_set * (last_games_record_pct ** last_games_record_pct_scaler)
    #         team.set.home_set = round(home_set, 3)


    # @staticmethod
    # def find_away_set(teams, gamelog):
    #     for team in teams.values():
    #         away_games = 0
    #         away_games_total_points = 0
    #         away_games_total_opp_points = 0
    #         away_games_record = {
    #             "wins": 0,
    #             "losses": 0,
    #             "ties": 0
    #             }

    #         for _, game in gamelog[::-1].iterrows():

    #             home = teams[game["Home Team"]]
    #             home_points = game["Home Team Points"]
    #             away = teams[game["Away Team"]]
    #             away_points = game["Away Team Points"]                

    #             if team == away:
    #                 away_games += 1
    #                 away_games_total_points += away_points
    #                 away_games_total_opp_points += home_points 

    #                 if away_points > home_points:
    #                     away_games_record['wins'] += 1
    #                 elif away_points < home_points:
    #                     away_games_record['losses'] += 1
    #                 elif away_points == home_points:
    #                     away_games_record['ties'] += 1

    #         wins = away_games_record["wins"]
    #         losses = away_games_record["losses"]
    #         ties = away_games_record["ties"]
    #         total = wins + losses + ties

    #         away_games_record_pct = round(((wins + (ties / 2)) / total), 3)
            
    #         away_games_margin_set = (away_games_total_points - away_games_total_opp_points) / away_games
    #         away_games_record_pct_damper = 0.5
    #         away_set = away_games_margin_set * (away_games_record_pct_damper + away_games_record_pct)
    #         # last_games_record_pct_scaler = 0.75
    #         # streak_set = last_games_margin_set * (last_games_record_pct ** last_games_record_pct_scaler)
    #         team.set.away_set = round(away_set, 3)


    @staticmethod
    def find_win_opp_set(teams, gamelog):
        for team in teams.values():
            win_opp_set_tracker = []
            games_won = 0

            for _, game in gamelog.iterrows():

                # do I even need points?
                home = teams[game["Home Team"]]
                home_points = game["Home Team Points"]
                away = teams[game["Away Team"]]
                away_points = game["Away Team Points"]

                if team == home and home_points > away_points:
                    win_opp_set_tracker.append(teams[away.mascot].set.raw_set)
                    games_won += 1

                if team == away and away_points > home_points:
                    win_opp_set_tracker.append(teams[home.mascot].set.raw_set)
                    games_won += 1
            
            if games_won == 0:
                pass # what should I do here?
            else:
                win_opp_set = sum(win_opp_set_tracker) / games_won # if issue exists in games played, this may be inaccurate
                team.set.win_opp_set = round(win_opp_set, 3)


    @staticmethod
    def find_loss_opp_set(teams, gamelog):
        for team in teams.values():
            loss_opp_set_tracker = []
            games_lost = 0

            for _, game in gamelog.iterrows():

                # do I even need points?
                home = teams[game["Home Team"]]
                home_points = game["Home Team Points"]
                away = teams[game["Away Team"]]
                away_points = game["Away Team Points"]

                if team == home and home_points < away_points:
                    loss_opp_set_tracker.append(teams[away.mascot].set.raw_set)
                    games_lost += 1

                if team == away and away_points < home_points:
                    loss_opp_set_tracker.append(teams[home.mascot].set.raw_set)
                    games_lost += 1
            
            if games_lost == 0:
                pass # what should I do here?
            else:
                loss_opp_set = sum(loss_opp_set_tracker) / games_lost # if issue exists in games played, this may be inaccurate
                team.set.loss_opp_set = round(loss_opp_set, 3)


    @staticmethod
    def find_playoff_potential_opp_record(teams, gamelog):
        for team in teams.values():

            for _, game in gamelog.iterrows():

                home = teams[game["Home Team"]]
                home_points = game["Home Team Points"]
                away = teams[game["Away Team"]]
                away_points = game["Away Team Points"]

                if team == home:
                    if home_points > away_points and away.set.true_set > 0:
                        team.set.ppo_record['wins'] += 1
                    elif home_points < away_points and away.set.true_set > 0:
                        team.set.ppo_record['losses'] += 1
                    elif home_points == away_points and away.set.true_set > 0:
                        team.set.ppo_record['ties'] += 1

                if team == away:
                    if away_points > home_points and home.set.true_set > 0:
                        team.set.ppo_record['wins'] += 1
                    elif away_points < home_points and home.set.true_set > 0:
                        team.set.ppo_record['losses'] += 1
                    elif away_points == home_points and home.set.true_set > 0:
                        team.set.ppo_record['ties'] += 1


    @staticmethod
    def find_playoff_potential_opp_record_pct(teams):
        for team in teams.values(): # iterating through class objects
            
            ppo_wins = team.set.ppo_record["wins"]
            ppo_losses = team.set.ppo_record["losses"]
            ppo_ties = team.set.ppo_record["ties"]
            ppo_total = ppo_wins + ppo_losses + ppo_ties

            ppo_record_pct = (ppo_wins + (ppo_ties / 2)) / ppo_total
            team.set.ppo_record_pct = round(ppo_record_pct, 3)


    @staticmethod
    def find_net_rating(teams):
        
        weight_true_set = 0.60
        weight_ppo_record_pct = 0.15
        weight_streak_set = 0.15
        weight_opp_set_delta = 0.10

        # weight_true_set = 0.70
        # weight_ppo_record_pct = 0.20
        # weight_streak_set = 0.10

        # TODO -- NORMALIZE EACH COMPONENT BEFORE THIS!!!

        for team in teams.values():
            team.set.net_rating = (
                weight_true_set * team.set.true_set + 
                weight_ppo_record_pct * team.set.ppo_record_pct + 
                weight_streak_set * team.set.streak_set + 
                weight_opp_set_delta * (team.set.win_opp_set - team.set.loss_opp_set)
            )



class AdvancedStats:
    """ For my fellow stat majors
        Works on BaseStats and setStats
    """

    import statistics
    
    def __init__(self, team):
        self.team = team


class RankStats:
    """ Ranks all stats by team
        Works on BaseStats and setStats
    """

    # i could use recursion and .pop() to get this to work
    
    def __init__(self, team):
        self.team = team