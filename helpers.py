import os
from bs4 import BeautifulSoup

def sort_function(card):
    return int(card.split('_')[0])

def get_id(name):
    return name.split('.')[0].split('_')[-1]

def get_order(name):
    return sort_function(name)

roster = os.listdir('html/fighter_details/')

ed_base = 'html/event_details'
event_details = sorted(os.listdir(ed_base), key=sort_function)

fd_base = 'html/fight_details'
fight_details = sorted(os.listdir(fd_base), key=sort_function)

r_base = 'html/fighter_details'

def fights(card): 
    return sorted(os.listdir(f'{fd_base}/{card}'), key=sort_function)

def make_soup(filepath):
    with open(filepath, 'r') as f:
        return BeautifulSoup(f, 'html.parser')