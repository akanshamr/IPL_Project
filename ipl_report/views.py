import pandas as pd
from django.shortcuts import render

deliveries = pd.read_csv('csv_files/deliveries.csv')
matches = pd.read_csv('csv_files/matches.csv')


def analyse(season):
    season_matches = matches.loc[matches['season'] == season]
    top_teams = list(season_matches.assign(
        win_count=season_matches.apply(
            lambda x: season_matches.winner.value_counts().to_dict()[x.team1], axis=1
        ))[['team1', 'win_count']].drop_duplicates().sort_values(
        'win_count', ascending=False)[:4]['team1'])
    toss_winner = list(season_matches.assign(
        toss_count=season_matches.apply(
            lambda x: season_matches.toss_winner.value_counts().to_dict()[x.team1], axis=1
        ))[['team1', 'toss_count']].drop_duplicates().sort_values(
        'toss_count', ascending=False)[:1]['team1'])
    player_of_match = list(season_matches.assign(
        player_of_match_count=season_matches.apply(
            lambda x: season_matches.player_of_match.value_counts().to_dict()[x.player_of_match], axis=1
        ))[['player_of_match', 'player_of_match_count']].drop_duplicates().sort_values(
        'player_of_match_count', ascending=False)[:1]['player_of_match'])
    top_team_list = season_matches[season_matches['winner'] == top_teams[0]]

    max_win_location = list(top_team_list.assign(
        venue_win_count=top_team_list.apply(
            lambda x: top_team_list.venue.value_counts().to_dict()[x.venue], axis=1
        ))[['venue', 'venue_win_count']].drop_duplicates().sort_values(
        'venue_win_count', ascending=False)[:1]['venue'])

    choose_to_bat_first = season_matches.loc[season_matches['toss_decision'] == 'bat']

    percent_of_team_decided_to_bat = len(choose_to_bat_first.index) / len(season_matches.index) * 100

    highest_margin_run_team = choose_to_bat_first.loc[choose_to_bat_first['win_by_runs'].idxmax()]['winner']

    team_won_by_highest_wickets = season_matches.loc[season_matches['win_by_wickets'].idxmax()]['winner']

    seasons = matches['season'].drop_duplicates()
    return {
        'top_teams': top_teams,
        'toss_winner': toss_winner[0],
        'player_of_match': player_of_match[0],
        'max_won_team': top_teams[0],
        'max_win_location': max_win_location[0],
        'percent_of_team_decided_to_bat': percent_of_team_decided_to_bat,
        'highest_margin_run_team': highest_margin_run_team,
        'team_won_by_highest_wickets': team_won_by_highest_wickets,
        'seasons': seasons
    }


def report(request):
    season = request.GET.get('season', '2017')
    context = analyse(int(season))
    context['season'] = season
    return render(request, template_name='report.html', context=context, )
