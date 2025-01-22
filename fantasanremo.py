import os
import csv
import itertools

import numpy as np
import matplotlib.pyplot as plt

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
    
def format_md(string):
    # Include bold text in `**` for bold formatting in Markdown. 
    BOLD = '\033[1m'
    END = '\033[0m'
    md_string = string.replace(BOLD, '**').replace(END, '**')
    # Change the "in-string" line-breaks (i.e. `\n`) to `\n<br>`. 
    # This allows line breaks in lists.
    md_string = md_string.replace('\n', '\n<br>').rstrip('<br>') + '\n'
    return md_string

if __name__ == "__main__":
    # Create an Artist object for each artist
    artists = []
    root = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(root, 'data', '2024post.txt')) as csvfile:
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

    # Create a plot with the distribution of the team scores
    points = [t.points for t in teams]
    fig, ax = plt.subplots()
    fig.set_size_inches(6*16/9, 6) # 16:9 aspect ratio
    color = 'grey'  # color to use for axis spines and text
                    # NOTE. It should be visible also against dark background.
    # Set axis, ticks, and labels color.
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(color)
    ax.spines['bottom'].set_linewidth(3)
    ax.spines['left'].set_color(color)
    ax.spines['left'].set_linewidth(3)
    ax.xaxis.label.set_color(color)
    ax.yaxis.label.set_color(color)
    ax.tick_params(colors=color, which='both')
    ax.grid(linestyle=':')
    # Create an histogram to display the distribution of scores
    counts, bins = np.histogram(points, 
                                max(points) - min(points) # bins
                                )
    ax.bar(bins[:-1], counts)
    ax.set_xlabel('Points', color = color)
    ax.set_ylabel('N° of teams', color = color)
    # Draw relevant quantiles over the bar plot
    ymax_ax = ax.get_ylim()[-1]     # get upper limit of the Y-axis
    inv = ax.transData.inverted()   # transform from image to data coordinates
    for q in [1, 10, 50, 90, 99]:
        # Write a textbox to display quantile data
        quantile = np.quantile(points, q/100)
        if q < 50:
            txt = "Flop {}%\n{}".format(q, quantile)
        else:
            txt = "Top {}%\n{}".format(100-q, quantile)
        txt_obj = ax.text(quantile, ymax_ax, txt,
            horizontalalignment='center',
            verticalalignment='top',
            color=color
            )
        # Draw a vertical line corresponding to the quantile value
        xmin_txt, ymin_txt = txt_obj.get_window_extent().get_points()[0, :]
        # Transform coordinates from image to data coordinates
        xmin_txt, ymin_txt = inv.transform((xmin_txt, ymin_txt))
        plt.axvline(quantile, 
                    ymax=ymin_txt/ymax_ax # transform from data to axes coord
                    )
    #plt.show() # uncomment for debugging
    plt.savefig(os.path.join(root, 'plot', '2024points_distribution.png'),
                transparent = True
                )
    
    # Write summary to a Markdown file
    with open('FANTASANREPORT2024.md', 'w+') as f:
        # Write the intro
        f.write("# FantaSanReport 2024\n")
        f.write("## General Stats\n")
        f.write("* Total teams <= 100 baudi: {}\n".format(len(teams) // 5))
        f.write("* Total teams <= 100 baudi with captain: {}\n\n".format(len(teams)))

        # Write the top 10 teams
        teams.sort(key=lambda x: x.points, reverse=True)
        f.write("## Top 10 teams\n")
        for i in range(10):
            f.write(format_md("{}. {}\n".format(i+1, teams[i])))
        
        # Write the flop 10 teams
        teams.sort(key=lambda x: x.points, reverse=False)
        f.write("## Flop 10 teams\n")
        for i in range(10):
            f.write(format_md("{}. {}\n".format(i+1, teams[i])))
        
        # Add score distribution image to Markdown file
        f.write("## Score distribution\n")
        f.write("![Score distribution histogram]" +
                "(./plot/2024points_distribution.png)")