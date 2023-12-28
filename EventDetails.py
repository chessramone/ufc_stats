import bs4
import requests
import os
from icecream import ic
from helpers import make_soup, sort_function, get_id, get_order
from EventIndex import scrape_recent_completed_event_link


event_details_dir   = 'html/event_details'
event_details_list  = sorted(os.listdir(event_details_dir), key=sort_function)


def get_recent_event_order() -> int:
   return get_order(event_details_list[-1])


def get_recent_event_id_from_link(link) -> str:
    return link.split('/')[-1]


def scrape_new_event_details() -> None:
    event_link  = scrape_recent_completed_event_link()
    order       = get_recent_event_order() + 1
    event_id    = get_recent_event_id_from_link(event_link)
    with open(f'{event_details_dir}/{order}_{event_id}.html', 'w') as htmlf:
        res = requests.get(event_link)
        htmlf.write(res.text)


def scrape_fight_card_table(file) -> bs4.element.Tag | None:
    soup = make_soup(file)
    return soup.table


def scrape_fight_card_tbody(elementTag) -> bs4.element.Tag:
    return elementTag.tbody


def scrape_fight_card_tr_elements(elementTag) -> list:
    return elementTag.find_all('tr')


def scrape_fight_card_td_elements(elementTag) -> list:
    return elementTag.find_all('td')


def scrape_fight_card_p_elements(elementTag) -> list:
    return elementTag.find_all('p')


def scrape_fight_card_fighter_link(elementTag) -> str:
    return elementTag.a['href']