import argparse
import re
import csv
import sys



def run(all_entries, names, team, threshold):
    entries = [entry for entry in all_entries if team in entry[1]]


    if len(entries) == 0:
        print "No entries for team %s!" % team
        sys.exit(1)

    r = 1
    eliminated = set()
    runner_up_losers = []
    print "Tabulating votes for %s" % team
    while True:
        indexmap = {}
        votes = 0
        for entry in entries:
            indices = [i for i,x in enumerate(entry) if x.startswith("5") and i not in eliminated and names[i]]
            if len(indices) > 0:
                votes += 1
            for index in indices:
                if index not in indexmap:
                    indexmap[index] = 0
                indexmap[index] += 1. / len(indices)

        print "Result after round %s (%s votes)" % (r, votes)
        winners = []
        loser = -1
        loserscore = 101.
        winner = -1
        winnerscore = 0
        for index in indexmap:
            pc = 100 * indexmap[index] / votes
            if pc <= loserscore:
                loser = index
                loserscore = pc
            if pc > winnerscore:
                winner = index
                winnerscore = pc
            print "{team}:\t{pc:2.2f}%".format(team=names[index], pc=pc)
            if pc > threshold:
                winners.append(index)

        if (winnerscore - loserscore) / winnerscore < 0.22:
            runner_up_losers.append(names[loser])
        if len(winners) == 1:
            print "Found winner: %s" % names[winners[0]]
            return (names[winner], 100 * indexmap[winner] / votes, ",".join(runner_up_losers))
        if len(indexmap) <= 2:
            print "Found winner: %s" % names[winner]
            return (names[winner], winnerscore, ",".join(runner_up_losers))
        elif len(winners) == 2:
            print "Multiple winners, running another round after eliminating %s" % names[loser]
        else:
            print "No winners above threshold, running another round after eliminating %s" % names[loser]
        print (winnerscore - loserscore) / winnerscore
        eliminated.add(loser)
        r += 1
        for entry in entries:
            number = 5
            indices = [i for i,x in enumerate(entry) if x.startswith(str(number)) and i not in eliminated]
            number -= 1
            while len(indices) == 0 and number > 0:
                indices = [i for i,x in enumerate(entry) if x.startswith(str(number)) and i not in eliminated]
                number -= 1

            if len(indices) != 0:
                for index in indices:
                    entry[index] = "5"


parser = argparse.ArgumentParser(description='Calculate results of SIBR name vote.')
parser.add_argument('--file',  type=str,
                    help='The .csv file of votes')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--team', type=str, help='Name of the team (any case-sensitive substring is okay)')
parser.add_argument('--threshold', type=int, default=55, help="Threshold percentage of votes for winning")
group.add_argument('--all', action="store_true", help="Run for all teams")

args = parser.parse_args()

firstrow = []
all_entries = []
all_teams = set()
with open(args.file) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    first = True
    for line in reader:
        if first:
            firstrow = line
            first = False
            continue
        all_entries.append(line)
        all_teams.add(line[1])

reg = re.compile("\\[([A-Z]+)\\]")
names = [reg.search(col).group(1) if reg.search(col) else None for col in firstrow]
if args.all:
    team_results = {}
    for team in all_teams:
        team_results[team] = run(all_entries, names, team, args.threshold)
        print "========================================"

        print "{:<25} {:<5} {} {}".format("Team", "Name", "Final score", "Runner up")
    for team in team_results:
        print "{:<25} {:<6} {:3.2f}%      {}".format(team, team_results[team][0], team_results[team][1], team_results[team][2])
else:
    run(all_entries, names, args.team, args.threshold)
