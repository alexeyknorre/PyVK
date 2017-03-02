# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 14:33:19 2017

@author: HOME
"""
import os
import pandas as pd
import friends2csv

friends_profiles = '..\\results\\friends\\'

# List comprehension

def get_numbers_of_friends(friends_profiles=friends_profiles):
    friends_csv = [f for f in os.listdir(friends_profiles) if os.path.isfile(os.path.join(friends_profiles, f))]
    c = 0
    for profile in friends_csv:
        c+=1
        print "*** {0}/{1} ***".format(c, len(friends_csv))
        friends2csv.add_friends_to_csv(profiles=friends_profiles+profile, 
                                   result_csv = friends_profiles+profile,
                                   drop_deactivated = False,
                                   get_friends_profiles = False)
    
    