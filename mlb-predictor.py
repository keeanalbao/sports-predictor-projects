''' READING THE DATA '''


import pandas as pd

# reads game data based on user input
team_choice = input("What team do you want to predict for? (Dodgers, Padres, or Angels) ")
if team_choice == "Dodgers" or team_choice == "dodgers":
    data = pd.read_csv('dodgers_data.csv')
if team_choice == "Padres" or team_choice == "padres":
    data = pd.read_csv('padres_data.csv')
if team_choice == "Angels" or team_choice == "angels":
    data = pd.read_csv('angels_data.csv')


''' CREATING THE LISTS & SUMMING THEM '''


# puts different opponent names into a list without duplicates
def get_opponent_names():
    opp_names = []
    for index, row in data.iterrows():
        opp_name = row[4]
        if opp_name not in opp_names:
            opp_names.append(opp_name)
    return opp_names


# puts the W/L differential from each game into a list for each individual opponent
def get_diff_list(data, team):
    rows = data['Opponent'] == team
    return list(data.loc[rows, 'W/L_Differential'])


# performs the get_diff_list function for each opponent and sums each list
def sum_diff(team_name):
    diff_sum = sum(get_diff_list(data, team_name))
    return diff_sum


# puts the runs scored from each game into a list for each individual opponent
def get_runs_list(data, team):
    rows = data['Opponent'] == team
    return list(data.loc[rows, 'R'])


# performs the get_runs_list function for each opponent and sums each list
def sum_runs_scored(team_name):
    runs_sum = sum(get_runs_list(data, team_name))
    return runs_sum


# puts the runs scored against from each game into a list for each individual opponent
def get_runs_against_list(data, team):
    rows = data['Opponent'] == team
    return list(data.loc[rows, 'RA'])


# performs the get_runs_against_list function for each opponent and sums each list
def sum_runs_against(team_name):
    runs_against_sum = sum(get_runs_against_list(data, team_name))
    return runs_against_sum


''' PREDICTING WIN PERCENTAGE, RUNS SCORED, & RUNS AGAINST '''


# calculates win percentage based on a given total difference
def calculate_win_percentage(diff_sum):
    # when sum of differential is positive
    if diff_sum >= 0:
        win_percent = (((diff_sum * 2.7) + 67) / 134) * 100
        if win_percent > 100.0:
            win_percent = 99
    # when sum of differential is negative
    else:
        win_percent = abs((((diff_sum * 2.7) + 67) / 134) * 100)
    return win_percent


# gives the win percentage based on a given opponent
def get_win_percentage_against_opponent(team_name):
    diff_sum = sum_diff(team_name)
    win_percent = calculate_win_percentage(diff_sum)
    return win_percent


# calculates predicted amount of runs based on given total runs
def calculate_runs(runs_sum):
    predicted_runs = runs_sum // len(get_runs_list(data, team))
    return predicted_runs


# gives the runs scored average based on a given opponent
def get_runs_team_scored(team_name):
    runs_sum = sum_runs_scored(team_name)
    predicted_runs = calculate_runs(runs_sum)
    return predicted_runs


# calculates predicted amount of runs against based on given total runs scored against
def calculate_runs_against(runs_against_sum):
    predicted_runs_against = runs_against_sum // len(get_runs_against_list(data, team))
    return predicted_runs_against


# gives the runs scored against average based on a given opponent
def get_runs_opponent_scored(team_name):
    runs_against_sum = sum_runs_against(team_name)
    predicted_runs_against = calculate_runs_against(runs_against_sum)
    return predicted_runs_against


''' VISUAL COMPONENT & USER INPUT '''


# visual component of the program; utilizes user input to predict outcomes
import shutil

columns = shutil.get_terminal_size().columns

print("\nMAJOR LEAGUE BASEBALL GAME PREDICTOR".center(columns))

print("\nThis program predicts the odds (by percentage) that the " + team_choice.capitalize() + " have to beat a given opponent.")

print("\nHere is a list of teams that the " + team_choice.capitalize() + " play/have played this year: " + str(get_opponent_names()) + ".")

print("\nChoose any one of these teams to predict the outcome of the next time the " + team_choice.capitalize() + " play that team.\n")

while True:
    team = input("Enter a team you want to predict the odds against (Case Sensitive): ")
    print("\n")

    if team not in get_opponent_names():
        print("This is not a team that the " + team_choice.capitalize() + " play!\n")
    else:
        print("The chances of the " + team_choice.capitalize() + " beating the " + team + " is " + str(get_win_percentage_against_opponent(team)) + "% given past data results.\n")

        if get_runs_team_scored(team) != get_runs_opponent_scored(team):
            print("The predicted score is: " + str(get_runs_team_scored(team)) + " to " + str(get_runs_opponent_scored(team)))
        else:
            print("It'll be a close game!")

        if get_win_percentage_against_opponent(team) > 50.0:
            print("\nThey will most likely win.")

        elif get_win_percentage_against_opponent(team) == 50.0:
            print("\nThe odds are 50/50.")

        else:
            print("\nThey will most likely lose.")
            
        print('\n')