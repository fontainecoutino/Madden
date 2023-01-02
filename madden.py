#! /usr/bin/python3

import json
import sys
import random

# control
def main():
    com = input('What would you like to do?\n(season, random, update, recap)\n')
    
    if (com == 'season' or com == 's'):
        season()
    elif (com == 'random'):
        random_teams()
    elif (com == 'update' or com == 'u'):
        update_wins()
    elif (com == 'recap'):
        recap()
    else:
        print('Try again dummy!')


# continues season games. looks which teams havent been used
# and picks a game random. updates info file when. lastly
# it asks for which team won to update that stat
def season():
    # open files
    info = json.load(open('info.json'))
    nfl = json.load(open('nfl.json'))

    # gets valid teams
    valid = []
    played = info['fontainePlayed'] + info['isaiahPlayed']
    for team in nfl:
        if (team['name'] not in played):
            valid.append(team['name'])
    
    # check if season ended
    if (len(valid) == 0):
        update_wins()
        store_season(info)
        return
    
    # gets two random teams
    team_1, team_2 = get_two_random(valid)
    
    # print board
    print_board(team_1, team_2)
    
    # update file
    info['fontainePlayed'].append(team_1)
    info['isaiahPlayed'].append(team_2)
    info['matchups'].append(team_1 + '-' + team_2)
    
    f = open('info.json', 'w')
    json.dump(info, f)
    f.close()

# returns two random team from list
def get_two_random(teams):
    random_1 = random.randrange(len(teams))
    random_2 = random.randrange(len(teams))
    while random_1 == random_2:
        random_2 = random.randrange(len(teams))
        
    return teams[random_1], teams[random_2]

# stores season in season folder
def store_season(info):
    # nice message
    print('\nNice you completed a season. I\'m going to store it in /seasons\n')
    
    # create new file and store
    file_name = 'seasons/season' + info['season'] + '.json'
    f = open(file_name, 'w')
    json.dump(info, f)
    f.close()
    
    # empty out info
    for data in info:
        if data == 'season':
            info['season'] = str( int(info['season'])+1 )
        else:
            info[data] = []
    
    f = open('info.json', 'w')
    json.dump(info, f)
    f.close()

# prints game board
def print_board(team_1, team_2):
    print('\n-----------------------')
    print('  ' + team_1 + ' vs ' + team_2)
    print('')
    print('  Fontaine: ' + team_1)
    print('  Isaiah:   ' + team_2)
    print('-----------------------\n')

# gets two random teams to create matchup
def random_teams():
    # open file
    nfl = json.load(open('nfl.json'))

    # gets teams
    teams = []
    for team in nfl:
        teams.append(team['name'])
    
    # gets two random teams
    team_1, team_2 = get_two_random(teams)
    
    # print board
    print_board(team_1, team_2)

# looks at previous season and gives summary
def recap():
    # open file
    season = input('Which season would you like to see?\n')
    try:
        info = json.load(open('seasons/season' + season + '.json'))
    except FileNotFoundError:
        print('No data on that season yet')
        return
    
    nfl = json.load(open('nfl.json'))
    
    # summary
    print('\n-----------------------\n')
    
    # overall record
    print('  -- Overall record -- ')
    print('  Fontaine: ' + str(len(info['fontaineWon'])) + ' wins')
    print('  Isaiah:   ' + str(len(info['isaiahWon'])) + ' wins')
    print('\n')
    
    # individual teams
    print('  -- Individual -- ')
    print('  Fontaine won with these teams: ')
    for team in info['fontaineWon']:
        print('    - ' + team)
    print('')
    print('  Isaiah won with these teams: ')
    for team in info['isaiahWon']:
        print('    - ' + team)
    print('\n')
    
    # NFC vs AFC
    nfc = 0
    afc = 0
    for team in nfl:
        if team['name'] in (info['fontaineWon'] + info['isaiahWon']):
            conf = team['conf']
            if conf == 'NFC':
                nfc += 1
            elif conf == 'AFC':
                afc += 1
    
    print('  -- Conference record -- ')
    print('  NFC: ' + str(nfc) + ' wins')
    print('  AFC: ' + str(afc) + ' wins')
    
    if nfc > afc:
        print('  BRO AFC WEAK AF!')
    else:
        print('  This does not mean anything')
    
    print('\n-----------------------\n')
    
# updates games that have been played with no result
def update_wins():
    info = json.load(open('info.json'))
    
    # get teams with no result
    to_update = []
    for matchup in info['matchups']:
        matchup_split = matchup.split('-')
        games_won = info['fontaineWon'] + info['isaiahWon']
        if ((matchup_split[0] not in games_won) and (matchup_split[1] not in games_won)):
            to_update.append(matchup)
    
    # asks for update
    for matchup in to_update:
        fontaine_team = matchup.split('-')[0]
        isaiah_team = matchup.split('-')[1]
        print('\nWho won the ' + matchup + ' game?')
        print('Fontaine with ' + fontaine_team + ' or Isaiah with ' + isaiah_team)
        won = input()
        if (won.lower() == 'fontaine' or won.lower() == fontaine_team.lower()):
            info['fontaineWon'].append(fontaine_team)
            print('Added')
        elif (won.lower() == 'isaiah' or won.lower() == isaiah_team.lower()):
            info['isaiahWon'].append(isaiah_team)
            print('Added')
        else:
            print('Umm you messed up the name. I\'m not adding that')

    print('\nDone')
    
    # update json
    f = open('info.json', 'w')
    json.dump(info, f)
    f.close()

main() # main main-
