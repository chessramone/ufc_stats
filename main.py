import EventIndex
import requests
from bs4 import BeautifulSoup
import helpers
from icecream import ic

# compare the websites index to the index.html on disk

## request the remote html file:
res = requests.get('http://ufcstats.com/statistics/events/completed?page=all')
remote_soup = helpers.make_soup(res.text)

# remote_recent_event = EventIndex.remote_recent_completed_event(remote_soup)

# ic(remote_soup)