# -*- coding: utf-8 -*-
"""
Created on Fri Nov 04 12:52:54 2016

@author: HOME
"""

import pandas as pd
import requests
import time   
import vk2csv

profiles = '..\\results\\profiles.csv'
result_csv = "..\\results\\profiles_friends.csv"

friends_profiles = '..\\results\\friends'
friends_response = '..\\results\\friends\\response.txt'


                              

def get_friends_ids(user_ids, get_friends_profiles = True):
    friends_ids = []
    number_of_friends = []
    counter = 1
    if get_friends_profiles:
        print "Getting friends profiles too."
    for user_id in user_ids:
        print("{0}/{1}, uid {2}".format(counter, len(user_ids), user_id))
        friends_user = requests.get('https://api.vk.com/method/friends.get?user_id={}'.format(user_id)).json()
        try:
            friends_user = friends_user[u'response']
        except:
            print friends_user
            friends_user = []
        time.sleep(0.334)
        
        # Get friends profiles and save them in separate tables
        if get_friends_profiles:
            if len(friends_user) == 0:
                print("No friends indicated")
            else:
                vk2csv.vk2csv(number_of_ids = friends_user, 
                              result_file = friends_profiles+"\\{}.csv".format(user_id),
                              response_file = friends_response,
                              delete_response = True)
                          
            
        counter += 1
        friends_ids.append(str(friends_user))
        number_of_friends.append(len(friends_user))
    print("Got friends!")
    return friends_ids,number_of_friends

def add_friends_to_csv(profiles=profiles, result_csv=result_csv, 
                       drop_deactivated = True,
                       get_friends_profiles = True):
    df = pd.read_csv(profiles, na_values = ["", "[]"], encoding = "utf-8")
    
    # Drop deactivated accounts
    if drop_deactivated:
        df = df[pd.isnull(df.deactivated)]
        df = df.drop("deactivated", 1)
    
    # Get friends for every ID
    ids = list(df.uid)
    
    friends_ids, number_of_friends = get_friends_ids(ids, get_friends_profiles)
    
    df["friends_ids"] = friends_ids
    df["number_of_friends"] = number_of_friends
    df.to_csv(result_csv, encoding = "utf-8", index = False)       