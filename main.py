from icecream import ic
import os
import csv
import sqlite3
from scrape import FightDetails, FighterDetails, Index

################################################################################
# Helper functions:
################################################################################
def sort_function(card):
    return int(card.split('_')[0])

roster = os.listdir('html/fighter_details/')

ed_base = 'html/event_details'
event_details = sorted(os.listdir(ed_base), key=sort_function)

fd_base = 'html/fight_details'
fight_details = sorted(os.listdir(fd_base), key=sort_function)

r_base = 'html/fighter_details'

def fights(card): 
    return sorted(os.listdir(f'{fd_base}/{card}'), key=sort_function)

    
################################################################################
# Main loop
################################################################################

# fighter_details_id, full_name, nickname, debut_date, dob, country, height, reach, stance, team
# con = sqlite3.connect("ufcql.db")
# cur = con.cursor()
# for fighter in roster:
#     data = FighterDetails(f'{r_base}/{fighter}')
#     params = [ (data['fid']), data['name'], data['nickname'], data['debut'], data['dob'], None, data['height'], data['reach'], data['stance'], None ]
#     cur.execute(f"""
#         INSERT INTO roster 
#         ("fighter_id", "full_name", "nickname", "debut_date", "dob", "country", "height", "reach", "stance", "team")
#         VALUES
#         (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, params)
# con.commit()
# con.close()

# event_details_id, fight_details_id, fighter_details_id, 
# round_number,
# kd, sig_str_landed, sig_str_att, total_str_landed, total_str_att, 
# td_landed, td_att, 
# head_landed ,head_att, body_landed, body_att, legs_landed, legs_att, 
# distance_landed, distance_att, clinch_landed, clinch_att, ground_landed, ground_att, 
# sub_att, rev, ctrl

# con = sqlite3.connect("ufcql.db")
# cur = con.cursor()

# cur.execute("""
#     DELETE FROM rounds
# """)

# cur.execute("""
#     DROP TABLE rounds
# """)

# cur.execute("""
#     CREATE TABLE rounds(
#         event_id TEXT,
#         fight_id TEXT,
#         fighter_id TEXT,
#         round NUMBER,
#         kd NUMBER,
#         sig_str_landed NUMBER,
#         sig_str_att NUMBER,
#         sig_str_perc REAL,
#         total_str_landed NUMBER,
#         total_str_att NUMBER,
#         td_landed NUMBER,
#         td_att NUMBER,
#         td_perc REAL,
#         head_landed NUMBER,
#         head_att NUMBER,
#         body_landed NUMBER,
#         body_att NUMBER,
#         legs_landed NUMBER,
#         legs_att NUMBER,
#         distance_landed NUMBER,
#         distance_att NUMBER,
#         clinch_landed NUMBER,
#         clinch_att NUMBER,
#         ground_landed NUMBER,
#         ground_att NUMBER,
#         sub_att NUMBER,
#         rev NUMBER,
#         ctrl TEXT
#     )
# """)

con = sqlite3.connect("ufcql.db")
cur = con.cursor()

for event in fight_details:
    for fight in fights(event):
        eid = event.split('_')[-1]
        fid = fight.split('_')[-1].split('.')[0]
        order = fight.split('_')[0]
        data = FightDetails(f'{fd_base}/{event}/{fight}')
        if not data: continue

        for rnd in range(int(data['total_rounds'])):
            red_row =  [eid, fid, data['rid'], rnd+1] + data['red_rbr'] [rnd][1:]
            blue_row = [eid, fid, data['bid'], rnd+1] + data['blue_rbr'][rnd][1:]

            # ic(len(red_row))
            # ic(red_row)

            # event_details_id, fight_details_id, fighter_details_id, 
            # round_number,
            # kd, sig_str_landed, sig_str_att, total_str_landed, total_str_att, 
            # td_landed, td_att, 
            # head_landed ,head_att, body_landed, body_att, legs_landed, legs_att, 
            # distance_landed, distance_att, clinch_landed, clinch_att, ground_landed, ground_att, 
            # sub_att, rev, ctrl

            cur.execute(f"""
            INSERT INTO rounds
            (
            "event_id", "fight_id", "fighter_id", "round",
            "kd",
            "sig_str_landed", "sig_str_att", "sig_str_perc",
            "total_str_landed", "total_str_att",
            "td_landed", "td_att", "td_perc",
            "head_landed", "head_att",
            "body_landed", "body_att",
            "legs_landed", "legs_att",
            "distance_landed", "distance_att",
            "clinch_landed", "clinch_att",
            "ground_landed", "ground_att",
            "sub_att", "rev", "ctrl"
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, red_row)
            
            cur.execute(f"""
            INSERT INTO rounds
            (
            "event_id", "fight_id", "fighter_id", "round",
            "kd",
            "sig_str_landed", "sig_str_att", "sig_str_perc",
            "total_str_landed", "total_str_att",
            "td_landed", "td_att", "td_perc",
            "head_landed", "head_att",
            "body_landed", "body_att",
            "legs_landed", "legs_att",
            "distance_landed", "distance_att",
            "clinch_landed", "clinch_att",
            "ground_landed", "ground_att",
            "sub_att", "rev", "ctrl"
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, blue_row)

con.commit()
con.close()
