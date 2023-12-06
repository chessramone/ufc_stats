import os
from icecream import ic
from bs4 import BeautifulSoup
import re
import pandas as pd
from helpers import *

################################################################################
# Fighter Details Page
# 
# scrapes the fighter details pages:
# html/fighter_details/FILENAME
################################################################################

def FighterDetails(filepath):
    soup = make_soup(filepath)

    fid =  filepath.split('_')[-1].split('.')[0]
    name = soup.find('span', class_='b-content__title-highlight').text.strip()
    nickname = soup.find('p', class_='b-content__Nickname').text.strip()
    if not nickname: nickname = None

    _box_list_items = soup.ul.find_all('li')
    [li.i.extract() for li in _box_list_items]
    _box_list_items = [li.text.strip() for li in _box_list_items]

    height, weight, reach, stance, dob = _box_list_items
    if height != '--':
        height = height.split('\'')
        feet, inches = height
        height = (int(feet) * 12) + int(inches.replace('"', '').strip())
    else:
        height = None

    if reach != '--': reach = int(reach.replace('"', '').strip())
    else: reach = None

    if weight != '--': weight = int(weight.replace('lbs.', '').strip())
    else: weight = None

    if stance == '--': stance = None
    if not stance: stance = None
    if dob == '--': dob = None

    debut = soup.tbody.find_all('tr')[-1].find_all('td')[-4].find_all('p')[-1].text.strip()

    # return
    return {
        'fid': fid,
        'name': name,
        'nickname': nickname,
        'height': height,
        'weight': weight,
        'reach': reach,
        'stance': stance,
        'dob': dob,
        'debut': debut,
    }
    
# x = FighterDetails(f'{r_base}/Dusko_Todorovic_866fd7b1a6c90e7f.html')
# ic(x)

################################################################################
# Fight Details Page
# 
# scrapes the fighter details pages, does not update
# html/fight_details/DIRNAME/FILENAME
################################################################################

def FightDetails(filename):
    # soup = make_soup(filename)
    with open(filename, 'r') as htmlf:
        soup = BeautifulSoup(htmlf, 'html.parser')
    ic(soup)

    # Not all fights have data:
    if not soup.table:
        return None

    # Get the event_details_id, and fight_details_id
    edid = filename.split('/')[-2].split('_')[-1]
    fdid = filename.split('/')[-1].split('_')[-1]
    
    # Get the fighters names, ids, and results:
    fighters = soup.find_all('a', class_='b-link b-fight-details__person-link')
    r_name, b_name = [a.text.strip() for a in fighters]
    rid, bid = [a['href'].split('/')[-1] for a in fighters]
    results = soup.find_all('i', class_='b-fight-details__person-status')
    r_res, b_res = [i.text.strip() for i in results]
    
    # ufcstats.com divides the stats into 2 tables:
    # t1 is called 'totals'
    # t2 is called 'significant strikes'
    _, t1, _, t2 = soup.find_all('table')
    for tbl in [t1, t2]:
        [thead.extract() for thead in tbl.find_all('thead')]

    # Get each row of the tables, those are the rounds:
    rds1 = t1.find_all('tr')
    rds2 = t2.find_all('tr')

    # Each round is a list of cols (td):
    rbr1 = [rnd.find_all('td') for rnd in rds1]
    rbr2 = [rnd.find_all('td') for rnd in rds2]

    # rd and bd are list[list[str]]
    # each inner list is the round data for the corresponding round
    rd = []
    bd = []
    # for each col, get the text, place it in a list, add it to the correct rd/bd list
    # this is for the table called 'totals' on ufcstats.com
    for rnd in rbr1:
        red_data = []
        blue_data = []
        for td in rnd:
            r = td.css.select('p:first-of-type')[0].text.strip().split(' of ')
            b = td.css.select('p:last-of-type')[0].text.strip().split(' of ')

            if '%' in r[0]: r[0] = float(r[0].replace('%', ''))/100
            if '%' in b[0]: b[0] = float(b[0].replace('%', ''))/100

            if r[0] == '--': r[0] = None
            if b[0] == '--': b[0] = None

            red_data += r
            blue_data += b
            
        rd.append(red_data)
        bd.append(blue_data)

    # for each col we've not already collects, add it to the rd/bd lists
    # this is for the table called 'significant strikes' on ufcstats.com
    for rn, rnd in enumerate(rbr2):
        red_data = []
        blue_data = []

        for idx, td in enumerate(rnd):
            if idx < 3:
                continue
            r = td.css.select('p:first-of-type')[0].text.strip().split(' of ')
            b = td.css.select('p:last-of-type')[0].text.strip().split(' of ')

            red_data += r
            blue_data += b
        rd[rn] += red_data
        bd[rn] += blue_data
    
    # for index, rnd in enumerate(rd):
    #     rd[idx] = [float(data.replace('%', ''))/100 if '%' in data else data for data in rd]
    #     bd[idx] = [float(data.replace('%', ''))/100 if '%' in data else data for data in bd]

    # we now have all the round data!
    # ic(rd, bd)

    # Now we want to do the box data at the top of the page
    # see an event on ufcstats.com for reference
    weight_imgs = soup.find('i', class_='b-fight-details__fight-title')
    imgs = weight_imgs.find_all('img')
    imgs = [img['src'].split('/')[-1].split('.')[0] for img in imgs]

    bonuses = list(filter(lambda s: s != 'belt', imgs))

    weight = weight_imgs.text.strip().lower()
    title = 'false'
    if 'title' in weight:
        title = 'true'
    if 'interim' in weight:
        title = 'iterim'
    weight = re.sub("ufc|interim|title|bout|women's", '', weight).strip()

    box_data, details = soup.find_all('p', class_='b-fight-details__text')
    box_data = box_data.find_all('i', recursive=False)
    [i.i.extract() for i in box_data]
    box_data = [i.text.strip() for i in box_data]
    method, rnd, time, time_format, ref = box_data

    details = details.text.strip().replace('\n', '')
    details = re.sub('\s{2,}', ' ', details)
    details = details.replace('Details: ', '')

    # Got it!
    # Now return EVERYTHING!

    # return None
    return {
        'event_details_id': edid,
        'fight_details_id': fdid,
        'bid': bid,
        'rid': rid,
        'b_name': b_name,
        'r_name': r_name,
        'b_result': b_res,
        'r_result': r_res,
        'weightclass': weight,
        'for_title': title,
        'method': method,
        'round': rnd,
        'total_rounds': rnd,
        'time': time,
        'time_format': time_format,
        'ref': ref,
        'details': details,
        'blue_rbr': bd,
        'red_rbr': rd,
        'bonuses': bonuses,
    } 

# test = FightDetails('html/fight_details/670_5a558ba1ff5e9121/13_b1f2ec122beda7a5.html')
# ic(test)

################################################################################
# Index Page
# 
# scrapes the index page
################################################################################
def Index():
    soup = make_soup('html/index.html')
    rows = soup.tbody.find_all('tr')[2:]
    tds = [tr.find_all('td') for tr in rows]

    events = []
    for td in tds[::-1]:
        # ic(td)
        eid = td[0].a['href'].split('/')[-1]
        name = td[0].a.text.strip()
        date = td[0].span.text.strip()
        location = td[1].text.strip()
        events.append([eid, name, date, location])

    return events

# ic(Index())