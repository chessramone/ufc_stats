import bs4
import os
import requests
from icecream import ic
from helpers import make_soup, event_details
import bs4
from EventDetails import get_recent_event_order


index_path = 'html/index.html'
soup  = make_soup(index_path)
event = soup.table.css.select_one('tr:nth-of-type(3)')


# NOTE: this must be run first!
def update_index() -> None:
    '''Write the most recent ufcstats.com index page to disk'''
    res = requests.get('http://ufcstats.com/statistics/events/completed?page=all')
    with open('html/index.html', 'w') as htmlf:
        htmlf.write(res.text)

        
def remote_recent_event_name() -> str:
    '''Return the name of the most recent event on ufcstats.com'''
    res  = requests.get('http://ufcstats.com/statistics/events/completed?page=all')
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    data = soup.css.select_one('tbody tr:nth-of-type(3)')
    return data.a.text.strip()


def scrape_recent_event_id() -> str:
    return event.a['href'].split('/')[-1]


# def scrape_recent_event_order() -> str:
#     return event_details[-1].split('_')[0]


def scrape_recent_event_name() -> str:
    return event.a.text.strip()


def scrape_recent_event_date() -> str:
    return event.span.text.strip()


def scrape_recent_event_location():
    return event.css.select_one('td:nth-of-type(2)').text.strip()


def scrape_recent_fight_data() -> dict:
    return {
        'event_id':         scrape_recent_event_id(), 
        'event_order':      get_recent_event_order(),
        'event_name':       scrape_recent_event_name(), 
        'event_date':       scrape_recent_event_date(), 
        'event_location':   scrape_recent_event_location(),
    }

ic(scrape_recent_fight_data())