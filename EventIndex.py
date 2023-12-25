import bs4
import os
import requests
from icecream import ic
from helpers import make_soup
import bs4


index_path = 'html/index.html'
soup = make_soup(index_path)


# NOTE: this must be run first!
def update_index() -> None:
    '''Write the most recent ufcstats.com index page to disk'''
    res = requests.get('http://ufcstats.com/statistics/events/completed?page=all')
    with open('html/index.html', 'w') as htmlf:
        htmlf.write(res.text)

        
def remote_recent_event() -> str:
    '''Return the name of the most recent event on ufcstats.com'''
    res  = requests.get('http://ufcstats.com/statistics/events/completed?page=all')
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    data = soup.css.select_one('tbody tr:nth-of-type(3)')
    return data.a.text.strip()


# def scrape_upcoming_event_soup() -> bs4.element.Tag:
#     event_list = soup.table.css.select('tr:nth-of-type(2)')
#     return event_list[0]


def scrape_recent_completed_event() -> str:
    event = soup.table.css.select_one('tr:nth-of-type(3)')
    return event.a.text.strip()


# def scrape_recent_completed_event_link() -> str:
#     soup = scrape_recent_completed_event_soup()
#     return soup.a['href']

# def remote_recent_completed_event(soup) -> str:
#     event = soup.css.select('tbody tr:nth-of-type(3)')
#     ic(event)
#     # return event.a.text.strip()


# def scrape_all_completed_events_soup() -> list[bs4.element.Tag]:
#     completed_events_list = soup.tbody.find_all('tr')
#     return completed_events_list[2:]


# def scrape_event_id(soup):
#     return soup.a['href'].split('/')[-1]


# def scrape_event_name(soup):
#     return soup.a.text.strip()


# def scrape_event_date(soup):
#     return soup.span.text.strip()


# def scrape_event_location(soup):
#     return soup.css.select('td:nth-of-type(2)')[0].text.strip()


# def scrape_event_info(soup):
#     return {
#         'event_id': scrape_event_id(soup),
#         'name':     scrape_event_name(soup),
#         'date':     scrape_event_date(soup),
#         'location': scrape_event_location(soup),
#     }

# upcoming_event_info         =  scrape_event_info(scrape_upcoming_event_soup())
# recent_completed_event_info =  scrape_event_info(scrape_recent_completed_event_soup())
# all_completed_event_info    = [scrape_event_info(event) for event in scrape_all_completed_events_soup()]