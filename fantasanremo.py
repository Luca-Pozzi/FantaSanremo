#! /usr/bin/env python

import csv
import itertools

class Artist:
    def __init__(self, id, name, value, points_tot, points_fin):
        self.id = id
        self.name = name
        self.value = value
        self.points_tot = points_tot
        self.points_fin = points_fin 

    def __str__(self):
        return self.name + '\nValue: ' + str(self.value) + '\nPoints: ' + str(self.points)

class Team:
    def __init__(self, artists, captain):
        assert len(artists) == 5, "A team must have 5 Artists!"
        self.artists = list(artists)
        self.captain_id = captain.id
        self.value = sum([a.value for a in artists])
        self.points = 0
        for a in artists:
            self.points += a.points_tot
            if a.id == self.captain_id:
                self.points += a.points_fin

    def __str__(self):
        s = ''
        BOLD = '\033[1m'
        END = '\033[0m'
        for i, a in enumerate (self.artists):
            if a.id == self.captain_id:
                s += BOLD + a.name + END
            else:
                s += a.name
            if i < 4:
                s += ', '

        return s + '\nValue: ' + str(self.value) + '\nPoints: ' + str(self.points)

if __name__ == "__main__":
    # Create an Artist object for each artist
    artists = []
    with open('data.txt') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for i, row in enumerate(rows):
            if not i:   # skip the first line (i.e. the header)
                continue
            a = Artist(row[0], 
                       row[1], 
                       int(row[2]), 
                       int(row[3]), 
                       int(row[4])
                       )
            artists.append(a)
    # Create a Team object for each possible team
    teams = []
    for artist_set in itertools.combinations(artists, 5):
        # Keep only teams which value is less or equal than 100
        if sum([a.value for a in artist_set]) <= 100:
            # Each set of artist leads to 5 teams (same set, different captain)
            for a in artist_set:
                t = Team(artists=artist_set,
                         captain=a
                         )
                teams.append(t)

    print("Total teams <= 100 baudi: ", len(teams) // 5)
    print("Total teams <= 100 baudi with captain: ", len(teams))
    
    teams.sort(key=lambda x: x.points, reverse=True)
    print("\nTop 10")
    for i in range(10):
        print(teams[i], '\n')
    
    teams.sort(key=lambda x: x.points, reverse=False)
    print("Flop 10")
    for i in range(10):
        print(teams[i], '\n')