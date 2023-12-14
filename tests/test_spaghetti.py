import bs4
from icecream import ic
from helpers import (
    sort_function,
    get_id,
    get_order,
    r_base, roster,
    ed_base, event_details,
    fd_base, fight_details,
    fights,
    make_soup,
)
from scrape import (
    FightDetails,
    FighterDetails,
    # Index,
)

# This is what we are refactoring
from update import (
    update_index, 
    update_event_details, 
    update_fight_details, 
    update_fighter_details, 
    update_fights, 
    update_rounds, 
    update_results
)


################################################################################
# Test that the types are as we expect:
################################################################################
def test_make_soup_return_type():
    soup = make_soup('html/index.html')
    assert type(soup) == bs4.BeautifulSoup

def test_roster_is_list():
    assert type(roster) == list
    
def test_event_details_is_list():
    assert type(event_details) == list

def test_fight_details_is_list():
    assert type(fight_details) == list

def test_fights_returns_list():
    assert type(fights('2_a6a9ab5a824e8f66')) == list

def test_get_order_return_type():
    assert type(get_order('1_4acab67848e78327.html')) == int

def test_get_id_return_type():
    assert type(get_id('1_4acab67848e78327.html')) == str


################################################################################
# Testing that each directory is ordered.
# probably would be better to do some random sampling here...
# or loop the whole thing?
################################################################################
def test_event_details_is_sorted():
    assert (
        get_order(event_details[0]) < get_order(event_details[1]) 
        and get_order(event_details[-2]) < get_order(event_details[-1])
    )
    
def test_fight_details_is_sorted():
    assert (
        get_order(fight_details[0]) < get_order(fight_details[1]) 
        and get_order(fight_details[-2]) < get_order(fight_details[-1])
    )

def test_fights_returns_sorted():
    assert (
        fights('2_a6a9ab5a824e8f66')[0] < fights('2_a6a9ab5a824e8f66')[1]
        and fights('2_a6a9ab5a824e8f66')[-2] < fights('2_a6a9ab5a824e8f66')[-1]
    )

################################################################################
# TODO
# Testing the fight details
################################################################################
fd = FightDetails('html/fight_details/2_a6a9ab5a824e8f66/1_4acab67848e78327.html')

def test_FightDetails_returns_dict():
    assert type(fd) == dict

def test_FightDetails_returns_event_details_id():
    assert fd['event_details_id'] != None

def test_FightDetails_returns_fight_details_id():
    assert fd['fight_details_id'] != None

def test_FightDetails_returns_fight_order():
    assert fd['fight_order'] != None

def test_FightDetails_returns_red_fighter_id():
    assert fd['rid'] != None

def test_FightDetails_returns_blue_fighter_id():
    assert fd['bid'] != None

def test_FightDetails_returns_red_name():
    assert fd['r_name'] != None

def test_FightDetails_returns_blue_name():
    assert fd['b_name'] != None

def test_FightDetails_returns_red_result():
    assert fd['r_result'] != None

def test_FightDetails_returns_blue_result():
    assert fd['b_result'] != None

def test_FightDetails_returns_weightclass():
    assert fd['weightclass'] != None

def test_FightDetails_returns_if_title_fight():
    assert fd['for_title'] != None

def test_FightDetails_returns_method_of_victory():
    assert fd['method'] != None

def test_FightDetails_returns_total_rounds():
    assert fd['total_rounds'] != None

def test_FightDetails_returns_deciding_round():
    assert fd['round'] != None

def test_FightDetails_returns_time_format():
    assert fd['time_format'] != None

def test_FightDetails_returns_deciding_time():
    assert fd['time'] != None

def test_FightDetails_returns_bonuses():
    assert fd['bonuses'] != None

################################################################################
# TODO
# Testing the Round By Round data:
################################################################################
blue = fd['blue_rbr']
red  = fd['red_rbr' ]

def test_FightDetails_returns_red_rbr_data():
    # assert type(r_rbr) == dict
    assert red != None

def test_FightDetails_returns_blue_rbr_data():
    assert blue != None

def test_rbr_data_contains_sig_str_landed():
    ic(red)
    assert red['sig_str_landed'] != None and blue['sig_str_landed'] != None

def test_rbr_data_contains_sig_str_attempted():
    assert red['sig_str_att'] != None and blue['sig_str_att'] != None

# Given the current setup all of this will fail...
# def test_rbr_data_contains_sig_str_perc():
#     ...

# def test_rbr_data_contains_total_str_landed():
#     ...
# def test_rbr_data_contains_total_str_attempted():
#     ...

# def test_rbr_data_contains_total_td_landed():
#     ...
# def test_rbr_data_contains_total_td_attempted():
#     ...
# def test_rbr_data_contains_total_td_perc():
#     ...

# def test_rbr_data_contains_total_head_landed():
#     ...
# def test_rbr_data_contains_total_head_attempted():
#     ...

# def test_rbr_data_contains_total_body_landed():
#     ...
# def test_rbr_data_contains_total_body_attempted():
#     ...

# def test_rbr_data_contains_total_legs_landed():
#     ...
# def test_rbr_data_contains_total_legs_attempted():
#     ...

# def test_rbr_data_contains_total_distance_landed():
#     ...
# def test_rbr_data_contains_total_distance_attempted():
#     ...

# def test_rbr_data_contains_total_clinch_landed():
#     ...
# def test_rbr_data_contains_total_clinch_attempted():
#     ...

# def test_rbr_data_contains_total_ground_landed():
#     ...
# def test_rbr_data_contains_total_ground_attempted():
#     ...

# def test_rbr_data_contains_sub_att():
#     ...
# def test_rbr_data_contains_rev():
#     ...
# def test_rbr_data_contains_ctrl():
#     ...


# ################################################################################
# # TODO
# # Testing the database
# ################################################################################
# def test_db_returns_events():
#     ...
# def test_db_returns_roster():
#     ...
# def test_db_returns_fights():
#     ...
# def test_db_returns_rounds():
#     ...
# def test_db_returns_results():
#     ...
