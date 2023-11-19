from icecream import ic
import os
import csv
import sqlite3
from scrape import FightDetails, FighterDetails, Index
from helpers import *


################################################################################
# Main loop
################################################################################
# con = sqlite3.connect("ufcql.db")
# cur = con.cursor()

# cur.execute("""
#     CREATE TABLE fights(
#         event_id            TEXT,
#         fight_id            TEXT,
#         fight_order         NUMBER,
#         red_fighter_id      TEXT,
#         blue_fighter_id     TEXT,
#         weightclass         TEXT,
#         time_format         TEXT,
#         title_bout          TEXT,
#         referee             TEXT,
#         FOREIGN KEY (red_fighter_id)  REFERENCES roster(fighter_id),
#         FOREIGN KEY (blue_fighter_id) REFERENCES roster(fighter_id)
#     )
# """)

# for card in fight_details:
#     event_id = get_id(card)
#     for fight in fights(card):
#         fight_id = get_id(fight)
#         fight_order = get_fight_order(fight)
#         data = FightDetails(f'html/fight_details/{card}/{fight}')
#         if data is None:
#             continue

#         values = [
#             event_id,
#             fight_id,
#             fight_order,
#             data['rid'],
#             data['bid'],
#             data['weightclass'],
#             data['time_format'],
#             data['for_title'],
#             data['ref']
#         ]

#         cur.execute("""INSERT INTO fights VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )""", values)

# con.commit()
# cur.close()