import EventIndex
import requests
from bs4 import BeautifulSoup
import helpers
from icecream import ic
import sys


################################################################################
# request the remote html index, and compare the event names
################################################################################
remote_recent = EventIndex.remote_recent_event_name()
disk_recent   = EventIndex.scrape_recent_event_name()

if remote_recent == disk_recent:
    sys.exit('the most recent completed events are the same, exiting the program.')


################################################################################
# Update all the html files:
################################################################################
print('ufcstats.com is different than the file on disk.')
print('updating the file.')

EventIndex.update_index()
# Update the html/event_details/...
# Update the html/fight_details/...
# Update the html/fighter_details/...


################################################################################
# Scrape the new html files for the appropriate data
################################################################################
# event_id, event_order, event_name, event_date, event_location
data = EventIndex.scrape_recent_fight_data()
EventIndex.db_insert_recent_event(data)

# TODO: update the roster table NOTE: use insert or ignore
# TODO: update the fights table
# TODO: update the rounds table
# TODO: update the results table
