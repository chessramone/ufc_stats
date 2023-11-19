from icecream import ic
import os
import sqlite3
from scrape import FightDetails, FighterDetails, Index
import requests

################################################################################
# Update functions
################################################################################

def update_index():
    res = requests.get('http://ufcstats.com/statistics/events/completed?page=all')
    with open('html/index', 'w') as index:
        index.write(res.text)


def update_event_details():
    ...
    

def update_fight_details():
    ...
    

def update_fighter_details():
    ...




### KEEP FOR UPDATE
# con = sqlite3.connect("ufcql.db")
# cur = con.cursor()

# for event in fight_details:
#     for fight in fights(event):
#         eid = event.split('_')[-1]
#         fid = fight.split('_')[-1].split('.')[0]
#         order = fight.split('_')[0]
#         data = FightDetails(f'{fd_base}/{event}/{fight}')
#         if not data: continue

#         for rnd in range(int(data['total_rounds'])):
#             red_row =  [eid, fid, data['rid'], rnd+1] + data['red_rbr'] [rnd][1:]
#             blue_row = [eid, fid, data['bid'], rnd+1] + data['blue_rbr'][rnd][1:]

#             cur.execute(f"""
#             INSERT INTO rounds
#             (
#             "event_id", "fight_id", "fighter_id", "round",
#             "kd",
#             "sig_str_landed", "sig_str_att", "sig_str_perc",
#             "total_str_landed", "total_str_att",
#             "td_landed", "td_att", "td_perc",
#             "sub_att", "rev", "ctrl",
#             "head_landed", "head_att",
#             "body_landed", "body_att",
#             "legs_landed", "legs_att",
#             "distance_landed", "distance_att",
#             "clinch_landed", "clinch_att",
#             "ground_landed", "ground_att"
#             )
#             VALUES
#             (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """, red_row)
            
#             cur.execute(f"""
#             INSERT INTO rounds
#             (
#             "event_id", "fight_id", "fighter_id", "round",
#             "kd",
#             "sig_str_landed", "sig_str_att", "sig_str_perc",
#             "total_str_landed", "total_str_att",
#             "td_landed", "td_att", "td_perc",
#             "sub_att", "rev", "ctrl",
#             "head_landed", "head_att",
#             "body_landed", "body_att",
#             "legs_landed", "legs_att",
#             "distance_landed", "distance_att",
#             "clinch_landed", "clinch_att",
#             "ground_landed", "ground_att"
#             )
#             VALUES
#             (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """, blue_row)

# con.commit()
# con.close()