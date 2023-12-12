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

    return None
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

    return None
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

    return None
# update_fight_details() 


def update_fighter_details():
    """Add new fighters to the roser"""
    fd = fight_details[-1]
    for fight in fights(fd):
        with open(f'html/fight_details/{fd}/{fight}', 'r') as htmlf:
            soup = BeautifulSoup(htmlf, 'html.parser')
        
        fighters = soup.find_all(class_='b-fight-details__person-text')
        red, blue = fighters

        r_name = '_'.join(red.a.text.strip().split(' '))
        r_id = red.a['href'].split('/')[-1]

        b_name = '_'.join(blue.a.text.strip().split(' '))
        b_id = blue.a['href'].split('/')[-1]

        rf = r_name + '_' + r_id + '.html'
        bf = b_name + '_' + b_id + '.html'

        with open(f'html/fighter_details/{rf}', 'w') as htmlf:
            res = requests.get(red.a['href'])
            htmlf.write(res.text)

        with open(f'html/fighter_details/{bf}', 'w') as htmlf:
            res = requests.get(blue.a['href'])
            htmlf.write(res.text)
# update_fighter_details()


################################################################################
# Update the sqlite db 
################################################################################

def update_fights():
    event_671 = fight_details[-2]
    event_672 = fight_details[-1]
    con = sqlite3.connect("ufcql.db")
    cur = con.cursor()
    for fight in fights(event_672):
        fd = FightDetails(f'{fd_base}/{event_672}/{fight}')
        data = [
            fd['event_details_id'],
            fd['fight_details_id'],
            fd['fight_order'],
            fd['rid'],
            fd['bid'],
            fd['weightclass'],
            fd['time_format'],
            fd['for_title'],
            fd['ref']
        ]
        cur.execute("""
            insert into fights
            (event_id, fight_id, fight_order, red_fighter_id, blue_fighter_id, weightclass, time_format, title_bout, referee)
            values
            (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)

    con.commit()
    con.close()
# update_fights() 


def update_rounds():
    # event_671 = fight_details[-2]
    # event_672 = fight_details[-1]
    con = sqlite3.connect("ufcql.db")
    cur = con.cursor()
    for fight in fights(event_672):
        fd = FightDetails(f'{fd_base}/{event_672}/{fight}')
        for round in range(int(fd['total_rounds'])):
            red_data = [
                fd['event_details_id'],
                fd['fight_details_id'],
                fd['rid'],
                round + 1,
            ] + fd['red_rbr'][round][1:]
            blue_data = [
                fd['event_details_id'],
                fd['fight_details_id'],
                fd['bid'],
                round + 1,
            ] + fd['blue_rbr'][round][1:]
            cur.execute("""
                insert into rounds
                (
                "event_id", "fight_id", "fighter_id", "round_number",
                "kd",
                "sig_str_landed", "sig_str_att", "sig_str_perc",
                "total_str_landed", "total_str_att",
                "td_landed", "td_att", "td_perc",
                "sub_att", "rev", "ctrl",
                "head_landed", "head_att",
                "body_landed", "body_att",
                "legs_landed", "legs_att",
                "distance_landed", "distance_att",
                "clinch_landed", "clinch_att",
                "ground_landed", "ground_att"
                )
                values
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, red_data)

            cur.execute("""
                insert into rounds
                (
                "event_id", "fight_id", "fighter_id", "round_number",
                "kd",
                "sig_str_landed", "sig_str_att", "sig_str_perc",
                "total_str_landed", "total_str_att",
                "td_landed", "td_att", "td_perc",
                "sub_att", "rev", "ctrl",
                "head_landed", "head_att",
                "body_landed", "body_att",
                "legs_landed", "legs_att",
                "distance_landed", "distance_att",
                "clinch_landed", "clinch_att",
                "ground_landed", "ground_att"
                )
                values
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, blue_data)
    con.commit()
    con.close()
# update_rounds() 


def update_results():
    con = sqlite3.connect("ufcql.db")
    cur = con.cursor()

    # event_671 = fight_details[-2]
    event_672 = fight_details[-1]
    for fight in fights(event_672):
        fd = FightDetails(f'{fd_base}/{event_672}/{fight}')
        data = [
            fd['event_details_id'],
            fd['fight_details_id'],
            fd['r_result'],
            fd['b_result'],
            fd['total_rounds'],
            fd['time'],
            fd['method'],
            fd['details'],
        ]

        cur.execute( """
        insert into results
        (event_id, fight_id, red_result, blue_result, round, time, method, details)
        values
        (?, ?, ?, ?, ?, ?, ?, ?)
        """, data)    

    con.commit()
    con.close()

# update_results()