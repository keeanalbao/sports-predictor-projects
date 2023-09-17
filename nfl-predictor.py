''' READING THE DATA '''


import pandas as pd

# reads game data
team_choice = 'chargers'
data = pd.read_csv('chargers_data.csv')


''' CREATING THE LISTS & SUMMING THEM '''


# puts different opponent names into a list without duplicates
def get_opponent_names():
    opp_names = []
    for index, row in data.iterrows():
        opp_name = row[4]
        if opp_name not in opp_names:
            opp_names.append(opp_name)
    return opp_names


# puts the point differential from each game into a list for each individual opponent
def get_diff_list(data, team):
    rows = data['Opponent'] == team
    return list(data.loc[rows, 'PD'])


# performs the get_diff_list function for each opponent and sums each list
def sum_diff(team_name):
    diff_sum = sum(get_diff_list(data, team_name))
    return diff_sum


# puts the points scored from each game into a list for each individual opponent
def get_points_list(data, team):
    rows = data['Opponent'] == team
    return list(data.loc[rows, 'PF'])


# performs the get_points_list function for each opponent and sums each list
def sum_points_scored(team_name):
    points_sum = sum(get_points_list(data, team_name))
    return points_sum


# puts the points scored against from each game into a list for each individual opponent
def get_points_against_list(data, team):
    rows = data['Opponent'] == team
    return list(data.loc[rows, 'PA'])


# performs the get_points_against_list function for each opponent and sums each list
def sum_points_against(team_name):
    points_against_sum = sum(get_points_against_list(data, team_name))
    return points_against_sum


''' PREDICTING WIN PERCENTAGE, POINTS SCORED, & POINTS AGAINST '''


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


# calculates predicted amount of points based on given total points
def calculate_points(points_sum):
    predicted_points = points_sum // len(get_points_list(data, team))
    return predicted_points


# gives the points scored average based on a given opponent
def get_points_team_scored(team_name):
    points_sum = sum_points_scored(team_name)
    predicted_points = calculate_points(points_sum)
    return predicted_points


# calculates predicted amount of points against based on given total points scored against
def calculate_points_against(points_against_sum):
    predicted_points_against = points_against_sum // len(get_points_against_list(data, team))
    return predicted_points_against


# gives the points scored against average based on a given opponent
def get_points_opponent_scored(team_name):
    points_against_sum = sum_points_against(team_name)
    predicted_points_against = calculate_points_against(points_against_sum)
    return predicted_points_against


''' VISUAL COMPONENT & USER INPUT '''


# visual component of the program; utilizes user input to predict outcomes
import shutil

columns = shutil.get_terminal_size().columns

print("\nLOS ANGELES CHARGERS GAME PREDICTOR".center(columns))

print("\nThis program predicts the odds (by percentage) that the " + team_choice.capitalize() + " have to beat a given opponent.")

print("\nHere is a list of teams that the " + team_choice.capitalize() + " play/have played since 2021: " + str(get_opponent_names()) + ".")

print("\nChoose any one of these teams to predict the outcome of the next time the " + team_choice.capitalize() + " play that team.\n")

while True:
    team = input("Enter a team you want to predict the odds against (Case Sensitive): ")
    print("\n")

    if team not in get_opponent_names():
        print("This is not a team that the " + team_choice.capitalize() + " play/have played!\n")
    else:
        print("The chances of the " + team_choice.capitalize() + " beating the " + team + " is " + str(get_win_percentage_against_opponent(team)) + "% given past data results.\n")

        if get_points_team_scored(team) != get_points_opponent_scored(team):
            print("The predicted score is: " + str(get_points_team_scored(team)) + " to " + str(get_points_opponent_scored(team)))
        else:
            print("It'll be a close game!")

        if get_win_percentage_against_opponent(team) > 50.0:
            print("\nThey will most likely win.")

        elif get_win_percentage_against_opponent(team) == 50.0:
            print("\nThe odds are 50/50.")

        else:
            print("\nThey will most likely lose.")
            
        print('\n')