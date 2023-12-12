import os
from bs4 import BeautifulSoup

################################################################################
# Sort and order for directories
################################################################################

def sort_function(card):
    return int(card.split('_')[0])

def get_id(name):
    return name.split('.')[0].split('_')[-1]

def get_order(name):
    return sort_function(name)

################################################################################
# Filepaths: 
################################################################################

r_base = 'html/fighter_details'
roster = os.listdir('html/fighter_details/')

ed_base = 'html/event_details'
event_details = sorted(os.listdir(ed_base), key=sort_function)

fd_base = 'html/fight_details'
fight_details = sorted(os.listdir(fd_base), key=sort_function)


# Why the fuck is that a function?
def fights(card): 
    return sorted(os.listdir(f'{fd_base}/{card}'), key=sort_function)


def make_soup(filepath):
    with open(filepath, 'r') as f:
        return BeautifulSoup(f, 'html.parser')