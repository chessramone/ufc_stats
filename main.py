from icecream import ic
import os
import csv
import sqlite3
from scrape import FightDetails, FighterDetails, Index

################################################################################
# Helper functions:
################################################################################
def sort_function(card):
    return int(card.split('_')[0])

roster = os.listdir('html/fighter_details/')

ed_base = 'html/event_details'
event_details = sorted(os.listdir(ed_base), key=sort_function)

fd_base = 'html/fight_details'
fight_details = sorted(os.listdir(fd_base), key=sort_function)

r_base = 'html/fighter_details'

def fights(card): 
    return sorted(os.listdir(f'{fd_base}/{card}'), key=sort_function)

    
################################################################################
# Main loop
################################################################################
