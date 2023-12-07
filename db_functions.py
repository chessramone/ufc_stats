import sqlite3

def db_connect():
    '''Opens a connection to ufcql.db'''
    con = sqlite3.connect("ufcql.db")
    cur = con.cursor()
    return (con, cur)


def db_commit_and_close(con):
    '''commits changes and closes an open sqlite connection'''
    con.commit()
    con.close()

    
def db_update_events(cur, event):
    '''Adds the most recent event to the events table of ufcql.db'''
    ...
    

def db_update_roster(cur, data: list[list]):
    '''
    Adds new fighters to the roster table of ufcql.db
    Duplicats are ignored
    arguments:
        cur:    sqlite cursor
        data:   list[list[roster_stats]] where roster stats is str or int
    '''
    ...
    

def db_update_fights(cur, data: list[list]):
    '''
    Adds new fights to the fights table of ufcql.db.
    Duplicate fights are ignored.
    arguments:
        cur: sqlite cursor
        data: list[list[fight_stats]] where fight stats is str or int
    '''
    ...
    

def db_update_rounds(cur, data: list[list]):
    '''
    Adds new rounds to the rounds table of ufcql.db.
    Duplicate fights are ignored.
    arguments:
        cur: sqlite cursor
        data: list[list[round_stats]] where fight stats is str or int
    '''
    ...
    

def db_update_results(cur, data: list[list]):
    '''
    Adds new results to the results table of ufcql.db.
    Duplicate fights are ignored.
    arguments:
        cur: sqlite cursor
        data: list[list[result_stats]] where fight stats is str or int
    '''
    ...