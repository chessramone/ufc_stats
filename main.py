import EventIndex
import requests
from bs4 import BeautifulSoup
import helpers
from icecream import ic

# compare the websites index to the index.html on disk

## request the remote html file:
remote_recent = EventIndex.remote_recent_event()
disk_recent   = EventIndex.scrape_recent_completed_event()

if remote_recent == disk_recent:
    print('The file on disk is the most recent updare to ufcstats.com.')
else:
    print('ufcstats.com is different than the file on disk.')
    print('updating the file.')
    EventIndex.update_index()