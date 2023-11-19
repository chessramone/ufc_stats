from icecream import ic
import os
import sqlite3
from scrape import FightDetails, FighterDetails, Index
import requests
from bs4 import BeautifulSoup
from helpers import *

################################################################################
# Update the html 
################################################################################

def update_index():
    """Request and write the updated index page from ufcstats.com as html/index.html"""
    res = requests.get('http://ufcstats.com/statistics/events/completed?page=all')
    with open('html/index.html', 'w') as htmlf:
        htmlf.write(res.text)
    return
# update_index()


def update_event_details():
    """Write the new event details page to the event_details directory"""
    # get the most recent completed event from html/index.html
    with open('html/index.html', 'r') as index:
        soup = BeautifulSoup(index, 'html.parser')
    new_event = soup.select('tbody tr:nth-of-type(3)')[0].a['href']

    # get the most recent fight card
    order = int(get_order(event_details[-1])) + 1
    eid = new_event.split('/')[-1]

    # request the card from ufcstats.com
    res = requests.get(new_event)

    # write the file
    with open(f'{ed_base}/{order}_{eid}.html', 'w') as htmlf:
        htmlf.write(res.text)
    return
# update_event_details()
    

def update_fight_details():
    """Adds a new directory, and scrapes each fight details page into it"""
    new_dir = event_details[-1].split('.')[0]
    os.mkdir(f'html/fight_details/{new_dir}')

    with open(f'html/event_details/{event_details[-1]}', 'r') as htmlf:
        soup = BeautifulSoup(htmlf, 'html.parser')
    rows = soup.find_all('tr')[1:]
    fight_urls = [tr['data-link'] for tr in rows]
    for order, url in enumerate(fight_urls):
        order += 1
        fid = url.split('/')[-1]
        res = requests.get(url)
        with open(f'html/fight_details/{new_dir}/{order}_{fid}.html', 'w') as htmlf:
            htmlf.write(res.text)
# update_fight_details() 


def update_fighter_details():
    """Add new fighters to the roser"""
    ...




################################################################################
# Update the html 
################################################################################

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