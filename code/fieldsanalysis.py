# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 14:40:04 2017

@author: HOME
"""

import pandas as pd
import numpy as np

profiles_csv = "../results/profiles_friends.csv"
friends_folder = "../results/friends/"
mean_fill_csv = "../results/mean_fill.csv"

fields = "about, activities, bdate, books, career, city, country, facebook, " \
"games, has_mobile, has_photo, home_phone, instagram, interests, movies, music, " \
"personal_alcohol, personal_inspired_by, personal_life_main, personal_people_main, "\
"personal_political, personal_religion, personal_smoking, personallangs_1, quotes, "\
"relation, relation_partner, relatives_1_type, schools_1_city, site, skype, status, "\
"tv, twitter, universities_1_name"


fields = fields.split(", ")

# Count mean fulfillness for profiles

profiles = pd.read_csv(profiles_csv)

# Drop if no friends

profiles = profiles[profiles.number_of_friends > 0]

profiles_selected_fields = profiles[fields]
profiles_selected_fields["mean_fill"] = (len(fields) - profiles_selected_fields.isnull().sum(axis=1)) / len(fields)

all_means = pd.concat([profiles['uid'], profiles_selected_fields['mean_fill']], axis=1)
all_means = pd.concat([all_means, profiles['number_of_friends']], axis=1)
# Count mean and median fullfilness for friends profiles
friends_means = []
friends_medians = []
for profile_id in list(profiles['uid']):
    print profile_id
    friends_csv = friends_folder + str(profile_id) + ".csv"
    friends = pd.read_csv(friends_csv)
    
    # Check if no particular field - create a empty one
    for field in fields:
        if field not in friends:
            friends[field] = np.nan   
    
    friends_selected_fields = friends[fields]
    friends_selected_fields["mean_fill"] = (len(fields) -friends_selected_fields.isnull().sum(axis=1)) / len(fields)
    friends_means.append(friends_selected_fields["mean_fill"].mean())
    friends_medians.append(friends_selected_fields["mean_fill"].median())
    
all_means["friends_mean_fill"] = friends_means
all_means["friends_medians_fill"] = friends_medians

all_means.to_csv(mean_fill_csv, index = False)
    

