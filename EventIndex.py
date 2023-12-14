import bs4
import requests
from icecream import ic
from helpers import make_soup


index_path = 'html/index.html'
soup = make_soup(index_path)


# NOTE: this must be run first!
def update_index():
    res = requests.get('http://ufcstats.com/statistics/events/completed?page=all')
    with open('html/index.html', 'w') as htmlf:
        htmlf.write(res.text)


def scrape_upcoming_event_soup() -> bs4.element.Tag:
    event_list = soup.table.css.select('tr:nth-of-type(2)')
    return event_list[0]


def scrape_recent_completed_event_soup() -> bs4.element.Tag:
    recent_event_list = soup.table.css.select('tr:nth-of-type(3)')
    return recent_event_list[0]


def scrape_recent_completed_event_link():
    soup = scrape_recent_completed_event_soup()
    return soup.a['href']


def scrape_all_completed_events_soup() -> list[bs4.element.Tag]:
    completed_events_list = soup.tbody.find_all('tr')
    return completed_events_list[2:]


def scrape_event_id(soup):
    return soup.a['href'].split('/')[-1]


def scrape_event_name(soup):
    return soup.a.text.strip()


def scrape_event_date(soup):
    return soup.span.text.strip()


def scrape_event_location(soup):
    return soup.css.select('td:nth-of-type(2)')[0].text.strip()


def scrape_event_info(soup):
    return {
        'event_id': scrape_event_id(soup),
        'name':     scrape_event_name(soup),
        'date':     scrape_event_date(soup),
        'location': scrape_event_location(soup),
    }


upcoming_event_info         =  scrape_event_info(scrape_upcoming_event_soup())
recent_completed_event_info =  scrape_event_info(scrape_recent_completed_event_soup())
all_completed_event_info    = [scrape_event_info(event) for event in scrape_all_completed_events_soup()]