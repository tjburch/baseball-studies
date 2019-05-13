# Statcast scraper, player lookup
from pybaseball import playerid_lookup, statcast_pitcher

# Numerical tools
import pandas as pd
import numpy as np

# Python tools
import sys

# Get info from command line
first = sys.argv[1]
last = sys.argv[2]

# Lookup player
player_info = playerid_lookup(last, first)
player_id = player_info["key_mlbam"].iloc[0]  # assume only one line
start_year = int(player_info["mlb_played_first"].iloc[0])
end_year = int(player_info["mlb_played_last"].iloc[0])
# ignore this year
if end_year == 2019:
    end_year = 2018

# Get all the stats
start_date = "{0}-01-01".format(start_year)
end_date = "{0}-12-31".format(end_year)
print("Scraping from {0) to {1}".format(start_date, end_date))
d_all_stats = statcast_pitcher(start_date, end_date, player_id)

# Only grab strikeouts
## TODO: Figure out a better metric for this
d_strikeouts = d_all_stats[d_all_stats["events"] == "strikeout"]
d_sorted_strikeouts = d_strikeouts.sort_values(["at_bat_number", "pitch_number"])

# Separate out useful columns
d_sorted_strikeouts = d_sorted_strikeouts[
    [
        "pitch_type",
        "release_speed",
        "description",
        "zone",
        "p_throws",
        "stand",
        "type",
        "balls",
        "strikes",
        "outs_when_up",
        "inning",
        "release_spin_rate",
        "at_bat_number",
        "pitch_number",
        "pitch_name",
        "home_score",
        "away_score",
        "if_fielding_alignment",
        "of_fielding_alignment",
    ]
]

# Convert these into a dictionary
d_abs = dict(tuple(sorted_id.groupby("at_bat_number")))

# TODO: Convert to a numpy array for loading into keras
